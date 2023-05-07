#include "common.h"
#include <stdio.h>
#include <pulse/simple.h>
#include <pulse/error.h>
#include <pulse/gccmacro.h>

//TODO - improve error handling and clean up

pa_simple* setup_output_stream() {
	static const pa_sample_spec ss = {
		.format = PA_SAMPLE_FLOAT32NE,
		.rate = SAMPLE_RATE,
		.channels = 1
	};

	static const pa_buffer_attr ba = {
		.maxlength = -1,
		.tlength = 1024,
	};

	pa_simple *s = NULL;
	int error;

	if (!(s = pa_simple_new(NULL, "efforting.tech", PA_STREAM_PLAYBACK, NULL, "playback", &ss, NULL, &ba, &error))) {
		fprintf(stderr, __FILE__": pa_simple_new() failed: %s\n", pa_strerror(error));
	}

	return s;

}

int write_output_buffer(pa_simple* output_stream, buffer_segment* buffer) {
	int error;
	int result = pa_simple_write(output_stream, *buffer, BUFFER_SIZE * sizeof(SAMPLE_TYPE), &error);
	if (result < 0) {
		fprintf(stderr, __FILE__": pa_simple_write() failed: %s\n", pa_strerror(error));
	}

	return result;
}

