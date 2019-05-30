// Hand.cpp

#include <iostream>
#include "Hand.h"
#include "sharedConstants.h"
#include "Card.h" // included here for Card dependency 
#include <algorithm>
#include <array>
#include <vector>

// Passing pointers is cheaper and easier (especially when we implement design patterns later)


Hand::Hand()
{
	Card* cardList[5];
}

void Hand::dealHand(Card* card0
	, Card* card1
	, Card* card2
	, Card* card3
	, Card* card4)
{
	cardList[0] = card0;
	cardList[1] = card1;
	cardList[2] = card2;
	cardList[3] = card3;
	cardList[4] = card4;
}

void Hand::printHand()
{
	int i;
	for (i = 0; i < NUM_CARDS_IN_HAND; i++) {
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

	int N;
	int k;
	int i;

	bool isInHandFlush = false;

	//*****************************************
	// Two card Combos: 5 choose 2
	k = 2;
	N = NUM_CARDS_IN_HAND;

	int* two_card_combo = new int[k];
	// initialize first combination
	for (int i = 0; i < k; i++) {
		two_card_combo[i] = i;
	}
	i = k - 1; // Index to keep track of maximum unsaturated element in array
	// a[0] can only be n-r+1 exactly once - our termination condition!
	while (two_card_combo[0] < N - k + 1) {
		// If outer elements are saturated, keep decrementing i till you find unsaturated element
		while (i > 0 && two_card_combo[i] == N - k + i) {
			i--;
		}
		/*************************************************************************************************/
		// Pairs, Three/Four of a kind:
		if (cardList[two_card_combo[0]]->number == cardList[two_card_combo[1]]->number) { score_pairs += 2; }
		// 15s of 2
		if (cardList[two_card_combo[0]]->value + cardList[two_card_combo[1]]->value == 15) { score_15s += 2; }
		/*************************************************************************************************/
		two_card_combo[i]++;
		// Reset each outer element to prev element + 1
		while (i < k - 1) {
			two_card_combo[i + 1] = two_card_combo[i] + 1;
			i++;
		}
	}

	//*****************************************
	// Three card Combos: 5 choose 3
	k = 3;
	N = NUM_CARDS_IN_HAND;

	int* three_card_combo = new int[k];
	// initialize first combination
	for (int i = 0; i < k; i++) {
		three_card_combo[i] = i;
	}
	i = k - 1; // Index to keep track of maximum unsaturated element in array
	// a[0] can only be n-r+1 exactly once - our termination condition!
	while (three_card_combo[0] < N - k + 1) {
		// If outer elements are saturated, keep decrementing i till you find unsaturated element
		while (i > 0 && three_card_combo[i] == N - k + i) {
			i--;
		}
		/*************************************************************************************************/
		// 15s of 3
		if (cardList[three_card_combo[0]]->value + cardList[three_card_combo[1]]->value +
			cardList[three_card_combo[2]]->value == 15) { score_15s += 2; }
		/*************************************************************************************************/
		three_card_combo[i]++;
		// Reset each outer element to prev element + 1
		while (i < k - 1) {
			three_card_combo[i + 1] = three_card_combo[i] + 1;
			i++;
		}
	}

	//*****************************************
	// Four card Combos: 5 choose 4
	k = 4;
	N = NUM_CARDS_IN_HAND;

	int* four_card_combo = new int[k];
	// initialize first combination
	for (int i = 0; i < k; i++) {
		four_card_combo[i] = i;
	}
	i = k - 1; // Index to keep track of maximum unsaturated element in array
	// a[0] can only be n-r+1 exactly once - our termination condition!
	while (four_card_combo[0] < N - k + 1) {
		// If outer elements are saturated, keep decrementing i till you find unsaturated element
		while (i > 0 && four_card_combo[i] == N - k + i) {
			i--;
		}
		/*************************************************************************************************/
		// 15s of 4
		if (cardList[four_card_combo[0]]->value + cardList[four_card_combo[1]]->value + 
			cardList[four_card_combo[2]]->value + cardList[four_card_combo[3]]->value == 15) { score_15s += 2; }
		/*************************************************************************************************/
		four_card_combo[i]++;
		// Reset each outer element to prev element + 1
		while (i < k - 1) {
			four_card_combo[i + 1] = four_card_combo[i] + 1;
			i++;
		}
	}
	// 15s of 5
	if (cardList[0]->value +
		cardList[1]->value +
		cardList[2]->value +
		cardList[3]->value +
		cardList[4]->value == 15) {
		score_15s += 2;
	}

	// Right Jack
	for (int i = 0; i < 4; i++) {
		if ((cardList[i]->number == JACK) && (cardList[i]->suit == cardList[4]->suit)) { 
			score_rightjack += 1;
			break; // Can't be more than one.
		}
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

	// Runs:
	score_runs = this->getRunPoints_new();


	score = score_15s + score_flush + score_pairs + score_rightjack + score_runs;


	delete [] two_card_combo;
	delete [] three_card_combo;
	delete [] four_card_combo;

	return score;
}


int Hand::getRunPoints()
{
	std::array<int, NUM_CARDS_IN_HAND> number_list;
	for (int i = 0; i < NUM_CARDS_IN_HAND; i++) {
		number_list[i] = cardList[i]->number;
	}

	int run_points = 0;
	int temp = 0;
	int highest_order_run = 0;
	int num;
	std::sort(number_list.begin(), number_list.end()); // Sort lets use ignore the two highest cards in the following loop.

	for (int i = 0; i < NUM_CARDS_IN_HAND - 2; i++) {
		num = number_list[i];
		temp = 1;
		// First two just kill it if we fail the check
		if (std::find(std::begin(number_list), std::end(number_list), num + 1) != std::end(number_list)) {
			temp += 1;
		}
		else {
			continue;
		}
		// First two just kill it if we fail the check
		if (std::find(std::begin(number_list), std::end(number_list), num + 2) != std::end(number_list)) {
			temp += 1;
		}
		else {
			continue;
		}
		// Now we could still have a run even if this fails
		if (std::find(std::begin(number_list), std::end(number_list), num + 3) != std::end(number_list)) {
			temp += 1;
		}
		else {
			if (temp <= 2) { temp = 0; }
			if (temp > highest_order_run) { highest_order_run = temp; }
			continue;
		}

		if (std::find(std::begin(number_list), std::end(number_list), num + 4) != std::end(number_list)) {
			temp += 1;
		}
		else {
			if (temp <= 2) { temp = 0; }
			if (temp > highest_order_run) { highest_order_run = temp; }
			continue;
		}

		if (temp > highest_order_run) { highest_order_run = temp; }
		if (highest_order_run == 5) { break; } // No need to keep going

	}

	if (highest_order_run < 2) { highest_order_run = 0; }
	// Do we bother checkng for double and triple runs? 
	if (highest_order_run == 0) { return 0; }
	if (highest_order_run == 5) { return 5; }

	// Get the correct number of highest_order_run's 
	

	int k = highest_order_run;
	int N = NUM_CARDS_IN_HAND;
	// initialize first combination
	std::vector<int> combo = std::vector<int>(highest_order_run);
	for (int i = 0; i < k; i++) {
		combo[i] = i;
	}
	int i = k - 1; // Index to keep track of maximum unsaturated element in array
	// a[0] can only be n-r+1 exactly once - our termination condition!
	while (combo[0] < N - k + 1) {
		// If outer elements are saturated, keep decrementing i till you find unsaturated element
		while (i > 0 && combo[i] == N - k + i) {
			i--;
		}
		/*************************************************************************************************/
		for (int j = 0; j < highest_order_run; j++) {
			// Similar logic here
			temp = 1;
			num = combo[j];

			if (std::find(std::begin(combo), std::end(combo), num + 1) != std::end(combo)) {
				temp += 1;
			}
			else {
				continue;
			}

			if (std::find(std::begin(combo), std::end(combo), num + 2) != std::end(combo)) {
				temp += 1;
			}
			else {
				continue;
			}

			if (std::find(std::begin(combo), std::end(combo), num + 3) != std::end(combo)) {
				temp += 1;
			}
			else {
				if (temp < 2) { temp = 0; }
				if (temp == highest_order_run) { run_points += highest_order_run; }
				continue;
			}

			if (std::find(std::begin(combo), std::end(combo), num + 4) != std::end(combo)) {
				temp += 1;
			}
			else {
				if (temp < 2) { temp = 0; }
				if (temp == highest_order_run) { run_points += highest_order_run; }
				continue;
			}
		}
			// If we make it this far it's a run of 5, which has already been caught.

		/*************************************************************************************************/
		combo[i]++;
		// Reset each outer element to prev element + 1
		while (i < k - 1) {
			combo[i + 1] = combo[i] + 1;
			i++;
		}
	}

	return run_points;
}


int Hand::getRunPoints_new() {

	std::array<int, NUM_CARDS_IN_HAND> number_list = { 0 };
	for (int i = 0; i < NUM_CARDS_IN_HAND; i++) {
		number_list[i] = cardList[i]->number;
	}

	int run_points = 0;
	int highest_order_run = 0;
	std::vector<int> run_indexes;

	// This array will contain the number of each card.number in the hand.
	std::array<int, 13> count_number_arr = { 0 };

	for (auto number : number_list) {
		count_number_arr[number-1] += 1;
	}

	std::vector<int> temp_indexes; 
	// Prime this if there are any Aces
	if (count_number_arr[0] > 0) { temp_indexes.push_back(0); }
	int temp = 1;
	bool was_last_nonzero = false; 
	for (int i = 0; i < count_number_arr.size(); i++) {
	
		if (count_number_arr[i] > 0 && was_last_nonzero) {
			temp += 1;
			temp_indexes.push_back(i);		
		} else {
			// Collect the temp before starting over from 1
			if (temp <= 2) { temp = 0; }
			if (temp > highest_order_run) {
				highest_order_run = temp; 
				run_indexes.swap(temp_indexes);
				
			}
			temp = 1; 
			temp_indexes.clear();
			temp_indexes.push_back(i);

			if (count_number_arr[i] > 0) {
				was_last_nonzero = true;
			} else {
				was_last_nonzero = false;
			}
		} // endelse
	

	} //endfor
	if (temp <= 2) { temp = 0; }
	if (temp_indexes.size() < 3) { temp_indexes.clear(); }
	
	if (temp > highest_order_run) {
		highest_order_run = temp;
		run_indexes = temp_indexes;
	}

	   	  
	if (highest_order_run < 2) { highest_order_run = 0; }
	// Do we bother checkng for double and triple runs? 
	if (highest_order_run == 0) { return 0; }
	if (highest_order_run == 5) { return 5; }

	// Calculate the number of points including doub/trip/quad runs.
	run_points = highest_order_run;
	for (auto ind : run_indexes) {
		run_points *= count_number_arr[ind];
	}

	/*
	this->printHand();
	std::cout << "Run points: " << run_points << std::endl;
	*/

	return run_points;
}


double Hand::getExpectationValue()
{
	return 0;
}