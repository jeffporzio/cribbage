// Deck.cpp 

#include "Deck.h"
#include "Card.h"
#include <iostream>
#include <new>
#include "suitsEnum.h"



Deck :: Deck()
{	
	int i = 0;
	for(int suit=0; suit<4; suit++){
		for(int number=1; number<=13; number++){
			Card thisCard;
			thisCard.initCard(number, (suitsEnum) suit);
			//thisCard.printCard();
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
	}
}