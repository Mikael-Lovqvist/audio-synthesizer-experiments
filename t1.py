import qplot
from ffi import lib, SAMPLE_RATE


instrument1 = lib.allocate_string_instrument()
instrument2 = lib.allocate_string_instrument()


lib.deprecated_initialize_string_instrument(instrument1, lib.calculate_frequency(45+24))
lib.deprecated_initialize_string_instrument(instrument2, lib.calculate_frequency(54+36))


lib.access_injection_buffer(instrument1, 0).contents[20] = 0.05
lib.access_injection_buffer(instrument2, 0).contents[40] = 0.03



lib.fill_buffer(lib.access_dampening_buffer(instrument1, 0), 0.05)
lib.fill_buffer(lib.access_dampening_buffer(instrument2, 0), 0.03)

lib.process_string_instrument(instrument1, 0)	#Run first buffer
lib.process_string_instrument(instrument2, 0)	#Run first buffer


output_buffer = lib.allocate_buffer()

lib.clear_buffer(output_buffer)
lib.mix_in_buffer(output_buffer, lib.access_output_buffer(instrument1, 0))
lib.mix_in_buffer(output_buffer, lib.access_output_buffer(instrument2, 0))

qplot.plot_buffer(output_buffer.contents, SAMPLE_RATE)

#print(tuple(lib.access_output_buffer(instrument1, 0).contents))
#print(tuple(lib.access_output_buffer(instrument2, 0).contents))


# #print(lib.

# #print(instrument.contents.ratio)