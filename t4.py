import qplot
from ffi import lib, SAMPLE_RATE,  filter, buffer_segment, ctypes


def tripple_buffer():
	return tuple(ctypes.pointer(buffer_segment()) for i in range(3))

f = filter(value=0, slope=10)
f.input_buffers[:] = tripple_buffer()
f.output_buffers[:] = tripple_buffer()


for i in range(10):
	f.input_buffers[0].contents[i + 5] = 1.0

lib.process_lp_filter(f, 0)

qplot.plot_multiple_buffers(SAMPLE_RATE, f.input_buffers[0].contents, f.output_buffers[0].contents)


#lib.allocate_buffer