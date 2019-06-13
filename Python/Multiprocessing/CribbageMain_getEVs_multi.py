#from cribbageLib_v4_withLookUp_multi import *
from cribbageLib_v4_snakes import *
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
	
	"""
	#look_up_dict = constructLookUpDict()
	start = time.time()
	print("Starting import...")
	look_up_dict = {}
	look_up_file = "..\cribbage_lookup_table.txt"
	with open(look_up_file, 'r') as f: 
		for line in f:
			key, val = line.split(',')
			look_up_dict[key] = int(val)
	end = time.time()
	print("Finished import after %f seconds." % (end-start))
	"""
	start = time.time()		
	
	# Chunking variables
	nProcs = 4
	chunk_size = 1000000
	chunk_length_returned = chunk_size
	"""
	chunk_size = 250000   (100% CPU, 48% mem) no mem change
	chunk_size = 500000   (100% CPU, 48% mem) no mem change
	chunk_size = 10000000 (100% CPU, 54% mem)
	"""
	
	# Cribbage objects 
	deck = Deck()
	cribbageDict = {}
	combo_gen = itertools.combinations(deck.CardList,5)

	# Perform with max number of CPUs.
	while chunk_length_returned > 0:
		
		# Take a chunk and do the work
		chunk = itertools.islice(combo_gen, chunk_size)
		with multiprocessing.Pool(nProcs) as pool:	
			chunk_EVs = pool.map(getEVOfHand,chunk)			
		chunk_length_returned = len(chunk_EVs)
		
		print("Size of chunk_scores in memory %i" %(sys.getsizeof(chunk_EVs)))
		
		# Save results from this chunk in the dict		
		for EV in chunk_EVs: 
			if EV in cribbageDict.keys():
				cribbageDict[EV] += 1 
			else:
				cribbageDict[EV] = 1
		
		
	for key in cribbageDict:
		print(key, '\t:\t', cribbageDict[key])
	
	stop = time.time()
	print( "Execution with calculation: ", stop-start, ' seconds')
	
	