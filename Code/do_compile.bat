@echo off

CALL g++ -static -static-libgcc -static-libstdc++ -o ../Building/Deck.o -c Deck.cpp
CALL g++ -static -static-libgcc -static-libstdc++ -o ../Building/Hand.o -c Hand.cpp
CALL g++ -static -static-libgcc -static-libstdc++ -o ../Building/Card.o -c Card.cpp
CALL g++ -static -static-libgcc -static-libstdc++ -o ../Building/CribbageMain.o -c CribbageMain.cpp

CALL g++ -static -static-libgcc -static-libstdc++ -o cribbage.exe ../Building/Deck.o ../Building/Hand.o ../Building/Card.o ../Building/CribbageMain.o
