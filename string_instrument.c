#include "string_instrument.h"
#include <stdlib.h>

//TODO - verify allocations


string_instrument* allocate_string_instrument() {
	return calloc(1, sizeof(string_instrument));
}

void deprecated_initialize_string_instrument(string_instrument* instrument, float frequency) {
	//Note - here we allocate buffers but there may be situations where we want one or more of these buffers to be the output buffer of a previous process
	//		so we should have a more intelligent initializer that can deal with this.
	//		best would be if we could set up the entire chain as a higher level and allocate buffers as needed.
	instrument->ratio = powf((frequency * M_TAU) / sSAMPLE_RATE, 2);
	instrument->velocity = 0;
	instrument->value = 0;

	for (int bid=0; bid<3; bid++) {
		instrument->output_buffers[bid] = calloc(BUFFER_SIZE, sizeof(SAMPLE_TYPE));
		instrument->dampening_buffers[bid] = calloc(BUFFER_SIZE, sizeof(SAMPLE_TYPE));
		instrument->injection_buffers[bid] = calloc(BUFFER_SIZE, sizeof(SAMPLE_TYPE));
	}

}


void set_string_instrument_frequency(string_instrument* instrument, float frequency) {
	instrument->ratio = powf((frequency * M_TAU) / sSAMPLE_RATE, 2);
}

void set_string_instrument_frequency_triangular(string_instrument_triangular* instrument, float frequency) {
	instrument->ratio = powf((frequency * M_TAU) / sSAMPLE_RATE, 2);
}

void process_string_instrument(string_instrument* instrument, int buffer_id) {

	#define O		(*instrument->output_buffers[buffer_id])[s]
	#define I 		(*instrument->injection_buffers[buffer_id])[s]
	#define D 		(*instrument->dampening_buffers[buffer_id])[s]
	#define Vel 	instrument->velocity
	#define Value	instrument->value
	#define R 		instrument->ratio

	for (int s=0; s<BUFFER_SIZE; s++) {
		Vel += -Value * R + I;
		Value += Vel;
		Vel *= (1.0 - D);
		O = Value;
	}
}

void process_string_instrument_triangular(string_instrument_triangular* instrument, int buffer_id) {

	#define O		(*instrument->output_buffers[buffer_id])[s]
	#define I 		(*instrument->injection_buffers[buffer_id])[s]
	#define D 		(*instrument->dampening_buffers[buffer_id])[s]
	#define Vel 	instrument->velocity
	#define Value	instrument->value
	#define R 		instrument->ratio
	#define Slope 	instrument->slope

	for (int s=0; s<BUFFER_SIZE; s++) {
		Vel += -Value * R + I;
		Value +=  copysignf(fminf(Slope, fabsf(Vel)), Vel);
		Vel *= (1.0 - D);
		O = Value;
	}
}

buffer_segment* access_output_buffer(string_instrument* instrument, int buffer_id) {
	return instrument->output_buffers[buffer_id];
}

buffer_segment* access_injection_buffer(string_instrument* instrument, int buffer_id) {
	return instrument->injection_buffers[buffer_id];
}

buffer_segment* access_dampening_buffer(string_instrument* instrument, int buffer_id) {
	return instrument->dampening_buffers[buffer_id];
}