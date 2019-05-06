// Hand.h

#include "SharedConstants.h"

class Card; // Forward declaration is sufficient for header files


class Hand
{
	Card* cardList[NUM_CARDS_IN_HAND];
	
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