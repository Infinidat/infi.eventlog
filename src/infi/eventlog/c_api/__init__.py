import infi.cwrap
import ctypes

HANDLE = ctypes.c_void_p
EVT_HANDLE = HANDLE
LPCWSTR = ctypes.c_wchar_p
DWORD = ctypes.c_ulong
BOOL = ctypes.c_ulong

class EventLogFunction(infi.cwrap.WrappedFunction):
    return_value = ctypes.c_ulong

    @classmethod
    def get_parameters(cls):
        raise NotImplementedError()

    @classmethod
    def get_errcheck(cls):
    	# return infi.cwrap.errcheck_zero()
        return infi.cwrap.errcheck_nonzero()

    @classmethod
    def get_library_name(cls):
    	return "Wevtapi.dll"


class EvtOpenLog(EventLogFunction):
	return_value = EVT_HANDLE

	@classmethod
	def get_errcheck(cls):
		return infi.cwrap.errcheck_zero()

	@classmethod
	def get_parameters(cls):
		return (
			    (EVT_HANDLE, infi.cwrap.IN, "Session"),
			    (LPCWSTR, infi.cwrap.IN, "Path"),
			    (DWORD, infi.cwrap.IN, "Flags"),
			   )

class EvtClose(EventLogFunction):
	return_value = BOOL

	@classmethod
	def get_parameters(cls):
		return (
                (EVT_HANDLE, infi.cwrap.IN, "Object"),
			   )

