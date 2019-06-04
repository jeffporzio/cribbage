
#include "Combo.h"
#include <iostream>
#include "sharedConstants.h"


Combo::Combo(int size) {
	this->size = size; // These will all be the same size. It is up to the user not to read -1's.
	
	/*
	std::cout << "From inside Combo::Combo(): " << std::endl;
	std::cout << "Size: " << size << std::endl;
	for (auto& val : indeces) {
		std::cout << val << " " << std::endl;
	}
	*/
}

Combo::~Combo() {}


void Combo::printCombo() {
	for (auto val : this->indeces) { std::cout << val << " "; }
	std::cout << std::endl;
}

int Combo::getIndex(unsigned i) {
	return this->indeces[i];
}

void Combo::setIndex(unsigned i, int val) {
	//std::cout << "i from setIndex()" << i << std::endl;
	this->indeces[i] = val;
}

void Combo::clear() {
	for (int i = 0; i < size; i++) {
		this->indeces[i] = -1;
	}
}