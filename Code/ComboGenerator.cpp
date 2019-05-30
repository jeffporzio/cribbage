#include "ComboGenerator.h"
#include <algorithm>
#include <iostream>
#include <new>
#include <vector>

ComboGenerator::ComboGenerator(int N, int k) {

	this->N = N;
	this->k = k;

	for (int j = 0; j < k; j++) {
		current_combo.pushback(0);
		combo_to_return.pushback(0);
	}



	// initialize first combination
	for (int i = 0; i < k; i++) {
		current_combo[i] = i;
	}


	int i = k - 1;

	bool is_finished = false;

}

ComboGenerator :: ~ComboGenerator() {
	delete [] current_combo;
	delete [] combo_to_return;
}

bool ComboGenerator::isFinished() {
	return this->is_finished;
}

int* ComboGenerator :: getNextCombo() {

	// a[0] can only be n-r+1 exactly once - our termination condition!
	if (current_combo[0] < N - k + 1) {
		// If outer elements are saturated, keep decrementing i till you find unsaturated element
		while (i > 0 && current_combo[i] == N - k + i) {
			i--;
		}

		std::copy(current_combo.begin(), current_combo.end(),
			std::back_inserter(combo_to_return));

		current_combo[i]++;
		// Reset each outer element to prev element + 1
		while (i < k - 1) {
			current_combo[i + 1] = current_combo[i] + 1;
			i++;
		}
	} else {
		is_finished = true;
	}

	return combo_to_return;


}

void ComboGenerator::restart() {}

