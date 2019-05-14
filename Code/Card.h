//Card.h

class Card
{
	int number;
	int value;
	int logicalID; 
	unsigned suit; 
	
public: 
	Card(int number, unsigned suit);
	Card(); //parameterless constructor
	void printCard();
	void printCardLogicalID();
	// Overloaded operators
	bool operator==(Card other);	
};