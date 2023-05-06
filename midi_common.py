from ctypes import *
import ctypes.util

SND_SEQ_OPEN_OUTPUT = 0x1
SND_SEQ_OPEN_INPUT = 0x2
SND_SEQ_OPEN_DUPLEX = SND_SEQ_OPEN_INPUT | SND_SEQ_OPEN_OUTPUT
SND_SEQ_PORT_TYPE_APPLICATION = 1 << 20
SND_SEQ_PORT_CAP_READ = 1 << 0
SND_SEQ_PORT_CAP_WRITE = 1 << 1
SND_SEQ_PORT_CAP_SUBS_READ = 1 << 5
SND_SEQ_PORT_CAP_SUBS_WRITE = 1 << 6
SND_SEQ_QUEUE_DIRECT = 253
SND_SEQ_ADDRESS_UNKNOWN = 253
SND_SEQ_ADDRESS_SUBSCRIBERS = 254

SND_SEQ_EVENT_NOTE = 5

SND_SEQ_EVENT_NOTEON = 6
SND_SEQ_EVENT_NOTEOFF = 7
SND_SEQ_EVENT_LENGTH_MASK = 3 << 2
SND_SEQ_EVENT_LENGTH_FIXED = 0 << 2
SND_SEQ_EVENT_CONTROLLER = 10
SND_SEQ_EVENT_CONTROL14 = 14
SND_SEQ_EVENT_PITCHBEND = 13

SND_SEQ_EVENT_NONE = 255

libasound = CDLL('libasound.so')


snd_seq_close = libasound.snd_seq_close
snd_seq_create_simple_port = libasound.snd_seq_create_simple_port
snd_seq_open = libasound.snd_seq_open
snd_seq_set_client_name = libasound.snd_seq_set_client_name
snd_seq_delete_simple_port = libasound.snd_seq_delete_simple_port


snd_seq_delete_simple_port.argtypes = c_void_p, c_int
snd_seq_delete_simple_port.restype = c_int

snd_seq_open.argtypes = POINTER(c_void_p), c_char_p, c_int, c_int
snd_seq_open.restype = c_int

snd_seq_close.argtypes = c_void_p,
snd_seq_close.restype = c_int

snd_seq_set_client_name.argtypes = c_void_p, c_char_p
snd_seq_set_client_name.restype = c_int

snd_seq_create_simple_port.argtypes = c_void_p, c_char_p, c_int, c_int
snd_seq_create_simple_port.restype = c_int


snd_seq_event_type_t = c_ubyte
snd_seq_tick_time_t = c_uint


class snd_seq_real_time(Structure):
	_fields_ = (
		('tv_sec', c_uint),
		('tv_nsec', c_uint),
	)

class snd_seq_timestamp_t(Union):
	_fields_ = (
		('tick', snd_seq_tick_time_t),
		('time', snd_seq_real_time),
	)

class snd_seq_addr_t(Structure):
	_fields_ = (
		('client', c_ubyte),
		('port', c_ubyte),
	)

class snd_seq_ev_note_t(Structure):
	_fields_ = (
		('channel', c_ubyte),
		('note', c_ubyte),
		('velocity', c_ubyte),
		('off_velocity', c_ubyte),
		('duration', c_uint),
	)

class snd_seq_ev_ctrl_t(Structure):
	_fields_ = (
		('channel', c_ubyte),
		('unused', c_ubyte*3),
		('param', c_uint),
		('value', c_int),
	)

class snd_seq_ev_raw8_t(Structure):
	_fields_ = (
		('d', c_ubyte * 12),
	)

class snd_seq_ev_raw32_t(Structure):
	_fields_ = (
		('d', c_uint * 32),
	)

class snd_seq_ev_ext_t(Structure):
	_fields_ = (
		('len', c_uint),
		('ptr', c_void_p),
	)

class snd_seq_queue_skew_t(Structure):
	_fields_ = (
		('value', c_uint),
		('base', c_uint),
	)

class snd_seq_connect_t(Structure):
	_fields_ = (
		('sender', snd_seq_addr_t),
		('dest', snd_seq_addr_t),
	)

class snd_seq_result_t(Structure):
	_fields_ = (
		('event', c_int),
		('result', c_int),
	)

class snd_seq_ev_queue_control_data_union(Union): #This union is anonymous in alsalib
	_fields_ = (
		('value', c_int),
		('time', snd_seq_timestamp_t),
		('position', c_uint),
		('skew', snd_seq_queue_skew_t),
		('d32', c_uint*2),
		('d8', c_ubyte*8),
	)

