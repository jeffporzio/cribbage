// Deck.h 


#ifndef _deckToken_h
#define _deckToken_h

#include "Card.h"


class Deck
{
private:
	static const int size = 52;
public:
	Card cardList[size];
	Deck();
	~Deck();
	// getCardsFromIndex();
	void shuffle();
	void printLogicalIDs();
	void printDeck();
};


#endif