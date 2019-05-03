"""
The previous work found and counted the number of ways to score X amount of points in any possible hands. This work will focus on finding the REALISTIC ways to score X points in a game, adding the layer of complexity that a player is dealt 5 cards to start and would never choose a subset of 4 cards that would net them less points.  
- This will not take into account pegging 


So for each 2.6M possible combinations of 5 cards, choose to discard the card that makes the REMIANING 4 cards have the best score. Score will be the weighted sum of the possible values of points you could score based on the random card
v = sum( prob of point value * point value) given the remaining 52-5 cards. 
"""
import itertools
from cribbageLib_v4 import * 
#import matplotlib
#import matplotlib.pyplot as plt
import time 
from timer_decorator import *
import operator

count = 0		
# A dictionary whose keys are the point values (Supposedly 0 through 29 excluding 19) and whose values are the number of hands that get you that many points. 

deck = Deck()
#deck.shuffle()

cribbageDict = {}
combo_gen = itertools.combinations(deck.CardList,5)

hands = itertools.imap(Hand, combo_gen)

getEV = operator.methodcaller('getExpectationValue')
EVs = itertools.imap(getEV, hands)

EVs_out = np.array(list(EVs))


if __name__ == '__main__':
	multiprocessing.freeze_support()
	pool = multiprocessing.Pool(4)
	
	for expectation_value in EVs_out: 
		
		ev_rounded = int(10 * expectation_value) / 10.
		if ev_rounded in cribbageDict.keys():
			cribbageDict[ev_rounded] += 1 
		else:
			cribbageDict[ev_rounded] = 1
			
		count += 1

		#if count > 10000:
		#	break

	print cribbageDict


