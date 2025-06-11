__all__ = [
    'get_short_path',
]

import ctypes
from pathlib import Path

from win_shortcut._winapi import GetShortPathNameW

def get_short_path(path: Path) -> Path:
    """
    Returns the short (8.3) path form (as a `pathlib.Path` object) of the specified path. This can be useful for getting around path length limitations and quoting issues (short paths contain no spaces).

    Note that not all NTFS volumes have short paths enabled. In that case, `get_short_path()` will simply return the path it was given.

    Arguments:
    - `path: Path`: File or directory path to query the short form of.
    """

    bufsize = 260
    while True:
        buffer = ctypes.create_unicode_buffer(bufsize)

        ret = GetShortPathNameW(str(path), buffer, bufsize)
        if ret==0:
            # an error happened
            raise ctypes.WinError(ctypes.GetLastError())
        elif ret > bufsize:
            # buffer was too small, retry with properly sized buffer
            bufsize = ret
        else:
            return Path(ctypes.wstring_at(buffer))
