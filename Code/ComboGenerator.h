#pragma once

#include <vector>


class ComboGenerator{

public: 
	ComboGenerator(const int N, const int k);
	~ComboGenerator();

	bool isFinished();
	int* getNextCombo();
	void restart();


private: 
	int N;
	int k;
	int i; 
	bool is_finished;
	std::vector<int> current_combo;
	std::vector<int> combo_to_return;


};