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

import multiprocessing 


deck = Deck()
#deck.shuffle()

cribbageDict = {}
combo_gen = itertools.combinations(deck.CardList,5)

hands = itertools.imap(Hand, combo_gen) # Hand generator
getEV = operator.methodcaller('getExpectationValue') # Method

def countHand(self):
	"""
	Should return a point value for this hand (where to common card is the 4th index).
	
	Ways to get points by card number involved: 
	2	Pairs, 15s, Right Jack
	3	Three of a kind*, runs, 15s
	4	Four of a kind*, runs, 15s, flush (in hand)
	5	Runs, flush (all cards), 15s	
	*** TooK and FooK are just combinations of pairs, so no need to look for them explicitly.
	15s can be made of any number of cards, so need to check those each time.
	"""

	points = 0
	JACK = 11
	####################
	# Two card points: #
	####################
	twoCardCombos = itertools.combinations(self.CardList,2)
	# pairs, trips, and quads
	for twoCardCombo in twoCardCombos:
		if twoCardCombo[0].number == twoCardCombo[1].number:
			points += 2
	
	# Right Jack
	for card in self.CardList[0:4]:
		if (card.number == JACK) and (card.suit == self.CardList[4].suit):
			points += 1
	
	######################
	# Three card points: #
	######################
	# No unique ones here 
	
	
	#####################
	# Four card points: #
	#####################		
	# In hand flush
	isInHandFlush = (
	 self.CardList[0].suit == self.CardList[1].suit and 
	 self.CardList[0].suit == self.CardList[2].suit and  
	 self.CardList[0].suit == self.CardList[3].suit
	 )
	if isInHandFlush:
		points += 4
		
	#####################
	# Five card points: #
	#####################
	# Add another point if the common card is the same suit as your flush		
	if isInHandFlush and (self.CardList[0].suit == self.CardList[4].suit):
		points += 1 
	
	###########
	# All 15s #
	###########
	"""
	This section is slowing the code down. There are only
	26 combos to go through. The slow part is the actual 
	"card in combo" and total += card.value
	"""
	"""
	for n in range(2,6):
		combos = itertools.combinations(self.CardList,n)
		for combo in combos:

			total = 0
			for card in combo:       # Here are the slow lines!
				total += card.value  #
			
			total = sum([card.value for card in combo])

			if total == 15:
				points += 2
	"""
	valueList = [card.value for card in self.CardList]	
	for n in range(2,6):
		
		combos = itertools.combinations(valueList,n)
		
		#for combo in combos:
		#	total = sum(combo)
		
		# This is marginally faster than the other commented versions
		for total in map(sum, combos):
			if total == 15:
				points += 2

	#####################
	# Runs of all kinds #
	#####################
	points += getRunPoints(self.CardList)


	return str(points)


def getExpectationValue(self):
	
	# Create a deck to iterate through 
	deck = Deck()if __name__ == '__main__':
	# Remove the five cards in this hand from the deck			multiprocessing.freeze_support()
	ind_to_remove = []	p = multiprocessing.Pool(4)
	ind = 0	
	for card_in_deck in deck.CardList:	count = 0
		for card_in_hand in self.CardList:	for expectation_value in p.imap_unordered(wrapped_getEV, hands): 
			if card_in_deck.logicalID == card_in_hand.logicalID:		print expectation_value, count
				ind_to_remove.append(ind)		"""
		ind += 1		ev_rounded = int(10 * expectation_value) / 10.
			if ev_rounded in cribbageDict.keys():
	ind_to_remove.sort() #guruntee in order			cribbageDict[ev_rounded] += 1 
	ind_to_remove.reverse() # reverse order		else:
	for ind in ind_to_remove:			cribbageDict[ev_rounded] = 1
		deck.CardList.pop(ind) # pop from back to front to not alter indexes		"""	
				count += 1
	# Create the five combinations of 4 cards 		
	fourCardCombos = itertools.combinations(self.CardList,4)	#print cribbageDict
	expectationList = []	p.close()
	for combo in fourCardCombos:	p.join()
		
		pointsDict = {}
		
		# Go through each possible hand, store value/multiplicity in a dict
		for drawCard in deck.CardList:
				
			possibleHand = Hand([combo[0],combo[1],combo[2],combo[3],drawCard])
			
			pointStr = possibleHand.countHand()
			
			if pointStr in pointsDict.keys():
				pointsDict[pointStr] += 1
			else:
				pointsDict[pointStr] = 1
		
		
		EV = 0
		for key, val in zip(pointsDict.keys(),pointsDict.values()):
			EV += val * float(key) / len(deck.CardList)
			
		expectationList.append(EV)
		
	return max(expectationList)			