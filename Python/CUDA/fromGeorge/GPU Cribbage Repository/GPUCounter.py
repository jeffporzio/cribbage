import numpy as np
import time
import operator as op
import math
from functools import reduce
from collections import Counter

from numba import vectorize, cuda, int64, int32, int8, uint64

@cuda.jit
def countScores(Scores, Tallies, chunk_size, max_score):
	
	#Values = cuda.shared.array(shape=(5), dtype=np.int64)
	
	#Thread id in a 1D block
	tx = cuda.threadIdx.x
	#Block id in a 1D grid
	ty = cuda.blockIdx.x
	#Block width, i.e. number of threads per block
	bw = cuda.blockDim.x
	
	#Compute flattened index inside the array
	thread_index = (tx + (ty * bw))
	
	#since each thread will process a chunk of the array
	#we need to calculate the first index for this thread's chunk of scores
	score_index = thread_index *chunk_size
	
	#the tallys will be groups of 30 consecutive array cells
	#each containing the score count for the scores 0 to 29
	#each cells index mod 30 will equal the score it represents
	tally_index = thread_index *(max_score + 1)
	
	#lots of bounds checks.... we might not need all of these, just being cautious
	if(tally_index + max_score < Tallies.size):
		
		#loop through each item in the thread's chunk of scores
		#use the score itself to identify the needed index, 
		#and just iterate up one at that cell
		for i in range(0,chunk_size):	
			ci = i+ score_index
			if(ci < Scores.size and tally_index + Scores[ci] < Tallies.size and Scores[ci] <= max_score):				
				Tallies[ tally_index + Scores[ci]] += 1
		
	
	
#this function takes and array of scores,
def CountScores(Scores, Totals):
	
	max_score = 29
	# Totals = np.zeros(30, dtype=np.int64)
	
	#the size of the sub-array that will be counted within each GPU thread
	chunk_size = 100000
	
	tpb = 32
	#blocks per group
	bpg =((Scores.size / tpb ) / chunk_size) + 1
	
	chunk_count = (Scores.size / chunk_size) + 1
	#cr = Scores.size % (chunk_size-1)
	
	#we need a separate tally list for each thread
	#so we will reserve evert 30 contiguous cells in the array for each one of the threads
	tally_count = (30* (chunk_count))
	Tallies = np.zeros(tally_count, dtype=np.int64)
	
	countScores[bpg, tpb](Scores, Tallies, chunk_size, max_score)
	
	
	for i in range(0,tally_count):
		Totals[i % 30] += Tallies[ i ]
	
	return Totals
		