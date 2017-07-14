/*
 * Hot Plate v0.c
 * Built for Atmega328p
 *
 * Created: 7/1/2017 4:21:26 PM
 * Author : Matthew
 */ 

/*******************   UART Message Format  *****************************
*  - First byte is a header dictating message type						*
*  - Second byte is data for that message, stored as raw binary			*
*		so that no string-to-int conversion is needed					*
*  - (For temp reading) Third byte combines with 2nd to form				*
*		16-bit temp reading. MSB sent first.							*
*																		*	
*  Message Types:  1) (H)eater - (Rx) Sets duty cycle for hot plate		*
*								 heater coil. Values [0.100]			*
*                  2) (F)an    - (Rx) Determines cooling fan state		*
*                                Is a binary on or off					*
*                  3) (T)emp   - (Tx) send out temperature reading		*
*																		*
*																		*
*************************************************************************/

#define F_CPU 16000000

#define FOSC 16000000 // Clock Speed
#define BAUD 9600
#define MYUBRR FOSC/16/BAUD-1

#define ON			PORTB |= (1<<PORTB1)
#define OFF			PORTB &= ~(1<<PORTB1)
#define TOGGLE		PINB |= (1<<PINB1)

#define BUFFER_SIZE 30

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <string.h>

#include "USART_driver.h"
#include "PWM_driver.h"

ISR(TIMER1_COMPA_vect) {
	TOGGLE;
}

void SPI_MasterInit(void) {
	/* Set MOSI and SCK output, all others input */
	DDRB |= (1<<PB3)|(1<<PB5);
	/* Enable SPI, Master, set clock rate fck/16 */
	SPCR = (1<<SPE)|(1<<MSTR)|(1<<SPR0)|(1<<SPR1);//|(1<<CPHA);
	//SPSR = _BV(SPI2X);
}

void SPI_MasterTransmit(char cData) {
	/* Start transmission */
	SPDR = cData;
	/* Wait for transmission complete */
	while(!(SPSR & (1<<SPIF)));
}

uint8_t SPI_ReceiveByte(void) {
	char Rx_char;
	SPI_MasterTransmit(0x00);
	while(!(SPSR & (1<<SPIF)));
	Rx_char = SPDR;
	return Rx_char;
}

int main(void) {
	/********* Variables   ****************************/
	char string[BUFFER_SIZE] = {'\n'};
	unsigned char sentHeaterDC = 0;
	unsigned char sentHeaterDC_old = 0;
	char fanState = 0;
	char temp_s[10] = {'\n'};
	uint32_t temp = 0;
	
	/********* Config bits and inits ******************/
	// Enable OCR1A output pin on PB1, !SS as output
	DDRB |= _BV(PB1) | _BV(PB2); 
	DDRD |= _BV(PD4);
	PORTD |= _BV(PD4);
	PORTB |= _BV(PB2);
    USART_Init(MYUBRR);
	SPI_MasterInit();
	PWM_Init();
	sei();
	
    while (1) {
		clearString(string, BUFFER_SIZE);
		getString(string);
		switch (string[0]) {
			case 'H':
				sentHeaterDC_old = sentHeaterDC;
				sentHeaterDC = string[1];
				break;
			case 'F':
				fanState = string[1];
				break;
		}
		if (sentHeaterDC != sentHeaterDC_old)
			updatePWM((uint16_t)sentHeaterDC*80);
		PORTD &= ~_BV(PD4);
		PORTB &= ~_BV(PB2);
		//_delay_us(1);
		temp = (uint32_t)SPI_ReceiveByte();
		temp <<= 8;
		temp |= (uint32_t)SPI_ReceiveByte();
		temp <<= 8;
		temp |= (uint32_t)SPI_ReceiveByte();
		temp <<= 8;
		temp |= (uint32_t)SPI_ReceiveByte();
		PORTD |= _BV(PD4);
		PORTB |= _BV(PB2);
		clearString(temp_s, 10);
		temp_s[0] = (uint8_t)(temp>>24);
		temp_s[1] = (uint8_t)(temp>>16);
		temp_s[2] = (uint8_t)(temp>>8);
		temp_s[3] = (uint8_t)(temp);
		temp_s[4] = 0;
		putString(temp_s);
    }
}

