// Deck.h 

// Forward declare Card
class Card;

class Deck
{
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