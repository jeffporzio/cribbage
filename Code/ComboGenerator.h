#pragma once


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
	int* current_combo; 
	bool is_finished;
	int* combo_to_return;

};