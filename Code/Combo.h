#pragma once

#include <array>

class Combo {


public:
	Combo(int size);
	~Combo();
	int& operator[](int i);
	Combo operator=(Combo other);
	void clear();
	int size;
private:
	std::array<int,5> indeces;
};
