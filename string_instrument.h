#ifndef STRING_INSTRUMENT_H
#include "common.h"

typedef struct string_instrument {
	SAMPLE_TYPE ratio;
	SAMPLE_TYPE velocity;
	SAMPLE_TYPE value;

	buffer_segment* output_buffers[3];
	buffer_segment* injection_buffers[3];
	buffer_segment* dampening_buffers[3];
} string_instrument;


string_instrument* allocate_string_instrument();
void set_string_instrument_frequency(string_instrument* instrument, float frequency);
buffer_segment* access_output_buffer(string_instrument* instrument, int buffer_id);
buffer_segment* access_injection_buffer(string_instrument* instrument, int buffer_id);
buffer_segment* access_dampening_buffer(string_instrument* instrument, int buffer_id);
void initialize_string_instrument(string_instrument* instrument, float frequency);
void process_string_instrument(string_instrument* instrument, int buffer_id);


#define STRING_INSTRUMENT_H
#endif