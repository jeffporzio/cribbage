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
		print( self.number, self.suit)
		
	#def __eq__(self, other):
	#	return self.logicalID == other.logicalID

		

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
		self.hash_string = ""
		self.updateHashString()
	
	def rotateHand(self):
		temp = self.CardList.pop(0)
		self.CardList.append(temp)
		self.updateHashString()
		
	def updateHashString(self):
		
		self.hash_string = ""
		for card in self.CardList:
			number = card.number
			suit = card.suit
			if number < 10:
				card_number = str(number)
			elif number == 10:
				card_number = 'T'
			elif number == 11:
				card_number = 'J'
			elif number == 12:
				card_number = 'Q'
			elif number == 13:
				card_number = 'K'
				
			if suit == "Diamonds":
				card_suit = "D"
			elif suit == "Hearts":
				card_suit = "H"
			elif suit == "Clubs":
				card_suit = "C"
			elif suit == "Spades":
				card_suit = "S"
				
			self.hash_string += card_number + card_suit

			
				
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
			
			# This is marginally faster than the other commented versions
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
			print( '\t',)
		print()
			
	def getExpectationValue(self):
		
		# Create a deck to iterate through 
		deck = Deck()
		# Remove the five cards in this hand from the deck		
		
		for card_in_hand in self.CardList:
			deck.removeCardbyLogicalID(card_in_hand.logicalID)
			
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
	
	"""
	# These didnt work and I don't know why.
	def __eq__(self, other):
		return ( self.CardList[0].logicalID == other.CardList[0].logicalID and
			     self.CardList[1].logicalID == other.CardList[1].logicalID and		
			     self.CardList[2].logicalID == other.CardList[2].logicalID and		
			     self.CardList[3].logicalID == other.CardList[3].logicalID and		
			     self.CardList[4].logicalID == other.CardList[4].logicalID )	
				
		
	def __hash__(self):
		# This can be tought of as a 5 digit base 52 number.
		hash = 0
		for i, card in enumerate(self.CardList):
			hash += card.logicalID * 52**i # 
			
		return hash
	"""
	"""
		return hash(
					(self.CardList[0].number, self.CardList[0].suit,
					 self.CardList[1].number, self.CardList[1].suit,
					 self.CardList[2].number, self.CardList[2].suit,
					 self.CardList[3].number, self.CardList[3].suit,
					 self.CardList[4].number, self.CardList[4].suit,
					)
				   )	
	"""
		
		
		
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
			print( card.logicalID)
			
	def printDeck(self):
		for card in self.CardList:
			card.printCard()
		print()
		
	def removeCardbyLogicalID(self, ID):
		# Breaking this out so only one card can be removed at a time fixes index issues when the array changes length.
		for i, card in enumerate(self.CardList):
			if card.logicalID == ID: 
				self.CardList.pop(i)
				

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
	
	#print "Hand: ", numberList
	for i in range(0,len(numberList)-2): # No need to check the last two cards because no runs of 2
		num = numberList[i]
		temp = 1
		if num+1 in numberList:
			temp += 1
		else: 
			continue # If it isn't, don't bother looking further 
		
		if num+2 in numberList:
			temp += 1
		else: 
			continue
			
		if num+3 in numberList:
			temp += 1	
		else: 
			if temp <= 2:
				temo = 0
			if temp > HIGHEST_ORDER_RUN:
				HIGHEST_ORDER_RUN = temp
			continue
		
		if num+4 in numberList: 
			temp += 1
		else: 
			if temp <= 2:
				temp = 0
			if temp > HIGHEST_ORDER_RUN:
				HIGHEST_ORDER_RUN = temp
			continue
			
			if temp <= 2:
				temp = 0
			#print 'temp: ', temp
		if temp > HIGHEST_ORDER_RUN:
			HIGHEST_ORDER_RUN = temp
		
		# Terminate loop if it's a run of 5.
		if HIGHEST_ORDER_RUN == 5: 
			break


	#print 'highest_order_run: ', HIGHEST_ORDER_RUN
	# Do we bother checking for double and triple runs?
	if HIGHEST_ORDER_RUN == 0:
		#print 'No run!'
		return 0 # Exit if no runs
	if HIGHEST_ORDER_RUN == 5: 
		#print 'Run of 5!'
		return 5 # Don't bother searching for multiple runs of 5
		
		
	
	# Now allow for double, triple runs
	hORC = itertools.combinations(numberList,HIGHEST_ORDER_RUN) #highestOrderRunCombos = hORC
	for combo in hORC:
		for num in combo:
			temp = 1
			# First two just kill it if we fail the check
			if num+1 in combo:
				temp += 1
			else:
				continue
			# First two just kill it if we fail the check	
			if num+2 in combo:
				temp += 1
			else: 
				continue
			
			# From here on we could have a run even if this fails
			if num+3 in combo:
				temp += 1
			else:
				if temp <= 2:
					temp = 0		
				#print 'temp: ', temp
				if temp == HIGHEST_ORDER_RUN:
					runPoints += HIGHEST_ORDER_RUN
				continue
				
			if num+4 in combo: 
				temp += 1
			else:
				if temp <= 2:
					temp = 0						
				#print 'temp: ', temp
				if temp == HIGHEST_ORDER_RUN:
					runPoints += HIGHEST_ORDER_RUN
				continue
			
			# If we make it all the way through, this is a run of 5
			# Which we already checked for earlier. 
			
		#print combo			
	#print 'Run points in getRunPoints(): ', runPoints, '\n'					
	return runPoints			
	
	
	
