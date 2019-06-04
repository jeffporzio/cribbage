#pragma once

#include <array>

class Combo {


public:
	Combo(int size);
	~Combo();
	int getIndex(unsigned i);
	void setIndex(unsigned i, int val);
	void clear();
	int size;
	void printCombo();
	std::array<int, 5> indeces = { -1,-1,-1,-1,-1 };
};
