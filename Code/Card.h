//Card.h

class Card
{
	int number;
	int value;
	int logicalID; 
	unsigned suit; 
	
public: 
	Card(); //parameterless constructor
	void initCard(int number, unsigned suit);
	void printCard();
	void printCardLogicalID();
	// Overloaded operators
	bool operator==(Card other);	
};