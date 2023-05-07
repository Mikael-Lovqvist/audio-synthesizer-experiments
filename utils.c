#include "common.h"


float calculate_frequency(int semi) {
	/*
		In this calculation semi 48 is an A (440 Hz), we should figure out what is the common practice and make sure we comply.
		It seems that in MIDI, A2 is typically note 45 so I think that if we add 3 to the semi, we should be compatible.
	*/
	return powf(2, (float)(semi+3) / 12) * 27.5;
}



