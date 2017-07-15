#ifndef INCFILE1_H_
#define INCFILE1_H_

//volatile char stringReadyFlag;
//char buffer[100];

void USART_Init( unsigned int ubrr);
void USART_Transmit( unsigned char data );
unsigned char USART_Receive( void );
void getString(char strng[] );
void putString(char strng[]);
void clearString(char string[], char len);

#endif