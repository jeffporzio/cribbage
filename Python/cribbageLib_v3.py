import itertools
import numpy as np
from random import shuffle


class Card(object):

	def __init__(self,number,suit):
		# Cards are going to need a suit, number, and counting value
		self.number = number
		self.suit = suit
		# Deal with face cards
		if number >= 10:
			self.value = 10
		else:
			self.value = number
		
		if suit == "Diamonds":
			suit_offset = 0
		elif suit == "Hearts":
			suit_offset = 1
		elif suit == "Clubs":
			suit_offset = 2
		elif suit == "Spades":
			suit_offset = 3
		
		self.logicalID = number + 13*suit_offset
			
	def printCard(self):		
		print self.number, self.suit,

		

class Hand(object):

	def __init__(self,cards):
		# Hand has 4 cards and the card from the cut, will deal with the common card in the counting algorithm. 
		"""
		self.card1 = card1
		self.card2 = card2
		self.card3 = card3
		self.card4 = card4
		self.card5 = card5	
		"""
		self.CardList = cards
	
	#@profile
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
			
			for total in map(sum, combos):
				if total == 15:
					points += 2

		#####################
		# Runs of all kinds #
		#####################
		points += getRunPoints(self.CardList)
	
	
		return str(points)
		
		
	def printHand(self):
		for card in self.CardList:			
			card.printCard()
			print '\t',
		print
			
	def getExpectationValue(self):
		
		# Create a deck to iterate through 
		deck = Deck()
		# Remove the five cards in this hand from the deck		
		ind_to_remove = []
		ind = 0
		for card_in_deck in deck.CardList:
			for card_in_hand in self.CardList:
				if card_in_deck.logicalID == card_in_hand.logicalID:
					ind_to_remove.append(ind)
			ind += 1
		
		ind_to_remove.sort() #guruntee in order
		ind_to_remove.reverse() # reverse order
		for ind in ind_to_remove:
			deck.CardList.pop(ind) # pop from back to front to not alter indexes
			
		# Create the five combinations of 4 cards 
		fourCardCombos = itertools.combinations(self.CardList,4)
		expectationList = []
		for combo in fourCardCombos:
			
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
		
		
		
class Deck(object): 

	def __init__(self):
		self.CardList = []
		suits = ['Diamonds','Hearts','Clubs','Spades']	
		for suit in suits:
			for number in range(1,14):
				card = Card(number,suit)
				self.CardList.append(card)
				
	def shuffle(self):
		shuffle(self.CardList)
		
	def printLogicalIDs(self):
		for card in self.CardList:
			print card.logicalID

def getRunPoints(cardList):

	runPoints = 0

	numberList = [o.number for o in cardList]
	numberList.sort()
	### This is messy but I think it works...
	# Figure out what the highest length run is and use it to catch occurrences of smaller runs within 
	# bigger runs.  It shouldn't be possible for there to be a run of 3 in a hand where there is also a
	# run of 4, say. But I DO want to allow for double runs, which is why I need to do the combinations 
	# a second time, but only looking for runs of length HIGHEST_ORDER_RUN
	
	HIGHEST_ORDER_RUN = 0
	
	for i in range(0,len(numberList)-2): # No need to check the last two cards because no runs of 2
		num = numberList[i]
		temp = 1
		if num+1 in numberList:
			temp += 1
		else: 
			break # If it isn't, don't bother looking further 
		
		if num+2 in numberList:
			temp += 1
		else: 
			break
			
		if num+3 in numberList:
			temp += 1	
		else: 
			break
		
		if num+4 in numberList: 
			temp += 1	
		else: 
			break
		
		if temp <= 2: 
			temp = 0
		
		#print 'temp: ', temp
		if temp > HIGHEST_ORDER_RUN:
			HIGHEST_ORDER_RUN = temp
		""" 
		At some point replace this with a for loop... 
		for num in numberList:
			for ind in range(1,5):
				if num+ind in numberList:
					temp += 1
			...
		"""			
	if HIGHEST_ORDER_RUN == 0:
		# print 'No run!'
		return 0 # Exit if no runs
	if HIGHEST_ORDER_RUN == 5: 
		return 5 # Don't bother searching for double runs of 5
			
	hORC = itertools.combinations(numberList,HIGHEST_ORDER_RUN) #highestOrderRunCombos = hORC
	for combo in hORC:
		for num in combo:
			temp = 1
			if num+1 in numberList:
				temp += 1
			if num+2 in numberList:
				temp += 1
			if num+3 in numberList:
				temp += 1	
			if num+4 in numberList: 
				temp += 1	
			if temp <= 2: 
				temp = 0
			
			print 'temp: ', temp
			if temp == HIGHEST_ORDER_RUN:
				runPoints += HIGHEST_ORDER_RUN
					
			""" 
			At some point replace this with a for loop... 
			for num in numberList:
				for ind in range(1,5):
					if num+ind in numberList:
						temp += 1
				...
			"""		
	print 'Run points in getRunPoints(): ', runPoints					
	return runPoints			
	
	
	
