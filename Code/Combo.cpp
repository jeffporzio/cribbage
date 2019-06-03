
#include "Combo.h"
#include <iostream>
#include "sharedConstants.h"


Combo::Combo(int size) {
	this->size = size; // These will all be the same size. It is up to the user not to read -1's.
	
	std::cout << "From inside Combo::Combo(): " << std::endl;
	for (auto& val : indeces) {
		std::cout << val << " " << std::endl;
	}
}

Combo::~Combo() {}

int Combo::getIndex(unsigned i) {
	return indeces[i];
}

void Combo::setIndex(unsigned i, int val) {
	indeces[i] = val;
}

void Combo::clear() {
	for (int i = 0; i < size; i++) {
		indeces[i] = -1;
	}
}