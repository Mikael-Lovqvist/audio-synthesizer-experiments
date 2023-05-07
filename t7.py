from ffi import lib, SAMPLE_RATE, BUFFER_SIZE, filter, buffer_segment, ctypes, timer_filter, string_instrument_triangular, string_instrument, filter, weighted_memory_filter
import threading, midi, time
from math import tau, sqrt

transpose = -12


buffer_references = list()

def tripple_buffer():
	#We store them in buffer_references to make sure they don't get freed
	buffers = tuple(buffer_segment() for i in range(3))
	buffer_references.extend(buffers)
	return tuple(map(ctypes.pointer, buffers))

class pending_instrument:
	injection_compensation = 0.000025*10
	def __init__(self, note):
		self.buffer_index_lock = threading.Lock()
		self.buffer_index = 0
		self.backend = string_instrument()
		self.frequency = lib.calculate_frequency(note)
		self.frequency_in_rads_per_sec = self.frequency * tau / 360

		self.depressed_dampening = 0.00001
		self.released_dampening = 0.0005

		self.dampening_switcher = weighted_memory_filter()
		self.dampening_switcher.value = self.released_dampening
		self.dampening_switcher.input_buffers[:] = tripple_buffer()
		self.dampening_switcher.weight_buffers[:] = tripple_buffer()
		self.dampening_switcher.output_buffers[:] = tripple_buffer()

		lib.set_string_instrument_frequency(self.backend, self.frequency)
		self.backend.output_buffers[:] = tripple_buffer()
		self.backend.injection_buffers[:] = tripple_buffer()
		self.backend.dampening_buffers[:] = self.dampening_switcher.output_buffers[:]


		self.exp_filter = filter(value=.25)
		self.exp_filter.input_buffers[:] = self.backend.output_buffers[:]
		self.exp_filter.output_buffers[:] = tripple_buffer()


	def process(self):
		lib.process_weighted_memory_filter(self.dampening_switcher, self.buffer_index)
		lib.process_string_instrument(self.backend, self.buffer_index)
		lib.process_exp_filter(self.exp_filter, self.buffer_index)
		lib.clear_buffer(self.backend.injection_buffers[self.buffer_index])
		lib.clear_buffer(self.dampening_switcher.weight_buffers[self.buffer_index])	#Clear dampening weights

	def get_output_buffer(self):
		return self.exp_filter.output_buffers[self.buffer_index]

	def note_on(self, velocity):
		sample_index = int(time.monotonic() * SAMPLE_RATE) % BUFFER_SIZE

		note_injection = velocity / 127
		harmonic_amplitude = sqrt(note_injection**2 + (note_injection / self.frequency_in_rads_per_sec))
		with self.buffer_index_lock:
			self.backend.injection_buffers[self.buffer_index].contents[sample_index] = self.injection_compensation * 0.003 / harmonic_amplitude

			self.dampening_switcher.weight_buffers[self.buffer_index].contents[sample_index] = 1.0
			self.dampening_switcher.input_buffers[self.buffer_index].contents[sample_index] = self.depressed_dampening


	def note_off(self, off_velocity):
		sample_index = int(time.monotonic() * SAMPLE_RATE) % BUFFER_SIZE

		with self.buffer_index_lock:
			self.dampening_switcher.weight_buffers[self.buffer_index].contents[sample_index] = 1.0
			self.dampening_switcher.input_buffers[self.buffer_index].contents[sample_index] = self.released_dampening

class dampened_instrument:
	injection_compensation = 0.5
	def __init__(self, note):
		self.buffer_index_lock = threading.Lock()
		self.buffer_index = 0
		self.backend = string_instrument()
		self.frequency = lib.calculate_frequency(note)
		self.frequency_in_rads_per_sec = self.frequency * tau / 360

		self.depressed_dampening = 0.00001
		self.released_dampening = 0.0005

		self.dampening_switcher = weighted_memory_filter()
		self.dampening_switcher.value = self.released_dampening
		self.dampening_switcher.input_buffers[:] = tripple_buffer()
		self.dampening_switcher.weight_buffers[:] = tripple_buffer()
		self.dampening_switcher.output_buffers[:] = tripple_buffer()


		lib.set_string_instrument_frequency(self.backend, self.frequency)
		self.backend.output_buffers[:] = tripple_buffer()
		self.backend.injection_buffers[:] = tripple_buffer()
		self.backend.dampening_buffers[:] = self.dampening_switcher.output_buffers[:]


	def process(self):
		lib.process_weighted_memory_filter(self.dampening_switcher, self.buffer_index)
		lib.process_string_instrument(self.backend, self.buffer_index)
		lib.clear_buffer(self.backend.injection_buffers[self.buffer_index])
		lib.clear_buffer(self.dampening_switcher.weight_buffers[self.buffer_index])	#Clear dampening weights

	def get_output_buffer(self):
		return self.backend.output_buffers[self.buffer_index]

	def note_on(self, velocity):
		sample_index = int(time.monotonic() * SAMPLE_RATE) % BUFFER_SIZE

		note_injection = velocity / 127
		harmonic_amplitude = sqrt(note_injection**2 + (note_injection / self.frequency_in_rads_per_sec))
		with self.buffer_index_lock:
			self.backend.injection_buffers[self.buffer_index].contents[sample_index] = self.injection_compensation * 0.003 / harmonic_amplitude

			self.dampening_switcher.weight_buffers[self.buffer_index].contents[sample_index] = 1.0
			self.dampening_switcher.input_buffers[self.buffer_index].contents[sample_index] = self.depressed_dampening


	def note_off(self, off_velocity):
		sample_index = int(time.monotonic() * SAMPLE_RATE) % BUFFER_SIZE

		with self.buffer_index_lock:
			self.dampening_switcher.weight_buffers[self.buffer_index].contents[sample_index] = 1.0
			self.dampening_switcher.input_buffers[self.buffer_index].contents[sample_index] = self.released_dampening

