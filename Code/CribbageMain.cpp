// CribbageMain.cpp

#include "Deck.h"
#include "Hand.h"
#include "Card.h"
#include "sharedConstants.h"
#include "suitsEnum.h"
#include "ComboGenerator.h"
#include <iostream>
#include <algorithm>
#include <string>
#include <map>
#include <chrono>
#include <new>

int main_old()
{
	
	auto start = std::chrono::system_clock::now();
	
	Deck deck;
	Hand hand;

	// a map mapping scores to multiplicities.
	std::map<int, int> cribbageDict;

	int N = 52;
	int K = 5;
	Card* cardList[5]; // Will be initialized in main loop
	int score;
	int count = 0;

	std::string bitmask(K, 1); // K leading 1's
	bitmask.resize(N, 0); // N-K trailing 0's

	// Combinatorics for counting all the hands
	do {
		int card_ind = 0;
		for (int i = 0; i < N; ++i) // [0..N-1] integers
		{
			// Using deck as a flyweight, make the cardList point to the 5 cards for this combo:
			if (bitmask[i]) {
				
				cardList[card_ind] = &deck.cardList[i];
				card_ind++;
			}
		}
		// Now assemble and count the hand.
		hand.dealHand(cardList[0], cardList[1], cardList[2], cardList[3], cardList[4]);
		for (int j = 0; j < 5; j++) {

			//hand.printHand();
			score = hand.countHand();
			// Store the score
			if (cribbageDict.count(score) > 0) { 
				cribbageDict[score] += 1; 
			} else {
				cribbageDict[score] = 1; 
			}
			// Rotate the common card
			hand.rotateHand();

		}

		count++;
		
		if(count % 10000 == 0) {
			for (auto& x : cribbageDict) {
				std::cout << x.first << '\t' << x.second << std::endl;
				
			}
			std::cout << count << std::endl;
			std::cout << std::endl;
		}
	} while (std::prev_permutation(bitmask.begin(), bitmask.end()));
 
	for (auto& x : cribbageDict) {
		std::cout << x.first << '\t' << x.second << std::endl; 
	}


	auto end = std::chrono::system_clock::now();
	std::chrono::duration<double> elapsed_seconds = end - start;

	std::cout << "elapsed time: " << elapsed_seconds.count() << "s\n";

	return 0;
}

void printArray(int a[], int r) {

	for (int i = 0; i < r; i++) {
		std::cout << a[i] << ' ';

	}
	std::cout << std::endl;

}

int comboTester() {

	int N = 5;
	int k = 4;
	ComboGenerator comboGen = ComboGenerator(N, k);
	Combo* combo = new Combo(k);


	for (int i = 0; i < 4; i++) {
		while (!comboGen.isFinished()) {

			combo = comboGen.getNextCombo();
			for (int i = 0; i < NUM_CARDS_IN_HAND; i++) {
				std::cout << combo->getIndex(i) << ' ';
			}
			std::cout << std::endl;
		}

		comboGen.restart();
		std::cout << std::endl;
	}

	// Clean up
	delete combo;

	return 0;

}


int main() {

	auto start = std::chrono::system_clock::now();

	Deck deck = Deck();
	Hand hand = Hand();

	// a map mapping scores to multiplicities.
	std::map<int, int> cribbageDict;

	Card* cardList[5];
	int score;
	int count = 0;

	ComboGenerator deckGen = ComboGenerator(NUM_CARDS_IN_DECK, NUM_CARDS_IN_HAND);
	Combo* index_combo = new Combo(NUM_CARDS_IN_HAND);

	while (!deckGen.isFinished()) {

		index_combo = deckGen.getNextCombo();
		for (int i = 0; i < 5; i++) {
			cardList[i] = &deck.cardList[index_combo->getIndex(i)];
		}

		hand.dealHand(cardList[0], cardList[1], cardList[2], cardList[3], cardList[4]);
		for (int i = 0; i < 5; i++) {

			//hand.printHand();
			score = hand.countHand();
			// Store the score
			if (cribbageDict.count(score) > 0) {
				cribbageDict[score] += 1;
			}
			else {
				cribbageDict[score] = 1;
			}
			// Rotate the common card
			hand.rotateHand();
			count++;
		}

		if (count > 10000) {
			break;
		}
	}
		
		


	for (auto& x : cribbageDict) {
		std::cout << x.first << '\t' << x.second << std::endl;
	}
	std::cout << count << std::endl;


	auto end = std::chrono::system_clock::now();
	std::chrono::duration<double> elapsed_seconds = end - start;

	std::cout << "elapsed time: " << elapsed_seconds.count() << "s\n";


	// Clean up
	delete index_combo;

	return 0;
}

