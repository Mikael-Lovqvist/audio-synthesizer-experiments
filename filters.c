#include "filters.h"
#include <stdlib.h>



void process_exp_filter(filter* filter, int buffer_id) {

	#define O				(*filter->output_buffers[buffer_id])[s]
	#define I 				(*filter->input_buffers[buffer_id])[s]
	#define Value			filter->value

	for (int s=0; s<BUFFER_SIZE; s++) {
		O = copysignf(powf(fminf(fabs(I), 1.0), Value), I);
	}
}


void process_weighted_memory_filter(weighted_memory_filter* filter, int buffer_id) {

	#define O				(*filter->output_buffers[buffer_id])[s]
	#define W 				(*filter->weight_buffers[buffer_id])[s]
	#define I 				(*filter->input_buffers[buffer_id])[s]
	#define Value			filter->value

	for (int s=0; s<BUFFER_SIZE; s++) {
		Value = O = Value * (1.0 - W) + I * W;
	}
}




void process_lp_filter(filter* filter, int buffer_id) {

	#define O				(*filter->output_buffers[buffer_id])[s]
	#define I 				(*filter->input_buffers[buffer_id])[s]
	#define Value			filter->value
	#define Slope			filter->slope

	for (int s=0; s<BUFFER_SIZE; s++) {
		SAMPLE_TYPE D = I - Value;
		//Value += copysignf(powf(D, 2), D) / Slope;
		Value += D / Slope;
		O = Value;
	}
}



void process_timer_filter(timer_filter* filter, int buffer_id) {

	#define O				(*filter->output_buffers[buffer_id])[s]
	#define I 				(*filter->input_buffers[buffer_id])[s]
	#define Time			filter->time
	#define TimeOut			filter->timeout
	#define H				filter->high
	#define L				filter->low

	SAMPLE_TYPE D2 = (H - L) * 0.5;
	SAMPLE_TYPE L2 = (H + L) * 0.5;

	for (int s=0; s<BUFFER_SIZE; s++) {

		Time = fmaxf(Time, TimeOut * I);
		Time = fmaxf(Time - 1.0, -1.0);	//Go towards -1 with the slope 1.0
		O = L2 + copysignf(D2, Time);
	}
}
