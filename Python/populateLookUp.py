import itertools
from cribbageLib_v4 import * 
#import matplotlib
#import matplotlib.pyplot as plt
import time 
from timer_decorator import *


def populateLookUp():
	start = time.time()
	print "Starting counting..."
	count = 0		
	# A dictionary whose keys are the point values (Supposedly 0 through 29 excluding 19) and whose values are the number of hands that get you that many points. 

	deck = Deck()

	look_up_dict = {}
	combo_gen = itertools.combinations(deck.CardList,5)

	for combo in combo_gen:	
		
		hand = Hand(list(combo)) # Take a list of card objects
		
		for _ in xrange(0,5):
			
			score = hand.countHand()
			
			look_up_dict[hand.hash_string] = score
			#look_up_dict[hand] = score
			
			#print hand.hash_string,
			#hand.printHand()
			
			hand.rotateHand()
			count += 1
			
		#if count > 10000:
		#	break
	
	print 
	print "Count: ", count 
	print "Length: ", len(look_up_dict.keys())
	print 
	
	save_file = "cribbage_lookup_table.txt"
	with open(save_file, 'w') as f: 
		for key in look_up_dict:
			f.write(key + ',' + str(look_up_dict[key])+'\n')
	
	stop = time.time()
	print "Execution for counting took: ", stop-start, ' seconds'
	
populateLookUp()
	
	