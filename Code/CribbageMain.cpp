// CribbageMain.cpp

#include "Deck.h"
#include "Hand.h"
#include "Card.h"
#include "sharedConstants.h"
#include "suitsEnum.h"
#include <iostream>
#include <algorithm>
#include <string>
#include <map>

int main()
{
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

	return 0;
}