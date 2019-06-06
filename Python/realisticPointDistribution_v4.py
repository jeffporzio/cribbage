"""
The previous work found and counted the number of ways to score X amount of points in any possible hands. This work will focus on finding the REALISTIC ways to score X points in a game, adding the layer of complexity that a player is dealt 5 cards to start and would never choose a subset of 4 cards that would net them less points.  
- This will not take into account pegging 


So for each 2.6M possible combinations of 5 cards, choose to discard the card that makes the REMIANING 4 cards have the best score. Score will be the weighted sum of the possible values of points you could score based on the random card
v = sum( prob of point value * point value) given the remaining 52-5 cards. 
"""
import itertools
from cribbageLib_v4_withLookUp import * 
#from cribbageLib_v4 import * 
#import matplotlib
#import matplotlib.pyplot as plt
import time 
from timer_decorator import *
#from populateLookUp import populateLookUp

@timer_this_func
def main():


	start = time.time()
	print "Starting import..."
	look_up_dict = {}
	look_up_file = "cribbage_lookup_table.txt"
	with open(look_up_file, 'r') as f: 
		for line in f:
			key, val = line.split(',')
			look_up_dict[key] = int(val)
	end = time.time()
	print "Finished import after %f seconds." % (end-start)
			
	count = 0		
	checkpoint_num = 10000
	# A dictionary whose keys are the point values (Supposedly 0 through 29 excluding 19) and whose values are the number of hands that get you that many points. 

	deck = Deck()
	#deck.shuffle()
	
	cribbageDict = {}
	combo_gen = itertools.combinations(deck.CardList,5)

	start = time.time()
	for combo in combo_gen:	
		
		hand = Hand(list(combo)) # Take a list of card objects
		
		if (count % checkpoint_num) == 0 and count > 0:
			localtime = time.asctime( time.localtime(time.time()) )
			end = time.time()
			delta_t = end - start

			print '%i hands counted in %f secs. %f hands/sec' % (count, delta_t, checkpoint_num/delta_t)
			
			start = time.time()
		
		#expectation_value = hand.getExpectationValue()
		expectation_value = hand.getExpectationValue(look_up_dict)
		
		
		#ev_rounded = int(10 * expectation_value) / 10.
		ev_rounded = np.round(expectation_value)
		
		if ev_rounded in cribbageDict.keys():
			cribbageDict[ev_rounded] += 1 
		else:
			cribbageDict[ev_rounded] = 1
			
		count += 1

		#if count > 10000:
		#    break
	
	print cribbageDict
	
	save_file = "realisticDist_v4_out_nearestPoint.txt"
	with open(save_file, 'w') as f: 
		for key in look_up_dict:
			f.write(key + ',' + str(look_up_dict[key])+'\n')
	
	"""
	with look-ups, calculating 10000 hands in about 30 seconds.
	"""

	
	
main()