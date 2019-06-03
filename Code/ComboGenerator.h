#pragma once

#include <vector>
#include "Combo.h"


class ComboGenerator{

public: 
	ComboGenerator(const int N, const int k);
	~ComboGenerator();

	bool isFinished();
	Combo getNextCombo();
	void restart();


private: 
	int N;
	int k;
	int max_unsat; 
	bool is_finished;
	Combo current_combo;
	Combo combo_to_return;


};