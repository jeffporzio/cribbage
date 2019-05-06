// Deck.cpp 

#include "Deck.h"
#include "Card.h"
#include <iostream>
#include "suitsEnum.h"



Deck :: Deck()
{
	try { 
		cardList = new Card[size];
	} catch (bad_alloc xa) { 
		cout << "Bad allocation. \n"; 
		return 1; 
	}
	
	
	
}

Deck :: ~Deck()
{
	delete [] cardList;
}

void Deck :: shuffle()
{
	
}

void Deck :: printLogicalIDs()
{
	for(int i = 0; i < size; i++){
		cardList[i]->printCardLogicalID();
	}
}

void Deck :: printDeck()
{
	for(int i = 0; i < size; i++){
		cardList[i]->printCard();
		cout << "\n";
	}
}