
#include "Combo.h"
#include <iostream>
#include "sharedConstants.h"


Combo::Combo(int size) {
	this->size = NUM_CARDS_IN_HAND; // These will all be the same size. It is up to the user not to read -1's.
	for (int i = 0; i < size; i++) {
		this->indeces[i] = -1;
	}
}

Combo::~Combo() {}

int& Combo::operator[](int i) {
	return this->indeces[i];
}

Combo Combo::operator=(Combo other) {

	if (this->indeces.size() == other.indeces.size()) {
		for (int i = 0; i < this->size; i++) {
			this->indeces[i] = other[i];
		}
	}
	else {
		std::cout << "Tried to compare two different size combos! \n Did not copy in Combo::operator=()";
	}

	return *this;
}

void Combo::clear() {
	for (int i = 0; i < 5; i++) {
		this->indeces[i] = -1;
	}
}