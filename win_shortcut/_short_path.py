__all__ = [
    'get_short_path',
]

import ctypes
from pathlib import Path

def get_short_path(path: Path) -> Path:
    """
    Returns the short (8.3) path form (as a `pathlib.Path` object) of the specified path. This can be useful for getting around path length limitations and quoting issues (short paths contain no spaces).

    Note that not all NTFS volumes have short paths enabled. In that case, `get_short_path()` will simply return the path it was given.

    Arguments:
    - `path: Path`: File or directory path to query the short form of.
    """

    while True:
        buf_size = ctypes.windll.kernel32.GetShortPathNameW(str(path), None, 0)
        output = ctypes.create_unicode_buffer(buf_size)

        result = ctypes.windll.kernel32.GetShortPathNameW(str(path), output, buf_size)
        if result == 0:
            raise ctypes.WinError()

        if result==buf_size-1:
            return Path(ctypes.wstring_at(output))
