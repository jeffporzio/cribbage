// Hand.h

// Forward declare Card
class Card;


class Hand
{
	Card* cardList[5];
	
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