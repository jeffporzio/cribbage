#include "ComboGenerator.h"
#include <algorithm>
#include <iostream>
#include <new>
#include <vector>

/*
https://dev.to/rrampage/algorithms-generating-combinations-100daysofcode-4o0a
*/

ComboGenerator::ComboGenerator(int N, int k) {

	this->N = N;
	this->k = k;

	for (int i = 0; i < k; i++) {
		current_combo.push_back(0);
		combo_to_return.push_back(0);
	}

	// initialize first combination
	for (int i = 0; i < k; i++) {
		current_combo[i] = i;
	}

	this->max_unsat = k - 1;

	this->is_finished = false;

}

ComboGenerator :: ~ComboGenerator() {

}

bool ComboGenerator::isFinished() {
	return this->is_finished;
}

std::vector<int> ComboGenerator :: getNextCombo() {

	// a[0] can only be n-r+1 exactly once - our termination condition!
	// However, we lag behind one, so need to terminate one early.
	if (current_combo[0] < N - k + 1) {
		// If outer elements are saturated, keep decrementing i till you find unsaturated element
		while (max_unsat > 0 && current_combo[max_unsat] == N - k + max_unsat) {
			max_unsat--;
		}

		std::copy(current_combo.begin(), current_combo.end(), combo_to_return.begin());
		/*
		This is really slow. Going to make a combo class that is just 5 ints with functions to copy, etc 
		Then use memcopy to just swap instances around, which will be the lowest level operation we can do. 
		*/


		current_combo[max_unsat]++;
		// Reset each outer element to prev element + 1
		while (max_unsat < k - 1) {
			current_combo[max_unsat + 1] = current_combo[max_unsat] + 1;
			max_unsat++;
		}
	} 
	
	// Check again to see if next iteration will be good.
	if (current_combo[0] < N - k + 1) {
		is_finished = false;
	} else {
		is_finished = true;

	}

	return combo_to_return;


}

void ComboGenerator::restart() {


	// initialize first combination
	for (int i = 0; i < k; i++) {
		current_combo[i] = i;
	}

	max_unsat = k - 1;

	is_finished = false;

}

