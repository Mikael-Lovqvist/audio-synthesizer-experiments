import qplot
from ffi import lib, SAMPLE_RATE,  filter, buffer_segment, ctypes, timer_filter, string_instrument_triangular


def tripple_buffer():
	return tuple(ctypes.pointer(buffer_segment()) for i in range(3))


i = string_instrument_triangular()
i.output_buffers[:] = tripple_buffer()
i.injection_buffers[:] = tripple_buffer()
i.dampening_buffers[:] = tripple_buffer()

lib.fill_buffer(i.dampening_buffers[0], 0.05)

i.slope = 0.1

i.injection_buffers[0].contents[10] = 1.0

lib.set_string_instrument_frequency_triangular(i, 2000)
lib.process_string_instrument_triangular(i, 0)


qplot.plot_multiple_buffers(SAMPLE_RATE, i.output_buffers[0].contents)


