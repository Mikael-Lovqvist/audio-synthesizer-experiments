from midi_common import *
import time

#TODO is def to add output queue so we can schedule note off

cstr = lambda s: bytes(s, 'utf-8')+ b'\x00'
#todo - make more stuff with _ prefix
#Note - was testing using libc to free events that were read but got "double free" so I guess it is handled properly - not sure how/why yet

def get_address(target, seq_port_id=None):
	if isinstance(target, Sequencer):
		assert seq_port_id != None and seq_port_id >= 0, 'When calling get_address with target of Sequencer, seq_port_id must be supplied'
		return snd_seq_addr_t(client=target.client_id, port=seq_port_id)
	elif isinstance(target, tuple):
		return snd_seq_addr_t(client=target[0], port=target[1])
	else:
		raise TypeError(target)

class Subscription:
	def __init__(self, sequencer, sender=None, dest=None):
		self.sequencer = sequencer
		self.sender = sender
		self.dest = dest
		self.subcriptions = c_void_p()
		snd_seq_port_subscribe_malloc(self.subcriptions)
		sequencer.register_child(self)

	def free(self):
		if self.subcriptions:
			snd_seq_port_subscribe_free(self.subcriptions)

	def start(self):

		if self.sender:
			snd_seq_port_subscribe_set_sender(self.subcriptions, get_address(self.sender, self.sequencer.port_out_id))
		if self.dest:
			snd_seq_port_subscribe_set_dest(self.subcriptions, get_address(self.dest, self.sequencer.port_in_id))

		#These things should not be hardcoded
		snd_seq_port_subscribe_set_queue(self.subcriptions, 0)
		snd_seq_port_subscribe_set_time_update(self.subcriptions, 1)
		snd_seq_port_subscribe_set_time_real(self.subcriptions, 1)
		snd_seq_subscribe_port(self.sequencer.handle, self.subcriptions)


class Sequencer:
	default_dest = snd_seq_addr_t(
		client=SND_SEQ_ADDRESS_SUBSCRIBERS,
		port=SND_SEQ_ADDRESS_UNKNOWN,
	)

	def __init__(self, sequencer_name='default', mode=SND_SEQ_OPEN_DUPLEX, client_name='efforting.tech', port_in_name='Input Stream', port_out_name='Output Stream', send_vel_0_instead_of_note_off=False, default_dest_client=None, default_dest_port=None):
		self.handle = c_void_p()
		self.sequencer_name = sequencer_name
		self.mode = mode
		self.client_name = client_name
		self.client_id = None
		self.send_vel_0_instead_of_note_off = send_vel_0_instead_of_note_off

		self.port_in_name = port_in_name
		self.port_in_id = None

		self.port_out_name = port_out_name
		self.port_out_id = None

		self.children = set()


		dest_client = self.default_dest.client if default_dest_client is None else default_dest_client
		dest_port = self.default_dest.port if default_dest_port is None else default_dest_port

		self.default_dest = snd_seq_addr_t(dest_client, dest_port)


	def read_event(self):
		event_ptr = POINTER(snd_seq_event_t)()
		r = snd_seq_event_input(self.handle, event_ptr)
		return event_ptr

	def __enter__(self):
		assert snd_seq_open(self.handle, cstr(self.sequencer_name), self.mode, 0) == 0, f'Failed to open device `{self.sequencer_name}´'
		snd_seq_set_client_name(self.handle, cstr(self.client_name))
		self.client_id = snd_seq_client_id(self.handle)

		if self.mode & SND_SEQ_OPEN_INPUT:
			self.port_in_id = snd_seq_create_simple_port(self.handle, cstr(self.port_in_name), SND_SEQ_PORT_CAP_WRITE | SND_SEQ_PORT_CAP_SUBS_WRITE, SND_SEQ_PORT_TYPE_APPLICATION)
			assert self.port_in_id >= 0, f'Failed to create input stream `{self.port_in_name}´'

		if self.mode & SND_SEQ_OPEN_OUTPUT:
			self.port_out_id = snd_seq_create_simple_port(self.handle, cstr(self.port_out_name), SND_SEQ_PORT_CAP_READ | SND_SEQ_PORT_CAP_SUBS_READ, SND_SEQ_PORT_TYPE_APPLICATION)
			assert self.port_out_id >= 0, f'Failed to create input stream `{self.port_out_name}´'

		return self

	def __exit__(self, exc_type, exc_value, traceback):

		for child in self.children:
			try:
				child.free()
			except Exception as e:
				print(f'Failed to clean up child {child} due to {e}')

		if self.port_in_id != None and self.port_in_id >= 0:
			snd_seq_delete_simple_port(self.handle, self.port_in_id)

		if self.port_out_id != None and self.port_out_id >= 0:
			snd_seq_delete_simple_port(self.handle, self.port_out_id)

		if self.handle:
			snd_seq_close(self.handle)

	def register_child(self, child):
		self.children.add(child)


	def output_direct(self, event):
		snd_seq_event_output_direct(self.handle, event)

	def drain_output(self):
		snd_seq_drain_output(self.handle)


	def send_note_on(self, channel, note, velocity, **kw_args):
		self.send_note_event(SND_SEQ_EVENT_NOTEON, channel, note, velocity, **kw_args)

	def send_note(self, channel, note, duration, velocity, **kw_args):
		self.send_note_event(SND_SEQ_EVENT_NOTE, channel, note, velocity, duration=duration, **kw_args)

	def send_note_off(self, channel, note, **kw_args):
		if self.send_vel_0_instead_of_note_off:
			self.send_note_event(SND_SEQ_EVENT_NOTEON, channel, note, 0, **kw_args)
		else:
			self.send_note_event(SND_SEQ_EVENT_NOTEOFF, channel, note, 0, **kw_args)

	def send_controller(self, channel, parameter, value, dest=default_dest, evt_type=SND_SEQ_EVENT_CONTROLLER):
		self.output_direct(snd_seq_event_t(
			type=evt_type,
			queue=SND_SEQ_QUEUE_DIRECT,
			dest = dest,
			source = get_address(self, self.port_out_id),
			data=snd_seq_event_data_union(
				control=snd_seq_ev_ctrl_t(
					channel=channel,
					parameter=parameter,
					value=value,
				),
			)
		))
	def send_controller_14bit(self, channel, parameter, value, dest=default_dest):
		self.send_controller(channel, parameter, value, dest=dest, evt_type=SND_SEQ_EVENT_CONTROL14)

	def send_pitchbend(self, channel, value, dest=default_dest):
		self.send_controller(channel, 0, value, dest=dest, evt_type=SND_SEQ_EVENT_PITCHBEND)

	def send_note_event(self, event, channel, note, velocity, duration=0, dest=None):
		if dest == None:
			dest = self.default_dest

		self.output_direct(snd_seq_event_t(
			type=event,
			queue=SND_SEQ_QUEUE_DIRECT,
			dest = dest,
			source = get_address(self, self.port_out_id),
			data=snd_seq_event_data_union(
				note=snd_seq_ev_note_t(
					channel=channel,
					note=note,
					velocity=velocity,
					duration=duration,
				),
			)
		))

