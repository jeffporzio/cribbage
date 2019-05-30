from cribbageLib_v4 import * #v4 takes 
#from cribbageLib_v5 import * #v5 takes 
#import matplotlib
#import matplotlib.pyplot as plt
import time 
from timer_decorator import *

@timer_this_func_stats
def main():
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
			
			score = hand.countHand()
			if score in cribbageDict.keys():
				cribbageDict[score] += 1 
			else:
				cribbageDict[score] = 1
			
			hand.rotateHand()
			count += 1
			
			if score == '19':
				hand.pointBreakDown()
			

	for key in cribbageDict:
		print key, '\t:\t', cribbageDict[key]
	print count
	
main()