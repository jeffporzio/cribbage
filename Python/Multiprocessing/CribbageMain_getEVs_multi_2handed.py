from cribbageLib_v4_snakes_2handed import *
import time 
from timer_decorator_multi import *

import multiprocessing
from functools import partial
import sys

"""
Going to try to get this to run on multiple cores.
This problem isn't really big enough to warrent a 
chunk_size, but the logic is sound. 10million chunk_size
is about 20 MB in RAM? Guesstimating a good size for a larger
problem would be 50million. 
"""

def getEVOfHand(combo):
	hand = Hand(list(combo)) # Take a list of card objects
	return hand.getExpectationValue()

if __name__ == "__main__":
	
	start = time.time()		
	
	# Chunking variables
	nProcs = 4
	chunk_size = 100000
	chunk_length_returned = chunk_size
	"""
	chunk_size = 250000   (100% CPU, 48% mem) no mem change
	chunk_size = 500000   (100% CPU, 48% mem) no mem change
	chunk_size = 10000000 (100% CPU, 54% mem)
	"""
	
	# Cribbage objects 
	deck = Deck()
	cribbageDict = {}
	combo_gen = itertools.combinations(deck.CardList,6)

	count = 0
	# Perform with max number of CPUs.
	while chunk_length_returned > 0:
		
		# Take a chunk and do the work
		chunk = itertools.islice(combo_gen, chunk_size)
		with multiprocessing.Pool(nProcs) as pool:	
			chunk_EVs = pool.map(getEVOfHand,chunk)			
		chunk_length_returned = len(chunk_EVs)
		
		count += chunk_length_returned
		print("Chunk finished. Counted: %i hands" %(count))
		
		# Save results from this chunk in the dict		
		for EV in chunk_EVs: 
			ev_rounded = int(10 * EV) / 10.
			if ev_rounded in cribbageDict.keys():
				cribbageDict[ev_rounded] += 1 
			else:
				cribbageDict[ev_rounded] = 1
				
		print()
		print(cribbageDict)
		print()
		
		
	for key in cribbageDict:
		print(key, '\t:\t', cribbageDict[key])
	
	stop = time.time()
	print( "Execution with calculation: ", stop-start, ' seconds')
	
	