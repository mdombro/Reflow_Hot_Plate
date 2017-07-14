#include <avr/io.h>
#include "PWM_driver.h"

void PWM_Init(void) {
	/**************************************************
	*					Equation:                     *
	*			   F_CPU/(2*N*TOP))                   * 
	*	Where N is the prescalar set by CS bits, can  *
	*	be 1, 8, 64, 256, 1024                        *
	*	TOP == ICR1, input compare register           * 
	*	See datasheet page 166 for more details       * 
	**************************************************/
	
	TCCR1A=0;
	TCCR1B=0;
	TCCR1A |= _BV(WGM11);
	TCCR1B |= _BV(WGM13)| _BV(CS12) | _BV(CS10);
	OCR1A = 1;
	ICR1=8000;  // Sets the PWM frequency
	TCCR1A |= _BV(COM1A1);
}

void updatePWM(uint16_t DC) {
	OCR1A = DC;
}