class snd_seq_ev_queue_control_t(Structure):
	_fields_ = (
		('queue', c_ubyte),
		('unused', c_ubyte*3),
		('param', snd_seq_ev_queue_control_data_union),
	)


class snd_seq_event_data_union(Union):	#This union is anonymous in alsalib
	_fields_ = (
		('note', snd_seq_ev_note_t),
		('control', snd_seq_ev_ctrl_t),
		('raw8', snd_seq_ev_raw8_t),
		('raw32', snd_seq_ev_raw32_t),
		('ext', snd_seq_ev_ext_t),
		('queue', snd_seq_ev_queue_control_t),
		('time', snd_seq_timestamp_t),
		('addr', snd_seq_addr_t),
		('connect', snd_seq_connect_t),
		('result', snd_seq_result_t),
	)


class snd_seq_event_t(Structure):
	_fields_ = (
		('type', snd_seq_event_type_t),
		('flags', c_ubyte),
		('tag', c_ubyte),
		('queue', c_ubyte),
		('time', snd_seq_timestamp_t),
		('source', snd_seq_addr_t),
		('dest', snd_seq_addr_t),
		('data', snd_seq_event_data_union),
	)


snd_midi_event_encode = libasound.snd_midi_event_encode
snd_midi_event_free = libasound.snd_midi_event_free
snd_midi_event_new = libasound.snd_midi_event_new
snd_seq_drain_output = libasound.snd_seq_drain_output
snd_seq_event_output_direct = libasound.snd_seq_event_output_direct

snd_midi_event_encode.argtypes = c_void_p, c_char_p, c_long, POINTER(snd_seq_event_t)
snd_midi_event_encode.restype = c_long


snd_midi_event_new.argtypes = c_size_t, c_void_p
snd_midi_event_new.restype = c_int

snd_midi_event_free.argtypes = c_void_p,
snd_midi_event_free.restype = None

snd_seq_event_output_direct.argtypes = c_void_p, POINTER(snd_seq_event_t)
snd_seq_event_output_direct.restype = c_int

snd_seq_drain_output.argtypes = c_void_p,
snd_seq_drain_output.restype = c_int

snd_seq_event_input = libasound.snd_seq_event_input	#Blocking, otherwise -EAGAIN, if fifi overrun -ENOSPC
snd_seq_event_input.argtypes = c_void_p, POINTER(POINTER(snd_seq_event_t))


snd_seq_client_id = libasound.snd_seq_client_id
snd_seq_client_id.argtypes = c_void_p,
snd_seq_client_id.restype = c_int


snd_seq_port_subscribe_malloc = libasound.snd_seq_port_subscribe_malloc
snd_seq_port_subscribe_malloc.argtypes = POINTER(c_void_p),
snd_seq_port_subscribe_malloc.restype = c_int

snd_seq_port_subscribe_free = libasound.snd_seq_port_subscribe_free
snd_seq_port_subscribe_free.argtypes = c_void_p,

snd_seq_port_subscribe_set_sender = libasound.snd_seq_port_subscribe_set_sender
snd_seq_port_subscribe_set_sender.argtypes = c_void_p, POINTER(snd_seq_addr_t)

snd_seq_port_subscribe_set_dest = libasound.snd_seq_port_subscribe_set_dest
snd_seq_port_subscribe_set_dest.argtypes = c_void_p, POINTER(snd_seq_addr_t)

snd_seq_port_subscribe_set_queue = libasound.snd_seq_port_subscribe_set_queue
snd_seq_port_subscribe_set_queue.argtypes = c_void_p, c_int

snd_seq_alloc_named_queue = libasound.snd_seq_alloc_named_queue
snd_seq_alloc_named_queue.argtypes = c_void_p, c_char_p
snd_seq_alloc_named_queue.restype = c_int

snd_seq_free_queue = libasound.snd_seq_free_queue
snd_seq_free_queue.argtypes = c_void_p, c_int
snd_seq_free_queue.restype = c_int

snd_seq_port_subscribe_set_time_update = libasound.snd_seq_port_subscribe_set_time_update
snd_seq_port_subscribe_set_time_update.argtypes = c_void_p, c_int

snd_seq_port_subscribe_set_time_real = libasound.snd_seq_port_subscribe_set_time_real
snd_seq_port_subscribe_set_time_real.argtypes = c_void_p, c_int

snd_seq_subscribe_port = libasound.snd_seq_subscribe_port
snd_seq_subscribe_port.argtypes = c_void_p, c_void_p
snd_seq_subscribe_port.restype = c_int


#libc = CDLL(ctypes.util.find_library("c"))
#libc.free.argtypes = c_void_p,
