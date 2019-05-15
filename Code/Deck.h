// Deck.h 

#include "Card.h"

class Deck
{
private:
	static const int size = 52;
	Card cardList[size];
public:
	Deck();
	~Deck();
	// getCardsFromIndex();
	void shuffle();
	void printLogicalIDs();
	void printDeck();
};