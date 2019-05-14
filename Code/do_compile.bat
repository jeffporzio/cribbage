@echo off 

g++ -o Building/Deck.o -c Deck.cpp
g++ -o Building/Hand.o -c Hand.cpp
g++ -o Building/Card.o -c Card.cpp
g++ -o Building/CribbageMain.o -c CribbageMain.cpp

g++ -o cribbage.exe Building/Deck.o Building/Hand.o Building/Card.o
