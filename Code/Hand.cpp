// Hand.cpp

#include <iostream>
#include "Hand.h"
#include "sharedConstants.h"
#include "Card.h" // included here for Card dependency 
#include <algorithm>
#include <array>
#include <vector>

// Passing pointers is cheaper and easier (especially when we implement design patterns later)


Hand :: Hand()
{
	Card *cardList[5];
}

void Hand :: dealHand(Card *card0
			,Card *card1 
			,Card *card2
			,Card *card3
			,Card *card4) 
{
	cardList[0] = card0;
	cardList[1] = card1;
	cardList[2] = card2;
	cardList[3] = card3;
	cardList[4] = card4;
}

void Hand :: printHand()
{
	int i;
	for(i = 0; i < NUM_CARDS_IN_HAND; i++){
		cardList[i]->printCard();
	}
	std::cout << "\n";
}

void Hand::rotateHand()
{
	std::rotate(cardList.begin(), cardList.begin() + 1, cardList.end());
}

int Hand::countHand()
{
	/*
		Should return a point value for this hand (where to common card is the 4th index).

		Ways to get points by card number involved :
		2	Pairs, 15s, Right Jack
		3	Three of a kind*, runs, 15s
		4	Four of a kind*, runs, 15s, flush(in hand)
		5	Runs, flush(all cards), 15s
		* **TooK and FooK are just combinations of pairs, so no need to look for them explicitly.
		15s can be made of any number of cards, so need to check those each time.
		-- Runs need to be checked separately.
	*/
	int score = 0; 
	int score_15s = 0;
	int score_pairs = 0;
	int score_flush = 0;
	int score_runs = 0;
	int score_rightjack = 0;

	bool isInHandFlush = false;

	//*****************************************
	// Two card Combos: 5 choose 2
	Card* two_card_combo[2];
	//Card* two_card_combo = new Card[2]; // I don't understand why this doesn't work.

	std::string bitmask_2(2, 1); // K leading 1's
	bitmask_2.resize(NUM_CARDS_IN_HAND, 0); // N-K trailing 0's
	do {
		int card_ind = 0;
		for (int i = 0; i < NUM_CARDS_IN_HAND; ++i){
			if (bitmask_2[i]) {
				two_card_combo[card_ind] = cardList[i];
				card_ind++;
			}
		}

		// Pairs, Three/Four of a kind:
		if(two_card_combo[0]->number == two_card_combo[1]->number) { score_pairs += 2; }
		// Right Jack
		if (two_card_combo[0]->number == JACK && two_card_combo[0]->suit == two_card_combo[1]->suit) { score_rightjack += 1; }
		// 15s of 2
		if (two_card_combo[0]->value + two_card_combo[1]->value == 15) { score_15s += 2;}

	} while (std::prev_permutation(bitmask_2.begin(), bitmask_2.end()));

	//*****************************************
	// Three card Combos: 5 choose 3
	Card* three_card_combo[3];

	std::string bitmask_3(3, 1); // K leading 1's
	bitmask_3.resize(NUM_CARDS_IN_HAND, 0); // N-K trailing 0's
	do {
		int card_ind = 0;
		for (int i = 0; i < NUM_CARDS_IN_HAND; ++i){
			if (bitmask_3[i]) {
				three_card_combo[card_ind] = cardList[i];
				card_ind++;
			}
		}

		// 15s of 3
		if (three_card_combo[0]->value + three_card_combo[1]->value + three_card_combo[2]->value == 15) { score_15s += 2; }

	} while (std::prev_permutation(bitmask_3.begin(), bitmask_3.end()));

	//*****************************************
	// Four card Combos: 5 choose 4
	Card* four_card_combo[4];

	std::string bitmask_4(4, 1); // K leading 1's
	bitmask_4.resize(NUM_CARDS_IN_HAND, 0); // N-K trailing 0's
	do {
		int card_ind = 0;
		for (int i = 0; i < NUM_CARDS_IN_HAND; ++i){
			if (bitmask_4[i]) {
				four_card_combo[card_ind] = cardList[i];
				card_ind++;
			}
		}

		// 15s of 4
		if (four_card_combo[0]->value + four_card_combo[1]->value + four_card_combo[2]->value + four_card_combo[3]->value == 15) { score_15s += 2; }

	} while (std::prev_permutation(bitmask_4.begin(), bitmask_4.end()));

	// 15s of 5
	if(cardList[0]->value +
		cardList[1]->value + 
		cardList[2]->value + 
		cardList[3]->value + 
		cardList[4]->value == 15) {
		score_15s += 2;
	}


	// In-Hand Flush
	if (cardList[0]->suit == cardList[1]->suit &&
		cardList[0]->suit == cardList[2]->suit &&
		cardList[0]->suit == cardList[3]->suit)
	{
		score_flush += 4;
		isInHandFlush = true;
	}
	// Check for full Flush: 
	if (isInHandFlush && cardList[0]->suit == cardList[4]->suit) { score_flush += 1; }

	score_runs = this->getRunPoints();





	score = score_15s + score_flush + score_pairs + score_rightjack + score_runs;
	/*
	this->printHand();
	std::cout << "15s: " << score_15s << std::endl;
	std::cout << "Flush: " << score_flush << std::endl;
	std::cout << "Pairs: " << score_pairs << std::endl;
	std::cout << "Right Jack: " << score_rightjack << std::endl;
	std::cout << "Runs: " << score_runs << std::endl;
	*/
	return score;
}


