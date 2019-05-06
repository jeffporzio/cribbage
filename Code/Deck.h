// Deck.h 

// Forward declare Card
class Card;

class Deck
{
	int size = 52;
	cardList = Card[size];
public:
	Deck();
	~Deck();
	getCardsFromIndex();
	void shuffle();
	void printLogicalIDs();
	void printDeck();
};