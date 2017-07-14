#include <avr/io.h>
#include "USART_driver.h"

void USART_Init( unsigned int ubrr)
{
	/*Set baud rate */
	UBRR0H = (unsigned char)(ubrr>>8);
	UBRR0L = (unsigned char)ubrr;
	//Enable receiver and transmitter */
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	/* Set frame format: 8data, 1 stop bit */
	UCSR0C = (3<<UCSZ00);
}

void USART_Transmit( unsigned char data )
{
	/* Wait for empty transmit buffer */
	while ( !( UCSR0A & (1<<UDRE0)) );
	/* Put data into buffer, sends the data */
	UDR0 = data;
}

unsigned char USART_Receive( void ) {
	/* Wait for data to be received */
	while ( !(UCSR0A & (1<<RXC0)) );
	
	/* Get and return received data from buffer */
	return UDR0;
}

void getString(char string[]) {
	char rch = 'a';
	uint8_t i = 0;
	while (rch != '\n') {
		rch = USART_Receive();
		string[i] = rch;
		i++;
	}
	string[++i] = '\n';
}

void putString(char string[]) {
	char ch;
	uint8_t i = 0;
	while(ch != '\n') {
		ch = string[i++];
		USART_Transmit(ch);
	}
}

// zero out string
void clearString(char string[], char len) {
	char i = 0;
	for (i; i < len; i++) {
		string[i] = '\n';
	}
}