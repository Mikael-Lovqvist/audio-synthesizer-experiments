#include "common.h"
#include <stdlib.h>

//TODO - verify allocations
//TODO - free stuff



void mix_in_buffer(buffer_segment* target_buffer, const buffer_segment* source_buffer) {
	for (int s=0; s<BUFFER_SIZE; s++) {
		(*target_buffer)[s] += (*source_buffer)[s];
	}
}
