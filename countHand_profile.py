from cribbageLib_v3 import * 
import matplotlib
import matplotlib.pyplot as plt
import time 
from timer_decorator import *

@timer_this_func
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
		
		expectation_value = hand.countHand()
		if expectation_value in cribbageDict.keys():
			cribbageDict[expectation_value] += 1 
		else:
			cribbageDict[expectation_value] = 1
			
		count += 1

		if count > 0:
			break

	print cribbageDict
	
	
main()