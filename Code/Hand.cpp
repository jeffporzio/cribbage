// Hand.cpp

#include "Hand.h"
#include <iostream>
#include "sharedConstants.h"

// Passing pointers is cheaper and easier (especially when we implement design patterns later)
Hand :: Hand(Card *card0
			,Card *card1 
			,Card *card2
			,Card *card3
			,Card *card4) 
{
	cardList[0] = card0;
	cardList[1] = card1;
	cardList[2] = card2;
	cardList[3] = card3;
	cardList[4] = card4;
}

int Hand :: countHand()
{
	return 0;
}

void Hand :: printHand()
{
	int i;
	for(i = 0; i < NUM_CARD_IN_HAND; i++){
		cardList[i]->printCard();
	}
}