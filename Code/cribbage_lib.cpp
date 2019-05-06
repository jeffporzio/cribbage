// cribbage_lib.cpp 

// Standard Libraries
#include <iostream> 
#include <new>

// Headers: 
#include "suitsEnum.h"

using namespace std;

#define JACK 11
#define NUM_CARD_IN_HAND 5

// Card class
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
	logicalID = number + 13*suit_offset;
}

void Card :: printCard()
{
	cout << number << " of " << suit << "\t"; 
}

bool Card :: operator==(const Card &other)
{
	if(this->logicalID == other.logicalID){
		return true;
	} else {
		return false;
	}
}


// Hand class
class Hand
{
	Card cardList[5];
	
public: 
	Hand(Card *card0
		,Card *card1 
		,Card *card2
		,Card *card3
		,Card *card4);
		 
	int countHand();
	void printHand();
	double getExpectationValue();
};

Hand :: Hand(Card *card0
			,Card *card1 
			,Card *card2
			,Card *card3
			,Card *card4)
{
	cardList[0] = *card0;
	cardList[1] = *card1;
	cardList[2] = *card2;
	cardList[3] = *card3;
	cardList[4] = *card4;
}

int Hand :: countHand()
{
	return 0;
}

void Hand :: printHand()
{
	int i;
	for(i = 0; i < NUM_CARD_IN_HAND; i++){
		cardList[i].printCard();
	}
}
