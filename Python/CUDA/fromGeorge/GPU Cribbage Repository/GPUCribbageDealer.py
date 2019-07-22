import numpy as np
import time
import operator as op
import math
from functools import reduce
from collections import Counter


from numba import vectorize, cuda, int64, int32, int8, uint64

import GPUCounter 
 
MAX_SCORE = 29
HAND_SIZE = 6
DECK_SIZE = 52
binoms = binoms = np.zeros((HAND_SIZE+1) * (DECK_SIZE+1), dtype=np.int32)

#array of all possible arrangements for 6choose4... now correct, with 15 items
four_array = np.array([[0,1,2,3],[0,1,2,4],[0,1,2,5],[0,1,3,4],[0,1,3,5],[0,1,4,5],[0,2,3,4],[0,2,3,5],[0,2,4,5],[0,3,4,5],[1,2,3,4],[1,2,3,5],[1,2,4,5],[1,3,4,5],[2,3,4,5]])
#array of indexes of cards to discard for corresponding item in four_array, used to simplify output for verification of hands
disc_array = np.array([[4,5],[3,5],[3,4],[2,5],[2,4],[2,3],[1,5],[1,4],[1,3],[1,2],[0,5],[0,4],[0,3],[0,2],[0,1]])


def CalculateScoreOccurrence():

	#Array to hold the total count for 	every possible score
	#we simply use the index as the reference for the score it self
	#For example ScoreCountTotal[19] would hold the number of times
	#that a hand scores 19 points.... is should always be zero in this case	
	ScoreCountTotals = np.zeros(MAX_SCORE +1, dtype=np.uint64)

	#We want to run exactly one thread for each possible hand configuration
	#each hand has 15 (6choose4) possible arrangements
	#each arrangement has 46 possible cut cards 
	#15*46 is 690, so we need 690 threads for each possible 52choose6 hand	
	#for a total of (52choose6) * 690 = 14,047,378,800 different possible deals
	#each possible deal will be processed on a different thread		
	N = ncr(DECK_SIZE, HAND_SIZE) *690

	#total max number of threads per run
	#14 billion different deals is too much for one output array
	#so I am processing them in separate "passes" of 100 million
	#each pass processes a different 100million deal chunk, out of the whole dataset
	#feel free to play with this, 100mil seemed to be about otpimal, but I didnt calculate this
	#value based on anything, so there is likely room for improvement
	pass_size = 100000000
	
	
	pass_count = math.floor(N/pass_size) 
	if(N%pass_size != 0): pass_count+=1		
		
	print "FULL SET SIZE: " + str(N)
	print "TOTAL PASSES:" + str(pass_count)

	#create the binoms array we will be passing to the gpu
	generateBinoms(DECK_SIZE+1, HAND_SIZE +1)


	Cards = np.zeros((pass_size,HAND_SIZE+1), dtype=np.int8)
	Scores = np.zeros((pass_size), dtype=np.int8)
	
	#not exactly sure what the optimal thread, block counts are, feel free to play around with this. 
	#I do know multiples of 32 should be optimal, but the difference is negligible
	#threads per block
	tpb = 1024
	#blocks per group
	bpg =(Cards.size / tpb )+1
	
	i =0
	pc=0

	#as long as the remaining portion of the card set is bigger than the pass_size
	#we run each pass in a loop, running pass_size threads each time
	while(i+ pass_size < N): 
		CreateDeals[bpg, tpb](Cards, binoms, i, pass_size, Scores)
		GPUCounter.CountScores(Scores, ScoreCountTotals)		
		i = i + pass_size
		pc += 1
	remainder = N-i
	
	#run the last pass containing any remaining deals that still need to be counted
	if (remainder > 0 ):		
		Cards = np.zeros((remainder,HAND_SIZE+1), dtype=np.int8)		
		Scores = np.zeros(remainder, dtype=np.int8)		
		bpg =(Cards.size / (tpb - 1))
		CreateDeals[bpg, tpb](Cards, binoms,  i,remainder, Scores)
		GPUCounter.CountScores(Scores, ScoreCountTotals)		
		
	return ScoreCountTotals



