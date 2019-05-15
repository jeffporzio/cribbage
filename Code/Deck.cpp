// Deck.cpp 

#include "Deck.h"
#include "Card.h"
#include <iostream>
#include <new>
#include "suitsEnum.h"



Deck :: Deck()
{
	int numbers[13] = {1,2,3,4,5,6,7,8,9,10,11,12,13};
	int suits[4] = {0,1,2,3};
	
	int i = 0;
	for(int suit=0; suit<4; suit++){
		for(int number=0; number<13; number++){
			Card thisCard;
			thisCard.initCard(number, (suitsEnum) suit);
			cardList[i] = thisCard;
			i++;
		}
	}

}

Deck :: ~Deck()
{

}

void Deck :: shuffle()
{
	
}

void Deck :: printLogicalIDs()
{
	for(int i = 0; i < size; i++){
		cardList[i].printCardLogicalID();
	}
}

void Deck :: printDeck()
{
	for(int i = 0; i < size; i++){
		cardList[i].printCard();
		std::cout << "\n";
	}
}