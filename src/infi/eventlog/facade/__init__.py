
from infi.pyutils.contexts import contextmanager
from infi.exceptools import InfiException
from logging import getLogger

logger = getLogger(__name__)

def get_c_api_module():
	from brownie.importing import import_string
	from os import name
	from mock import Mock
	is_windows = name == "nt"
	return import_string("infi.eventlog.c_api") if is_windows else Mock()

c_api = get_c_api_module()


class EventLogException(InfiException):
	pass

class EventLog(object):	
	def __init__(self, channel_name):
		super(EventLog, self).__init__()
		self._channel_name = channel_name

	def __repr__(self):
		try:
			return "<Eventlog(channel_name={!r}>".format(channel_name)
		except:
			return super(EventLog, self).__repr__() 

	@contextmanager
	def open_context(self):
		self._evt_handle = c_api.EvtLogOpen(None, self._channel_name, 0)
		try:
			yield
		finally:
			c_api.EvtClose(self._evt_handle)