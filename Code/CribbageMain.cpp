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
	Card* cardList[5];
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
				
				card_ind++; cardList[card_ind] = &deck.cardList[i];
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

int main_good() {

	auto start = std::chrono::system_clock::now();

	Deck deck;
	Hand hand;

	// a map mapping scores to multiplicities.
	std::map<int, int> cribbageDict;

	Card* cardList[5];
	int score;
	int count = 0;


	int k = 5;
	int N = 52;

	int* index_combos = new int[k];
	// initialize first combination
	for (int i = 0; i < k; i++) {
		index_combos[i] = i;
	}
	int i = k - 1; // Index to keep track of maximum unsaturated element in array
	// a[0] can only be n-r+1 exactly once - our termination condition!
	while (index_combos[0] < N - k + 1) {
		// If outer elements are saturated, keep decrementing i till you find unsaturated element
		while (i > 0 && index_combos[i] == N - k + i) {
			i--;
		}
		
		
		/*************************************************************************************************/
		// Main code goes here
		
		for (int j{}; j < 5; j++) {
			cardList[j] = &deck.cardList[index_combos[j]];
		}
		hand.dealHand(cardList[0], cardList[1], cardList[2], cardList[3], cardList[4]);
		for (int p = 0; p < 5; p++) {

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

		
		
		if (count % 100000 == 0) {
			for (auto& x : cribbageDict) {
				std::cout << x.first << '\t' << x.second << std::endl;

			}
			std::cout << count << std::endl;
			std::cout << std::endl;
		}
		

		/*************************************************************************************************/
		index_combos[i]++;
		// Reset each outer element to prev element + 1
		while (i < k - 1) {
			index_combos[i + 1] = index_combos[i] + 1;
			i++;
		}
	}

	for (auto& x : cribbageDict) {
		std::cout << x.first << '\t' << x.second << std::endl;
	}
	std::cout << count << std::endl;


	auto end = std::chrono::system_clock::now();
	std::chrono::duration<double> elapsed_seconds = end - start;

	std::cout << "elapsed time: " << elapsed_seconds.count() << "s\n";


	delete [] index_combos;

	return 0;
}


int main() {

	int N = 5; 
	int k = 4;
	ComboGenerator comboGen = ComboGenerator(N,k);
	std::vector<int> combo; 

	while (!comboGen.isFinished()) {
	
		combo = comboGen.getNextCombo();
		for (auto val : combo) {
			std::cout << val << ' ';
		}
		std::cout << std::endl;
	}



	return 0;
}