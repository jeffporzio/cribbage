// Deck.h 

#include <iostream>

// Forward declare Card
class Card;

class Deck
{
public:
	Card cardList[52];
	Deck();
	void shuffle();
	void printLogicalIDs();
	void printDeck();
};