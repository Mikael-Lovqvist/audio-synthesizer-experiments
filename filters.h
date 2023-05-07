#ifndef FILTERS_H
#include "common.h"


typedef struct filter {
	SAMPLE_TYPE value;
	SAMPLE_TYPE slope;

	buffer_segment* input_buffers[3];
	buffer_segment* output_buffers[3];

} filter;


typedef struct weighted_memory_filter {
	SAMPLE_TYPE value;

	buffer_segment* input_buffers[3];
	buffer_segment* weight_buffers[3];
	buffer_segment* output_buffers[3];

} weighted_memory_filter;


typedef struct timer_filter {
	SAMPLE_TYPE high;
	SAMPLE_TYPE low;
	SAMPLE_TYPE time;
	SAMPLE_TYPE timeout;

	buffer_segment* input_buffers[3];
	buffer_segment* output_buffers[3];

} timer_filter;


void process_lp_filter(filter* filter, int buffer_id);
void process_timer_filter(timer_filter* filter, int buffer_id);
void process_exp_filter(filter* filter, int buffer_id);
void process_weighted_memory_filter(weighted_memory_filter* filter, int buffer_id);

#define FILTERS_H
#endif