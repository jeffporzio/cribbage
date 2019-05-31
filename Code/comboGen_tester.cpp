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


int comboGen_tester() {

	int N = 5;
	int k = 4;
	ComboGenerator comboGen = ComboGenerator(N, k);
	std::vector<int> combo;


	for (int i = 0; i < 4; i++) {
		while (!comboGen.isFinished()) {

			combo = comboGen.getNextCombo();
			for (auto val : combo) {
				std::cout << val << ' ';
			}
			std::cout << std::endl;
		}

		comboGen.restart();
		std::cout << " \n \r " << std::endl;
	}

	return 0;
}