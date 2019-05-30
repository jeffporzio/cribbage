// Hand.h

#ifndef _handToken_h
#define _handToken_h

#include "SharedConstants.h"
#include "Card.h"
#include <array>

class Hand
{
	std::array<Card*, 5> cardList; // List of pointers to Cards
	
public: 
	Hand();
	void dealHand(Card *card0
		,Card *card1 
		,Card *card2
		,Card *card3
		,Card *card4);
		 
	int countHand();
	int getRunPoints();
	int getRunPoints_new();
	void rotateHand();
	void printHand();
	double getExpectationValue();
};


#endif