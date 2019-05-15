//Card.h

#ifndef _cardToken_h
#define _cardToken_h

#include "suitsEnum.h"

class Card
{
	int number;
	int value;
	int logicalID; 
	unsigned suit; 
	
public: 
	Card(); //Dong a constructor and an init function make builders and dependancy injection safer.
	void initCard(int number, suitsEnum suit);
	void printCard();
	void printCardLogicalID();
	// Overloaded operators
	bool operator==(Card other);	
};

#endif