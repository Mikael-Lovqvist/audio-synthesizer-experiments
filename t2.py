from ffi import lib, SAMPLE_RATE
import threading, midi


buffer_index_lock = threading.Lock()


instrument1 = lib.allocate_string_instrument()

lib.initialize_string_instrument(instrument1, lib.calculate_frequency(45+24))




lib.fill_buffer(lib.access_dampening_buffer(instrument1, 0), 0.0001)
lib.fill_buffer(lib.access_dampening_buffer(instrument1, 1), 0.0001)
lib.fill_buffer(lib.access_dampening_buffer(instrument1, 2), 0.0001)


#output_buffer = lib.allocate_buffer()

#lib.clear_buffer(output_buffer)
#lib.mix_in_buffer(output_buffer, lib.access_output_buffer(instrument1, 0))
#lib.mix_in_buffer(output_buffer, lib.access_output_buffer(instrument2, 0))

buffer_index = 0


def midi_input_thread():
	last_note = None
	with midi.Sequencer(mode=midi.SND_SEQ_OPEN_INPUT) as seq:

		s = midi.Subscription(seq, (16, 0), seq)
		s.start()

		while True:
			ev = seq.read_event().contents



			if ev.type == midi.SND_SEQ_EVENT_NOTEON:
				note = ev.data.note
				last_note = note.note

				print('Note on', note.note, note.velocity)

				if note.velocity == 0:
					with buffer_index_lock:		#No action for now
						pass
				else:
					with buffer_index_lock:
						lib.set_string_instrument_frequency(instrument1, lib.calculate_frequency(note.note))
						lib.access_injection_buffer(instrument1, buffer_index).contents[0] = 0.02 * note.velocity / 127


			elif ev.type == midi.SND_SEQ_EVENT_PITCHBEND:
				print('Pitch', ev.data.control.value)
				if last_note:
					frequency_bend = (1.0 + (ev.data.control.value / 8192) *.125)
					print(frequency_bend)
					lib.set_string_instrument_frequency(instrument1, lib.calculate_frequency(last_note) * frequency_bend)

			elif ev.type == midi.SND_SEQ_EVENT_NOTEOFF:
				note = ev.data.note
				print('Note off', note.note, note.off_velocity)


t = threading.Thread(target=midi_input_thread)
t.start()


output_stream = lib.setup_output_stream()

while True:


	lib.process_string_instrument(instrument1, buffer_index)	#Run first buffer
	lib.clear_buffer(lib.access_injection_buffer(instrument1, buffer_index))	#We clear injection buffer always here, we are just testing

	lib.write_output_buffer(output_stream, lib.access_output_buffer(instrument1, buffer_index))

	with buffer_index_lock:
		buffer_index = (buffer_index + 1) % 3
