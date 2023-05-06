#ifndef MIXER_H
#include "common.h"

buffer_segment* allocate_buffer();
void clear_buffer(buffer_segment* target_buffer);
void mix_in_buffer(buffer_segment* target_buffer, const buffer_segment* source_buffer);
void fill_buffer(buffer_segment* target_buffer, SAMPLE_TYPE value);

#define MIXER_H
#endif