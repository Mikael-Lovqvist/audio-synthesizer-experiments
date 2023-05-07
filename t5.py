import qplot
from ffi import lib, SAMPLE_RATE,  filter, buffer_segment, ctypes, timer_filter


def tripple_buffer():
	return tuple(ctypes.pointer(buffer_segment()) for i in range(3))

f = timer_filter(high = 0.5, low = 0.0, timeout=3.0)
f.input_buffers[:] = tripple_buffer()
f.output_buffers[:] = tripple_buffer()


for i in range(3):
	f.input_buffers[0].contents[i*10 + 5] = 1.0

lib.process_timer_filter(f, 0)

qplot.plot_multiple_buffers(SAMPLE_RATE, f.input_buffers[0].contents, f.output_buffers[0].contents)


#lib.allocate_buffer