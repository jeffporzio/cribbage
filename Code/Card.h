//Card.h

#include <iostream>
# include "suitsEnum.h"

class Card
{
	int number;
	int value;
	int logicalID; 
	unsigned suit; 
	
public: 
	Card(int number, unsigned suit);
	void printCard();
	// Overloaded operators
	bool operator==(const Card &other);	
};