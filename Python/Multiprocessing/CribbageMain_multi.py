#from cribbageLib_v4_withLookUp_multi import *
from cribbageLib_v4_snakes import *
import time 
from timer_decorator_multi import *

import multiprocessing
from functools import partial

"""
Going to try to get this to run on multiple cores.
"""

def getScoresOfHand(combo):
	hand = Hand(list(combo)) # Take a list of card objects
	
	scores = [0,0,0,0,0]
	
	for i in range(0,5):
		
		scores[i] = hand.countHand()
		#score = look_up_dict[hand.hash_string]
		
		"""
		if score in cribbageDict.keys():
			cribbageDict[score] += 1 
		else: 
			cribbageDict[score] = 1
		"""
		
		hand.rotateHand()
	
	return scores


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
	
	deck = Deck()

	cribbageDict = {}
	combo_gen = itertools.combinations(deck.CardList,5)

	# multiprocessing?
	with multiprocessing.Pool() as pool:
		all_scores = pool.map(getScoresOfHand,combo_gen)			

	
	for scores in all_scores:
		for score in scores: 
			if score in cribbageDict.keys():
				cribbageDict[score] += 1 
			else:
				cribbageDict[score] = 1
	
	
	for key in cribbageDict:
		print(key, '\t:\t', cribbageDict[key])
	
	stop = time.time()
	print( "Execution with calculation: ", stop-start, ' seconds')
	
	