class exp_regular_instrument:
	injection_compensation = 0.002
	def __init__(self, note):
		self.buffer_index_lock = threading.Lock()
		self.buffer_index = 0
		self.backend = string_instrument()
		self.frequency = lib.calculate_frequency(note)
		self.frequency_in_rads_per_sec = self.frequency * tau / 360


		self.backend.output_buffers[:] = tripple_buffer()
		self.backend.injection_buffers[:] = tripple_buffer()
		self.backend.dampening_buffers[:] = tripple_buffer()

		lib.set_string_instrument_frequency(self.backend, self.frequency)
		lib.fill_buffer(self.backend.dampening_buffers[0], 0.001)
		lib.fill_buffer(self.backend.dampening_buffers[1], 0.001)
		lib.fill_buffer(self.backend.dampening_buffers[2], 0.001)

		self.exp_filter = filter(value=.25)
		self.exp_filter.input_buffers[:] = self.backend.output_buffers[:]
		self.exp_filter.output_buffers[:] = tripple_buffer()


	def process(self):
		lib.process_string_instrument(self.backend, self.buffer_index)
		lib.process_exp_filter(self.exp_filter, self.buffer_index)
		lib.clear_buffer(self.backend.injection_buffers[self.buffer_index])


	def get_output_buffer(self):
		return self.exp_filter.output_buffers[self.buffer_index]

class triangular_instrument:
	injection_compensation = 1.0
	def __init__(self, note):
		self.buffer_index_lock = threading.Lock()
		self.buffer_index = 0
		self.backend = string_instrument_triangular()
		self.frequency = lib.calculate_frequency(note)
		self.frequency_in_rads_per_sec = self.frequency * tau / 360

		self.backend.slope = (self.frequency / SAMPLE_RATE) * 5

		lib.set_string_instrument_frequency_triangular(self.backend, self.frequency)
		self.backend.output_buffers[:] = tripple_buffer()
		self.backend.injection_buffers[:] = tripple_buffer()
		self.backend.dampening_buffers[:] = tripple_buffer()


		lib.fill_buffer(self.backend.dampening_buffers[0], 0.00007)
		lib.fill_buffer(self.backend.dampening_buffers[1], 0.00007)
		lib.fill_buffer(self.backend.dampening_buffers[2], 0.00007)

	def process(self):
		lib.process_string_instrument_triangular(self.backend, self.buffer_index)
		lib.clear_buffer(self.backend.injection_buffers[self.buffer_index])

	def get_output_buffer(self):
		return self.backend.output_buffers[self.buffer_index]

instrument_lut = {note:pending_instrument(note) for note in range(0, 100)}



def midi_input_thread():
	last_note = None
	with midi.Sequencer(mode=midi.SND_SEQ_OPEN_INPUT) as seq:

		s = midi.Subscription(seq, (16, 0), seq)
		s.start()


		while True:
			ev = seq.read_event().contents

			if ev.type == midi.SND_SEQ_EVENT_NOTEON:
				note = ev.data.note
				last_note = note.note + transpose

				if note.velocity == 0:
					if i := instrument_lut.get(last_note):
						i.note_off(note.off_velocity)
				else:
					if i := instrument_lut.get(last_note):
						i.note_on(note.velocity)


			elif ev.type == midi.SND_SEQ_EVENT_NOTEOFF:
				note = ev.data.note
				last_note = note.note + transpose

				if i := instrument_lut.get(last_note):
					i.note_off(note.off_velocity)



t = threading.Thread(target=midi_input_thread)
t.start()








output_buffer = lib.allocate_buffer()
output_stream = lib.setup_output_stream()

while True:

	for i in instrument_lut.values():
		i.process()


	lib.clear_buffer(output_buffer)
	for i in instrument_lut.values():
		lib.mix_in_buffer(output_buffer, i.get_output_buffer())

	lib.write_output_buffer(output_stream, output_buffer)

	for i in instrument_lut.values():
		with i.buffer_index_lock:
			i.buffer_index = (i.buffer_index + 1) % 3
