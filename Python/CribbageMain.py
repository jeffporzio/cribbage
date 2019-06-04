from cribbageLib_v4 import * #v4 takes 197 +/- 10 seconds
#from cribbageLib_v5 import * #v5 takes 240 +/- 22 seconds
#import matplotlib
#import matplotlib.pyplot as plt
import time 
from timer_decorator import *

"""
using dict[hand.hash_string] took 240, 55 secs
Keep getting hash collisions trying to use dict[hand] because my 
	hand.__hash__() isn't very good. 
"""

def constructLookUpDict():
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
			
			hand.rotateHand()
			count += 1
			
		#if count > 10000:
		#	break
	
	print 
	print "Count: ", count 
	print "Length: ", len(look_up_dict.keys())
	print 
	
	stop = time.time()
	print "Execution for counting took: ", stop-start, ' seconds'
	
	return look_up_dict


def redoWithLookUp():
	

	look_up_dict = constructLookUpDict()
	
	start = time.time()
	
	count = 0		
	# A dictionary whose keys are the point values (Supposedly 0 through 29 excluding 19) and whose values are the number of hands that get you that many points. 

	deck = Deck()
	#deck.shuffle()
	#deck.printLogicalIDs()

	cribbageDict = {}
	combo_gen = itertools.combinations(deck.CardList,5)

	for combo in combo_gen:	
		
		hand = Hand(list(combo)) # Take a list of card objects
		
		for _ in xrange(0,5):
			
			score = look_up_dict[hand.hash_string]
			"""
			try: 
				score = look_up_dict[hand]
			except KeyError:
				hand.printHand()
				score = hand.countHand()
			"""
			if score in cribbageDict.keys():
				cribbageDict[score] += 1 
			else:
				cribbageDict[score] = 1
			
			hand.rotateHand()
			count += 1			

	for key in cribbageDict:
		print key, '\t:\t', cribbageDict[key]
	print count
	
	stop = time.time()
	print "Execution with look-ups took: ", stop-start, ' seconds'

redoWithLookUp()