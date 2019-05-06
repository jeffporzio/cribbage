// Deck.h 

// Forward declare Card
class Card;

class Deck
{
	Card cardList[52];
public:
	Deck();
	getCardsFromIndex();
	void shuffle();
	void printLogicalIDs();
	void printDeck();
};