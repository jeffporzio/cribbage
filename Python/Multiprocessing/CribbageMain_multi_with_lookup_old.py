#from cribbageLib_v4_withLookUp_multi import *
from cribbageLib_v4_snakes import *
import time 
from timer_decorator_multi import *

import multiprocessing
from functools import partial

"""
Going to try to get this to run on multiple cores.
"""

def getScoresOfHand(combo,look_up_dict={}):
	hand = Hand(list(combo)) # Take a list of card objects
	
	for _ in range(0,5):
		
		score = hand.countHand()
		#score = look_up_dict[hand.hash_string]
		hand.rotateHand()


if __name__ == "__main__":
	
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
	start = time.time()		


	deck = Deck()

	cribbageDict = {}
	combo_gen = itertools.combinations(deck.CardList,5)

	partial_func = partial(getScoresOfHand, look_up_dict=look_up_dict)
	
	# multiprocessing?
	with multiprocessing.Pool() as pool:
		pool.map(partial_func,combo_gen)			
	"""
	for combo in combo_gen: 
		partial_func(combo)
	"""
	for key in cribbageDict:
		print(key, '\t:\t', cribbageDict[key])
	
	stop = time.time()
	print( "Execution with calculation: ", stop-start, ' seconds')
	
	