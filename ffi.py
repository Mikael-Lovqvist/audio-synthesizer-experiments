import ctypes

lib = ctypes.CDLL('build/t1.so')

SAMPLE_TYPE = ctypes.c_float
SAMPLE_RATE = 48000
buffer_segment = SAMPLE_TYPE * 128

class string_instrument(ctypes.Structure):
	_fields_ = (
		('ratio', 					SAMPLE_TYPE),
		('velocity', 				SAMPLE_TYPE),
		('value', 					SAMPLE_TYPE),
		('output_buffers', 			ctypes.POINTER(buffer_segment) * 3),
		('injection_buffers', 		ctypes.POINTER(buffer_segment) * 3),
		('dampening_buffers', 		ctypes.POINTER(buffer_segment) * 3),
	)

lib.allocate_string_instrument.restype = ctypes.POINTER(string_instrument)
lib.initialize_string_instrument.argtypes = (ctypes.POINTER(string_instrument), ctypes.c_float)
lib.set_string_instrument_frequency.argtypes = (ctypes.POINTER(string_instrument), ctypes.c_float)

lib.process_string_instrument.argtypes = (ctypes.POINTER(string_instrument), ctypes.c_int)

lib.access_output_buffer.restype = ctypes.POINTER(buffer_segment)
lib.access_output_buffer.argtypes = (ctypes.POINTER(string_instrument), ctypes.c_int)

lib.access_injection_buffer.restype = ctypes.POINTER(buffer_segment)
lib.access_injection_buffer.argtypes = (ctypes.POINTER(string_instrument), ctypes.c_int)

lib.access_dampening_buffer.restype = ctypes.POINTER(buffer_segment)
lib.access_dampening_buffer.argtypes = (ctypes.POINTER(string_instrument), ctypes.c_int)

lib.allocate_buffer.restype = ctypes.POINTER(buffer_segment)
lib.clear_buffer.argtypes = (ctypes.POINTER(buffer_segment),)
lib.fill_buffer.argtypes = (ctypes.POINTER(buffer_segment), SAMPLE_TYPE)
lib.mix_in_buffer.argtypes = (ctypes.POINTER(buffer_segment), ctypes.POINTER(buffer_segment))


lib.calculate_frequency.restype = ctypes.c_float
lib.calculate_frequency.argtypes = (ctypes.c_int,)


lib.setup_output_stream.restype = ctypes.c_void_p	#We don't filly specify the actual type, we just use it as a handle

lib.write_output_buffer.argtypes = (ctypes.c_void_p, ctypes.POINTER(buffer_segment))
lib.write_output_buffer.restype = ctypes.c_int