// Hand.h

#ifndef _handToken_h
#define _handToken_h

#include "SharedConstants.h"
#include "Card.h"
#include <array>
#include <string>

class Hand
{
	std::array<Card*, 5> cardList; // List of pointers to Cards
	std::string hash_string;
	
public: 
	Hand();
	~Hand();
	void dealHand(Card *card0
		,Card *card1 
		,Card *card2
		,Card *card3
		,Card *card4);
		 
	int countHand();
	int getRunPoints();
	int getRunPoints_old();
	void rotateHand();
	void printHand();
	double getExpectationValue();
	std::string getHashString();
	void updateHashString();
};


#endif