import numpy as np
import time
import operator as op
import math
from functools import reduce


from numba import vectorize, cuda, int64, int8

	
HAND_SIZE = 6
DECK_SIZE = 52
binoms = binoms = np.zeros((HAND_SIZE+1) * (DECK_SIZE+1))

#Uses the GPU to generate a collection of unique card hand configurations
#It uses the thread and block id to get an encoding values unqiue to the thread. 
#Then, we use that encoding to generate a unique hand configuration
@cuda.jit
def createHands(Hands, binoms, hand_size, pass_floor, pass_size):
	
	#Thread id in a 1D block
	tx = cuda.threadIdx.x
	#Block id in a 1D grid
	ty = cuda.blockIdx.x
	#Block width, i.e. number of threads per block
	bw = cuda.blockDim.x
	
	#Compute flattened index inside the array
	#This will be our unique encoding
	#and also be the x position in the output array 
	pos = tx + (ty * bw)
	
	
	deck_size = Hands.size / Hands[0].size
	
	if pos < deck_size and pos < pass_size:  # Check array boundaries
		
		#the decoding algorithm begins!!
		#Im not going to try to explain this one because I am still working 
		#to fully understand how it really works 
		
		k = hand_size
		N = pass_floor + pos		
		card = k - 1
				
		while (binoms[(card * (hand_size+1)) + k] < N ):
			card = card +1
		
		while(card >= 0 and k > 0 ):
			b = (card * (hand_size+1)) + k
			if (binoms[b] <= N):
				N = N- binoms[b]				
				#save the card 
				Hands[pos][hand_size-k] = card
				k = k - 1
			card = card - 1
		
		

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

def main():

	#symbols = ["AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",		"AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",		"AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",		"AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS"];

	
	#N is the total number of hands we will generate using our cuda jit function
	#set to 270725 (52 choose 4) since that should be the maximum 4 card hands for a 52 card deck
	#because of the way that the encoding sequence progresses, you will see in the output that
	#there is a recognizable pattern leading up to the highest possible hand, [51, 50, 49, 48]
	
	#N = 270725 		#52 choose 4
	#N = 3679075400		#52 choose 9
	N = ncr(DECK_SIZE, HAND_SIZE)
	print "FULL SET SIZE: " + str(N)
	
	pass_size = 100000000
	pass_count = math.floor(N/pass_size) 
	if(N%pass_size != 0): pass_count+=1
	
	print "TOTAL PASSES:" + str(pass_count)
	
	#precomputed array of binom output values needed for 4 card hands
	#constant array saves some time, but I have commented this out and 
	#I'm using the generateBinoms function for now to test different hand and deck sizes
	#binoms = np.array([1, 0, 0, 0, 0,1, 1, 0, 0, 0,1, 2, 1, 0, 0,1, 3, 3, 1, 0,1, 4, 6, 4, 1,1, 5, 10, 10, 5,1, 6, 15, 20, 15,1, 7, 21, 35, 35,1, 8, 28, 56, 70,1, 9, 36, 84, 126,1, 10, 45, 120, 210,1, 11, 55, 165, 330,1, 12, 66, 220, 495,1, 13, 78, 286, 715,1, 14, 91, 364, 1001,1, 15, 105, 455, 1365,1, 16, 120, 560, 1820,1, 17, 136, 680, 2380,1, 18, 153, 816, 3060,1, 19, 171, 969, 3876,1, 20, 190, 1140, 4845,1, 21, 210, 1330, 5985,1, 22, 231, 1540, 7315,1, 23, 253, 1771, 8855,1, 24, 276, 2024, 10626,1, 25, 300, 2300, 12650,1, 26, 325, 2600, 14950,1, 27, 351, 2925, 17550,1, 28, 378, 3276, 20475,1, 29, 406, 3654, 23751,1, 30, 435, 4060, 27405,1, 31, 465, 4495, 31465,1, 32, 496, 4960, 35960,1, 33, 528, 5456, 40920,1, 34, 561, 5984, 46376,1, 35, 595, 6545, 52360,1, 36, 630, 7140, 58905,1, 37, 666, 7770, 66045,1, 38, 703, 8436, 73815,1, 39, 741, 9139, 82251,1, 40, 780, 9880, 91390,1, 41, 820, 10660, 101270,1, 42, 861, 11480, 111930,1, 43, 903, 12341, 123410,1, 44, 946, 13244, 135751,1, 45, 990, 14190, 148995,1, 46, 1035, 15180, 163185,1, 47, 1081, 16215, 178365,1, 48, 1128, 17296, 194580,1, 49, 1176, 18424, 211876,1, 50, 1225, 19600, 230300,1, 51, 1275, 20825, 249900])
	
	#generate the array  binom function output values
	#currently this appears to work for 4 card hands in a 52 card deck_size
	#I have not yet thoroughly tested other hand sizes, but initial testing with
	#a 5 card hand size showed possible problems with higher decks.
	start = time.time()  
	
	generateBinoms(DECK_SIZE+1, HAND_SIZE +1)
	tot = time.time() - start	
	print "generateBinoms Function took % seconds" % tot
	print "binoms array length:" + str(binoms.size)
	
	Hands = np.zeros((pass_size,HAND_SIZE), dtype=np.int8)
	
	#not exactly sure what the optimal thread, block counts are, feel free to play around with this
	#threads per block
	tpb = 1024
	#blocks per group
	bpg =(Hands.size / (tpb - 1))
	
	i =0
	sample_size = 10

	full_start_time = time.time()
	while(i+ pass_size < N):
		
		start = time.time()  
		createHands[bpg, tpb](Hands, binoms, HAND_SIZE, i, pass_size)
		tot = time.time() - start	
		print "createHands Function took % seconds" % tot				
		print "Hand Start:  " + str(Hands[:sample_size])
		print "Hand End: " + str(Hands[-sample_size:])
		i = i + pass_size
		
	remainder = N-i
	
	if (remainder > 0 ):		
		Hands = np.zeros((remainder,HAND_SIZE), dtype=np.int8)
		bpg =(Hands.size / (tpb - 1))
		start = time.time()
		#print "Hand Size:  " + str(Hands.size)
		createHands[bpg, tpb](Hands, binoms, HAND_SIZE, i,remainder)
		tot = time.time() - start	
		print "createHands Function took %s seconds" % tot				
		print "Hand Start:  " + str(Hands[:sample_size])
		print "Hand End: " + str(Hands[-sample_size:])
	
	full_tot_time = time.time()- full_start_time
	print "Full createHands Function Call Time: %s seconds" % full_tot_time
	
	
if __name__=='__main__':
    main()