#Uses the GPU to generate a collection of unique card hand configurations
#It uses the thread and block id to get an encoding values unqiue to the thread. 
#Then, we use that encoding to generate a unique hand configuration
#Cards:An array of lists of all Cards in the deal. Every 7 congiuous cells in the array make up a list
#Cards 0 - 4 are the cards chosen for the hand.  Card 5 is the cut card, and cards 6 and 7 are the discarded cards
#binoms: precomputed array we utilize to calculate the 52choose6 hand from an encoding value
#HAND_SIZE: # of cards actually dealt to the player, in this case it is 6
#pass_floop: 
@cuda.jit	#(argtypes=[int8[:], int32[:], int32, int32, int32], target='gpu')
def CreateDeals(Cards, binoms, pass_floor, pass_size, score_out):
	
	#HAND_SIZE=HAND_SIZE
	#Values = cuda.shared.array(shape=(5), dtype=np.int64)
	
	#Thread id in a 1D block
	tx = cuda.threadIdx.x
	#Block id in a 1D grid
	ty = cuda.blockIdx.x
	#Block width, i.e. number of threads per block
	bw = cuda.blockDim.x
	
	#This equation computes a unique index for the thread it is running on
	#every thread is part of a block of (bw) threads
	#every block has a unique id (ty)
	#every thread has a unique id within its block (tx), with a value from 0 to (bw)
	#the equation below gives us a unique index value based on those ids
	#ranging from 0 to N, where N is the total number of threads running in all blocks
	#for example, if tx = 22 and ty= 10, and every block contains 64 threads
	#then the thread_index is (22 + (10 * 64)) which equals 662
	thread_index = (tx + (ty * bw))
	
	#we divide the thread_index by 690 to get the encoding, so that each encoding will run on 690 consecutive threads
	#so when the thread index is some value from 0 to 689, encoding will be zero
	#then from 690 to 1379, ecoding will equal 1, and so on for each thread_index
	encoding = (thread_index/690)
	
	#grab the remainder to get position within the 690 threads per encoding
	#as an example, if we were at thread_index 
	r =  thread_index%690
	
	#this is the position in the array of 6c4 index combos
	#divide remainer by 46, so we get 46 consecutive threads per c4i value
	#this will cycle from 46 0s to 46 15s within a single encoding cycle
	c4i = (r/46)
	
	#grab remainder to get position within the 46 cards per ordering value
	#this will represent one of the 46 possible cut cards
	cut_card= r%46
	
	deck_size = Cards.size / Cards[0].size
	
	if thread_index < deck_size and thread_index < pass_size:  # Check array boundaries
		
		#the decoding algorithm begins
		#this generates our six card deal
		k = HAND_SIZE
		N = pass_floor/690 + encoding		
		card = k - 1				
		while (binoms[(card * (HAND_SIZE+1)) + k] < N ):
			card = card +1		
		while(card >= 0 and k > 0 ):
			b = (card * (HAND_SIZE+1)) + k
			if (binoms[b] <= N):
				N = N- binoms[b]				
				#save the card 
				Cards[thread_index][HAND_SIZE-k] = card
				k = k - 1
			card = card - 1
		
		#to find the correct cut cards we must
		#skip over cards already in the 6 card hand
		#to do this we add 1 to the cut_card value, for each card in the hand
		#with a value that is less than or equal to the cut card's value
		if(cut_card>= Cards[thread_index][5]):
			cut_card += 1
		if(cut_card>= Cards[thread_index][4]):
			cut_card += 1
		if(cut_card>= Cards[thread_index][3]):
			cut_card += 1
		if(cut_card>= Cards[thread_index][2]):
			cut_card += 1
		if(cut_card>= Cards[thread_index][1]):
			cut_card += 1
		if(cut_card>= Cards[thread_index][0]):
			cut_card += 1
		
		#Set the cut card to the 7th position in the hand
		
		Cards[thread_index][6] = cut_card
		
		fours = cuda.const.array_like(four_array)
		discs = cuda.const.array_like(disc_array)
		
		F = cuda.local.array(5, int8)	
		
		#grab cards from the hand in the order specified in fours 
		#for the given iteration, mod 12 to get Face Value
		F[0] = Cards[thread_index][fours[c4i][0]] 
		F[1] = Cards[thread_index][fours[c4i][1]] 
		F[2] = Cards[thread_index][fours[c4i][2]] 
		F[3] = Cards[thread_index][fours[c4i][3]] 
		#grab the cut card and throw it on the end
		F[4] = cut_card
		#get discard cards for reference
		D1 = Cards[thread_index][discs[c4i][0]] 
		D2 = Cards[thread_index][discs[c4i][1]] 
		
		#reset output hand to match reorganization, for verification
		Cards[thread_index][0] = F[0]
		Cards[thread_index][1] = F[1]
		Cards[thread_index][2] = F[2]
		Cards[thread_index][3] = F[3]
		Cards[thread_index][4] = F[4]
		Cards[thread_index][5] = D1
		Cards[thread_index][6] = D2
		
		
		#get an array of the face values for the cards
		F[0] = F[0] %13
		F[1] = F[1] %13
		F[2] = F[2] %13
		F[3] = F[3] %13
		F[4] = F[4] %13
		
		
		#cheap sort, a bubble sort I think.. but its quick enough for a set this size... something like 15 iterations
		for i in range(0,5):
			min=i
			for j in range(i+1,5):		
				if(F[j] < F[min]):
					min= j
			if(min > i):	
				tmp = F[i]
				F[i]= F[min]
				F[min] = tmp
	
		#score counting time!!

		score = 0
	
		#get points for pairs, triples, quads
		#this one is kind of fun..  s starts at zero, e at s+1
		#if they are the same face value, increment e til one doesnt match
		#assign score based on the count,
		#repeat process with s at the last non-match, e
		s=0
		e=s+1
		
		while s<4 and e < 5:
			count =1
			while(e <5 and F[s] == F[e]):
				count += 1
				e += 1

			if(count==2): score += 2
			if(count==3): score += 6
			if(count==4): score += 12	

			s= e
			e= s+1
			
		#get points for runs
		#the hand is sorted so we just have to step through it, and count the cards in sequence
		#m tracks multiplier for a single pair, triples, we increase it instead of increasing the count, for each sequential value match
		#tm tracks multiplier over multiple pairs, every time we find the next card in the sequence, mutiply tm by m and reset m
		
		
		s=0
		e=1
		while  s<3 and e < 5:
			count =1
			m=1
			tm=1
			while(e <5 and (F[e] == F[s]+count or F[e] == F[e-1])):
				if(F[e] == F[e-1]):
					m += 1
				elif(F[e] == F[s]+count):
					count += 1
					tm*= m
					m=1

				e += 1
				
			s= e
			e= s+1
			if(count >=3):
				score += count * tm
		

		#get the card counting values for 15s
		F[0] = (F[0]) + 1		
		F[1] = (F[1]) + 1
		F[2] = (F[2]) + 1
		F[3] = (F[3]) + 1
		F[4] = (F[4]) + 1
		
		for i in range(0,5):
			if(F[i] > 10): F[i] = 10
			
		
		#check all possible card combos for 15s... only 25 in total
		if(F[0] + F[1] + F[2] + F[3] +F[4] == 15):
			score+=2
		if(F[0] + F[1] + F[2] + F[3] == 15):
			score+=2
		if(F[0] + F[1] + F[2] + F[4] == 15):
			score+=2
		if(F[0] + F[1] + F[3] + F[4] == 15):
			score+=2
		if(F[0] + F[2] + F[3] + F[4] == 15):
			score+=2
		if(F[1] + F[2] + F[3] + F[4] == 15):
			score+=2
		
		if(F[0] + F[1] + F[2] == 15):
			score+=2
		if(F[0] + F[1] + F[3] == 15):
			score+=2
		if(F[0] + F[1] + F[4] == 15):
			score+=2
		if(F[0] + F[2] + F[3] == 15):
			score+=2
		if(F[0] + F[2] + F[4] == 15):
			score+=2
		if(F[0] + F[3] + F[4] == 15):
			score+=2
		if(F[1] + F[2] + F[3] == 15):
			score+=2
		if(F[1] + F[2] + F[4] == 15):
			score+=2
		if(F[1] + F[3] + F[4] == 15):
			score+=2
		if(F[2] + F[3] + F[4] == 15):
			score+=2
			
		if(F[0] + F[1] == 15):
			score+=2
		if(F[0] + F[2] == 15):
			score+=2
		if(F[0] + F[3] == 15):
			score+=2
		if(F[0] + F[4] == 15):
			score+=2
		if(F[1] + F[2] == 15):
			score+=2
		if(F[1] + F[3] == 15):
			score+=2
		if(F[1] + F[4] == 15):
			score+=2
		if(F[2] + F[3] == 15):
			score+=2
		if(F[2] + F[4] == 15):
			score+=2
		if(F[3] + F[4] == 15):
			score+=2
	
		#get the points for flushes
		if(Cards[thread_index][0]/13 == Cards[thread_index][1]/13 and
			Cards[thread_index][0]/13 == Cards[thread_index][2]/13 and
			Cards[thread_index][0]/13 == Cards[thread_index][3]/13  ):
				score +=4
				if(Cards[thread_index][0]/13 == Cards[thread_index][4]/13):
					score+=1
		
		#check for right jack
		cut_suit = Cards[thread_index][4]/13
		
		if(Cards[thread_index][0] %13 == 10 and Cards[thread_index][0] /13 == cut_suit):
			score += 1
		if(Cards[thread_index][1] %13 == 10 and Cards[thread_index][1] /13 == cut_suit):
			score += 1	
		if(Cards[thread_index][2] %13 == 10 and Cards[thread_index][2] /13 == cut_suit):
			score += 1
		if(Cards[thread_index][3] %13 == 10 and Cards[thread_index][3] /13 == cut_suit):
			score += 1
					
		score_out[thread_index] = score
	
