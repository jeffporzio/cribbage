// cribbage_lib.cpp 

#include <iostream> 
#include <new>
#include <vector>
using namespace std;

#define JACK 11
#define NUM_CARD_IN_HAND

// Card class
class Card
{
	int number, value, logicalID; 
	char suit; 
	
public: 
	Card(int number, char suit);
	void printCard();
	
};

Card :: Card(int number, char suit)
{
	// Set the counting value
	if(number >= 10) { value = 10;}
	else {value = number;}

	// LogicalID: 
	int logicalID;
	if     (suit == "D")      {suit_offset = 0;}
	else if(suit == "H") {suit_offset = 1;}
	else if(suit == "C") {suit_offset = 2;}
	else if(suit == "S") {suit_offset = 3;}
	logicalID = number + 13*suit_offset;
}

void Card :: printCard()
{
	cout << number << " of " << suit << "\n"; 
}


// Hand class
class Hand
{
	Card cardList[5];
	
public: 
	Hand();
	void dumpHand();
	void putCardInHand(Card card);
	int countHand();
	void printHand();
	float getExpectationValue();
};

Hand :: Hand(Card *p)
{
	for(int i = 0; i < NUM_CARD_IN_HAND; i++){
		cardList[i] = 
	}		
}
