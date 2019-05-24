//Card.h

#ifndef _cardToken_h
#define _cardToken_h

#include "suitsEnum.h"

class Card
{
public:
	int value;
	int logicalID;  
	int number;
	unsigned suit;

	Card(); //Doing a constructor and an init function make builders and dependancy injection safer.
	void initCard(int number, suitsEnum suit);
	void printCard();
	void printCardLogicalID();
	// Overloaded operators
	bool operator==(Card other);
	bool operator<(Card other);
};

#endif