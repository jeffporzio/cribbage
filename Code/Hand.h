// Hand.h

#ifndef _handToken_h
#define _handToken_h

#include "SharedConstants.h"
#include "Card.h"

class Hand
{
	Card* cardList[NUM_CARDS_IN_HAND]; // List of pointers to Cards
	
public: 
	Hand();
	void dealHand(Card *card0
		,Card *card1 
		,Card *card2
		,Card *card3
		,Card *card4);
		 
	int countHand();
	void printHand();
	double getExpectationValue();
};


#endif