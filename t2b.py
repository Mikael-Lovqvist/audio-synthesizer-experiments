#This experiment is just to react to midi events

import midi

with midi.Sequencer(mode=midi.SND_SEQ_OPEN_INPUT) as seq:

	s = midi.Subscription(seq, (16, 0), seq)
	s.start()

	while True:
		ev = seq.read_event()
		print(ev)
