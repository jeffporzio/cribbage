"""
As an attempt to get a more organic distribution this will 
not compute the expectation value, but be a Monte Carlo 
simulation where a 5th card is *actually* randomly chosen
from the deck. 
"""
import itertools
from cribbageLib_v4_withLookUp import * 
#from cribbageLib_v4 import * 
#import matplotlib
#import matplotlib.pyplot as plt
import time 
from timer_decorator import *
#from populateLookUp import populateLookUp
import random

@timer_this_func
def main():

	## MC Constants 
	n_iter = int(5e6)

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
	
	best_dict = {}
	worst_dict = {}
	random_dict = {}

	start = time.time()
	for i in xrange(0,n_iter):	
		
		deck.shuffle()
		card_list = deck.CardList[0:5]
		hand = Hand(card_list) # Take a list of card objects
		
		if (count % checkpoint_num) == 0 and count > 0:
			localtime = time.asctime( time.localtime(time.time()) )
			end = time.time()
			delta_t = end - start

			print '%i hands counted in %f secs. %f hands/sec' % (count, delta_t, checkpoint_num/delta_t)
			
			start = time.time()
		
		# Ask Hand for the "best", "worst" and a random selection of 4 cards.
		(best_cards, worst_cards, random_cards) = hand.chooseHands(look_up_dict)
		best_cards.append(deck.CardList[5])
		worst_cards.append(deck.CardList[5])
		random_cards.append(deck.CardList[5])
		
		# Construct hand instance for each choice
		best_hand = Hand(best_cards)
		worst_hand = Hand(worst_cards)
		random_hand = Hand(random_cards)
		
		# Get the scores
		best_score = look_up_dict[best_hand.hash_string]
		worst_score = look_up_dict[worst_hand.hash_string]
		random_score = look_up_dict[random_hand.hash_string]
		
		# Add scores to dicts
		if best_score in best_dict.keys():
			best_dict[best_score] += 1 
		else:
			best_dict[best_score] = 1

		if worst_score in worst_dict.keys():
			worst_dict[worst_score] += 1 
		else:
			worst_dict[worst_score] = 1
		
		if random_score in random_dict.keys():
			random_dict[random_score] += 1 
		else:
			random_dict[random_score] = 1
			
		count += 1

	# Save them all when done.
	save_file = "..\Data\MonteCarlo_out"+str(n_iter)+"_best.txt"
	with open(save_file, 'w') as f: 
		for key in best_dict:
			f.write(str(key) + ',' + str(best_dict[key])+'\n')

	save_file = "..\Data\MonteCarlo_out"+str(n_iter)+"_worst.txt"
	with open(save_file, 'w') as f: 
		for key in worst_dict:
			f.write(str(key) + ',' + str(worst_dict[key])+'\n')
			
	save_file = "..\Data\MonteCarlo_out"+str(n_iter)+"_random.txt"
	with open(save_file, 'w') as f: 
		for key in random_dict:
			f.write(str(key) + ',' + str(random_dict[key])+'\n')

	
	
main()