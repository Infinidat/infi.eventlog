
import ctypes
import infi.cwrap

HANDLE = ctypes.c_void_p
EVT_HANDLE = HANDLE
LPCWSTR = ctypes.c_wchar_p
DWORD = ctypes.c_ulong
BOOL = ctypes.c_ulong
POINTER = ctypes.POINTER
PDWORD = POINTER(DWORD)

TRUE = 1
FALSE = 0

MAX_LENGTH = 256
ERROR_NO_MORE_ITEMS = 259

open_handles = dict()
handles_data = dict()
max_handle_id = 1
available_channel_names = ["System", "Application"]

class WindowsException(Exception):
    def __init__(self, winerror):
        super(WindowsException, self).__init__()
        self.winerror = winerror

InvalidHandle = WindowsException

class Channel(object):
    def __init__(self, name):
        super(Channel, self).__init__()
        self.name = name

class AvailableChannelsEnum(object):
    pass

def get_new_handle():
    global max_handle_id
    handle = max_handle_id
    max_handle_id +=1 
    return handle

def EvtOpenLog(session, path, flags):
    assert session is None
    assert path in available_channel_names
    handle = get_new_handle()
    open_handles[handle] = Channel(path)
    return handle

def EvtClose(handle):
    assert handle in open_handles
    open_handles.pop(handle)

def EvtOpenChannelEnum(session, flags):
    assert session is None
    handle = get_new_handle()
    open_handles[handle] = AvailableChannelsEnum()
    handles_data[handle] = list(available_channel_names)
    return handle

def EvtNextChannelPath(handle, buffer_size, buffer, buffer_used_size):
    assert handle in open_handles
    value = open_handles[handle]
    assert isinstance(value, AvailableChannelsEnum)
    if not handles_data[handle]:
        raise WindowsException(ERROR_NO_MORE_ITEMS)
    item = handles_data[handle].pop()
    return 1, ctypes.create_unicode_buffer(item), len(item)
