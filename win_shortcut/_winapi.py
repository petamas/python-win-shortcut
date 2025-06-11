import ctypes
import ctypes.wintypes as wintypes
from typing import cast as typing_cast

from win_shortcut._byref import ByRef as ByRef

kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32
ole32 = ctypes.windll.ole32

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8)
    ]

    def __init__(self, guid: str):
        CLSIDFromString(guid, ByRef(self)) # HRESULT errors raise OSError automatically

ole32.CLSIDFromString.argtypes = [wintypes.LPCOLESTR, ctypes.POINTER(GUID)]
ole32.CLSIDFromString.restype = ctypes.HRESULT
# Return None instead of HRESULT because we never return nonzero HRESULT
def CLSIDFromString(s: str, guid: ByRef[GUID]) -> None:
    # HRESULT errors raise OSError automatically, no need to check
    ole32.CLSIDFromString(s, guid)

shell32.SHGetKnownFolderPath.argtypes = [GUID, wintypes.DWORD, wintypes.HANDLE, ctypes.POINTER(wintypes.LPWSTR)]
shell32.SHGetKnownFolderPath.restype = ctypes.HRESULT
# Return None instead of HRESULT because we never return nonzero HRESULT
def SHGetKnownFolderPath(folderid: GUID, flags: int, token: wintypes.HANDLE | None, path: ByRef[ctypes.c_wchar_p]) -> None:
    # HRESULT errors raise OSError automatically, no need to check
    shell32.SHGetKnownFolderPath(folderid, flags, token, path)

ole32.CoTaskMemFree.argtypes = [ctypes.c_void_p]
ole32.CoTaskMemFree.restype = None
def CoTaskMemFree(p: ctypes.c_void_p | ctypes.c_char_p | ctypes.c_wchar_p) -> None:
    ole32.CoTaskMemFree(p)

kernel32.GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
kernel32.GetShortPathNameW.restype = wintypes.DWORD
def GetShortPathNameW(longpath: str, shortpath: ctypes.Array[ctypes.c_wchar], bufsize: int) -> int:
    return typing_cast(int, kernel32.GetShortPathNameW(longpath, shortpath, bufsize))
