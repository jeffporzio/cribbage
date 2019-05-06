// Card.cpp

#include "Card.h"
#include <iostream>
#include "suitsEnum"


Card :: Card(int number, unsigned suit)
{
	// Set the counting value
	if(number >= 10) { value = 10; }
	else {value = number;}

	// LogicalID: 
	int logicalID;
	int suit_offset;
	if     (suit == DIAMONDS) { suit_offset = 0; }
	else if(suit == HEARTS)   { suit_offset = 1; }
	else if(suit == CLUBS)    { suit_offset = 2; }
	else if(suit == SPADES  ) { suit_offset = 3; }
	logicalID = number + 13*suit_offset; // 13 cards per suit
}

Card :: Card()
{
	// Dummy values to be set later?
	number = -1;
	value = -1;
	logicalID = -1;
	suit = 5; 
}


void Card :: printCard()
{
	cout << number << " of " << suit << "\t"; 
}

void Card :: printCardLogicalID()
{
	cout << logicalID;
}

bool Card :: operator==(const Card &other)
{
	if(this->logicalID == other.logicalID){
		return true;
	} else {
		return false;
	}
}