int Hand::getRunPoints() 
{
	std::array<int,NUM_CARDS_IN_HAND> number_list;
	for (int i = 0; i < NUM_CARDS_IN_HAND; i++) {
		number_list[i] = cardList[i]->number;
	}
	
	int run_points = 0;
	int temp = 0; 
	int highest_order_run = 0;
	int num;
	std::sort(number_list.begin(), number_list.end());

	for (int i = 0; i < NUM_CARDS_IN_HAND - 2; i++) {
		num = number_list[i];
		if (std::find(std::begin(number_list), std::end(number_list), num + 1) != std::end(number_list)){
			temp += 1;
		} else {
			break;
		}
		if (std::find(std::begin(number_list), std::end(number_list), num + 2) != std::end(number_list)) {
			temp += 1;
		}
		else {
			break;
		}		
		if (std::find(std::begin(number_list), std::end(number_list), num + 3) != std::end(number_list)) {
			temp += 1;
		}
		else {
			break;
		}
		if (std::find(std::begin(number_list), std::end(number_list), num + 4) != std::end(number_list)) {
			temp += 1;
		}
		else {
			break;
		}

		if (temp <= 2) { temp = 0; }

		if (temp > highest_order_run) { highest_order_run = temp; }

		// Do we bother checkng for double and triple runs? 
		if (highest_order_run == 0) { return 0; }
		if (highest_order_run == 5) { return 5; }

		// Get the correct number of highest_order_run's 
		std::vector<int> combo;
		for (int i = 0; i < highest_order_run; i++) {
			combo.push_back(0);	
		}

		// THIS ISN'T RIGHT YET
		std::string bitmask_2(2, 1); // K leading 1's
		bitmask_2.resize(NUM_CARDS_IN_HAND, 0); // N-K trailing 0's
		do {
			int card_ind = 0;
			for (int i = 0; i < NUM_CARDS_IN_HAND; ++i) {
				if (bitmask_2[i]) {
					two_card_combo[card_ind] = cardList[i];
					card_ind++;
				}
			}

			// Pairs, Three/Four of a kind:
			if (two_card_combo[0]->number == two_card_combo[1]->number) { score_pairs += 2; }
			// Right Jack
			if (two_card_combo[0]->number == JACK && two_card_combo[0]->suit == two_card_combo[1]->suit) { score_rightjack += 1; }
			// 15s of 2
			if (two_card_combo[0]->value + two_card_combo[1]->value == 15) { score_15s += 2; }

		} while (std::prev_permutation(bitmask_2.begin(), bitmask_2.end()));


	}

	return run_points;
}





double Hand::getExpectationValue() 
{
	return 0;
}