#this allows us to control which cards are skipped 
#when we generate a card sequence from an encoding
#its recursive though, which is not good for a GPU function, plus its slow
#but for a finite deck/hand size, we can figure out all of the output values needed
#and map them to an array, to look up later
def binom(n, k):
	if (k > n): return 0
	if (n == k): return 1
	if (k == 0): return 1
	if binoms[(n*(HAND_SIZE + 1)) + k] > 0: return binoms[(n*(HAND_SIZE + 1)) + k];
	return binom(n - 1, k - 1) + binom(n - 1, k)


#precomputes all outputs we will need from the binom function above
#and saves them in an array for later use
def generateBinoms(max_n, max_k):
		
	for n in range(0, max_n):
		for k in range(0, max_k):			
			binoms[(n*max_k) + k] = binom(n,k)

#def generate15s():

# calculate n choose r	
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


symbols = ["AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD","AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH","AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC","AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS"];


#Prints Hand info to the screen, using a score based filter to reduce the output
#feel free to mess with this
def outputData(Cards,Scores,pass_size):
	
	for j in range(0,pass_size):
		#if(Scores[j] >= 29 ):
		#if Cards[j][0] == 7 and Cards[j][1]==7:
		#if(j == 4837474):
			print "Deal #:\t" + str(j)
			print "In Hand:\t" + str(Cards[j][0])+ ", " + str(Cards[j][1]) + ", " + str(Cards[j][2])+ ", " + str(Cards[j][3]) + ", " + str(Cards[j][4])
			print "Discarded:\t" + str(Cards[j][5]) + ", " + str(Cards[j][6])
			#print "In Hand:\t" + symbols[Cards[j][0]]+ ", " + symbols[Cards[j][1]] + ", " + symbols[Cards[j][2]]+ ", " + symbols[Cards[j][3]] + ", " + symbols[Cards[j][4]]
			#print "Discarded:\t" + symbols[Cards[j][5]] + ", " + symbols[Cards[j][6]]			
			#print "Score:\t\t" + str(Scores[j])
			#print