
from infi.pyutils.contexts import contextmanager
from infi.exceptools import InfiException
from logging import getLogger

logger = getLogger(__name__)

def get_c_api_module():
	from brownie.importing import import_string
	from os import name
	from mock import Mock
	is_windows = name == "nt"
	return import_string("infi.eventlog.c_api" if is_windows else "infi.eventlog.c_api.mock")

c_api = get_c_api_module()

class EventLogException(InfiException):
	pass

class Session(object):
	@contextmanager
	def open_context(self):
		raise NotImplementedError()

class LocalSession(Session):
	@contextmanager
	def open_context(self):
		yield None
		
class RemoteSession(Session):
	def __init__(self, computername, username, password, domain):
		raise NotImplementedError()

class EventLog(object):	
	def __init__(self, session):
		super(EventLog, self).__init__()
		self._session =  session

	@contextmanager
	def open_channel_context(self, channel_name):
		with self._session.open_context() as session_handle:
			evt_handle = c_api.EvtOpenLog(session_handle, channel_name, 0)
		try:
			yield evt_handle
		finally:
			c_api.EvtClose(evt_handle)

	def get_available_channels(self):
		with self._session.open_context() as session_handle:
			evt_handle = c_api.EvtOpenChannelEnum(session_handle, 0)
			while True:
				try:
					_, buffer, buffer_used = c_api.EvtNextChannelPath(evt_handle, c_api.MAX_LENGTH)
					yield buffer.value
				except c_api.WindowsException, error:
					if error.winerror != c_api.ERROR_NO_MORE_ITEMS:
						raise
					break

class LocalEventLog(EventLog):
	def __init__(self):
		super(LocalEventLog, self).__init__(LocalSession())
