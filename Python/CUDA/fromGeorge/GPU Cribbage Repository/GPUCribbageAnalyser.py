import numpy as np
import time
import operator as op
import math
from functools import reduce
from collections import Counter

from numba import vectorize, cuda, int64, int32, int8, uint64


import GPUCribbageDealer as dealer	

def main():
	
	start = time.time()
	score_counts = dealer.CalculateScoreOccurrence();
	tot = time.time() - start
	
	print "Total Run Time of CalculateScoreOccurence function: " + str(tot)
	print "Total Counts for each possible score:\n" 
	
	for i in range(0, score_counts.size):
		print str(i) + ":\t" + str(score_counts[i])
	
	print "Total Number of Scores Counted: " + str(np.sum(score_counts))


if __name__=='__main__':
    main()