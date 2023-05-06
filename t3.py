#In this experiment we will instantiate multiple instruments and mix them together
from ffi import lib, SAMPLE_RATE
import threading, midi




class instrument:
	def __init__(self, note):
		self.buffer_index_lock = threading.Lock()
		self.buffer_index = 0
		self.backend = lib.allocate_string_instrument()

		lib.initialize_string_instrument(self.backend, lib.calculate_frequency(note))

		lib.fill_buffer(lib.access_dampening_buffer(self.backend, 0), 0.0001)
		lib.fill_buffer(lib.access_dampening_buffer(self.backend, 1), 0.0001)
		lib.fill_buffer(lib.access_dampening_buffer(self.backend, 2), 0.0001)



transpose = 0

output_stream = lib.setup_output_stream()
instrument_lut = {note:instrument(note) for note in range(20, 100)}


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

				print('Note on', note.note, note.velocity)


				if note.velocity == 0:
					pass
					#with buffer_index_lock:		#No action for now
						#pass
				else:
					if i := instrument_lut.get(last_note):
						with i.buffer_index_lock:
							lib.access_injection_buffer(i.backend, i.buffer_index).contents[0] = 0.01 * note.velocity / 127


			# elif ev.type == midi.SND_SEQ_EVENT_PITCHBEND:
			# 	print('Pitch', ev.data.control.value)
			# 	if last_note:
			# 		frequency_bend = (1.0 + (ev.data.control.value / 8192) *.125)
			# 		print(frequency_bend)
			# 		lib.set_string_instrument_frequency(instrument1, lib.calculate_frequency(last_note) * frequency_bend)

			elif ev.type == midi.SND_SEQ_EVENT_NOTEOFF:
				note = ev.data.note
				print('Note off', note.note, note.off_velocity)


t = threading.Thread(target=midi_input_thread)
t.start()



output_buffer = lib.allocate_buffer()


while True:

	for i in instrument_lut.values():
		lib.process_string_instrument(i.backend, i.buffer_index)	#Run first buffer
		lib.clear_buffer(lib.access_injection_buffer(i.backend, i.buffer_index))	#We clear injection buffer always here, we are just testing


	lib.clear_buffer(output_buffer)
	for i in instrument_lut.values():
		lib.mix_in_buffer(output_buffer, lib.access_output_buffer(i.backend, i.buffer_index))

	lib.write_output_buffer(output_stream, output_buffer)

	for i in instrument_lut.values():
		with i.buffer_index_lock:
			i.buffer_index = (i.buffer_index + 1) % 3
