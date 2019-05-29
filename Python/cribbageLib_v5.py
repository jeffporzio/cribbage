import itertools
import numpy as np
from random import shuffle


class Card(object):

	#__slots__ = ['number','suit','value','logicalID']

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
		
		self.score = 0
		self.score_runs = 0 
		self.score_15s = 0
		self.score_pairs = 0
		self.score_flushes = 0
		self.score_rightJack = 0
	
	def rotateHand(self):
		temp = self.CardList.pop(0)
		self.CardList.append(temp)	
		
	def pointBreakDown(self):
		self.printHand()
		print 'Runs: ', self.score_runs
		print '15s: ', self.score_15s
		print 'Pairs: ', self.score_pairs
		print 'Flushes: ', self.score_flushes
		print 'RightJack: ', self.score_rightJack
		print
	
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
				self.score_pairs += 2
				
		# Right Jack
		for card in self.CardList[0:4]:
			if (card.number == JACK) and (card.suit == self.CardList[4].suit):
				points += 1
				self.score_rightJack += 1
		
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
			self.score_flushes += 4
			
		#####################
		# Five card points: #
		#####################
		# Add another point if the common card is the same suit as your flush		
		if isInHandFlush and (self.CardList[0].suit == self.CardList[4].suit):
			points += 1
			self.score_flushes += 1
		
		
		###########
		# All 15s #
		###########
		valueList = [card.value for card in self.CardList]	
		for n in range(2,6):
			
			combos = itertools.combinations(valueList,n)			
			# This is marginally faster
			for total in map(sum, combos):
				if total == 15:
					points += 2
					self.score_15s += 2

		#####################
		# Runs of all kinds #
		#####################
		runPoints = getRunPoints(self.CardList)
		points += runPoints
		self.score_runs += runPoints
		
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

	#print 'Hand: ', numberList
	
	highest_order_run = 0
	run_indexes = []
	
	# This array will contain the number of each card.number in the hand
	"""
	[1, 3, 4, 1, 2] = 
	[2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	In order to more efficiently find highest_order_run
	"""
	count_number_arr = [0]*13
	for number in numberList:
		count_number_arr[number-1] += 1
		
	temp = 1
	# Need to prime this if there are any Aces.
	if count_number_arr[0] > 0: 
		temp_indexes = [0]
	else: 
		temp_indexes = []
		
	was_last_nonzero = False
	for i in xrange(0,len(count_number_arr)):
		if count_number_arr[i] > 0 and was_last_nonzero:
			temp += 1
			temp_indexes.append(i)
		else: 
			# collect the temp before starting over from 1
			if temp <= 2:
				temp = 0 
			if temp > highest_order_run: 
				highest_order_run = temp
				run_indexes = temp_indexes
			# reset from 1 and reprime
			temp = 1
			temp_indexes = [i]
			
			if count_number_arr[i] > 0:
				was_last_nonzero = True
			else:
				was_last_nonzero = False
	else:
		if temp <= 2:
			temp = 0 
		if len(temp_indexes) < 3:
			temp_indexes = []
	
		if temp > highest_order_run: 
			highest_order_run = temp
			run_indexes = temp_indexes

	#print "run_indexes: ", run_indexes
	#print "highest_order_run: ", highest_order_run

	# Do we bother checking for double and triple runs?
	if highest_order_run == 0:
		#print 'No run!'
		return 0 # Exit if no runs
	if highest_order_run == 5: 
		#print 'Run of 5!'
		return 5 # Don't bother searching for multiple runs of 5

	# Calculate the number of points including double/triple/quad runs
	"""
	runPoints = reduce((lambda x, y: count_number_arr[x] * count_number_arr[y]),
							run_indexes) * highest_order_run
	"""
	runPoints = highest_order_run
	for ind in run_indexes:
		runPoints *= count_number_arr[ind]
						
	#print 'Run points in getRunPoints(): ', runPoints					
	return runPoints			
	
	
	
