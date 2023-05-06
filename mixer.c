#include "string_instrument.h"
#include <stdlib.h>

//TODO - verify allocations
//TODO - free stuff


buffer_segment* allocate_buffer() {
	return calloc(1, sizeof(buffer_segment));
}

void clear_buffer(buffer_segment* target_buffer) {
	for (int s=0; s<BUFFER_SIZE; s++) {
		(*target_buffer)[s] = 0;
	}
}

void fill_buffer(buffer_segment* target_buffer, SAMPLE_TYPE value) {
	for (int s=0; s<BUFFER_SIZE; s++) {
		(*target_buffer)[s] = value;
	}
}

void mix_in_buffer(buffer_segment* target_buffer, const buffer_segment* source_buffer) {
	for (int s=0; s<BUFFER_SIZE; s++) {
		(*target_buffer)[s] += (*source_buffer)[s];
	}
}
