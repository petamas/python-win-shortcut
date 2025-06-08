__all__ = [
    'get_known_folder',
    'get_desktop_folder',
    'get_start_menu_folder',
    'get_startup_folder',
    'get_windows_folder',
    'get_system_folder',
    'get_program_files_folder',
]

import ctypes
from pathlib import Path

from comtypes import GUID # type: ignore[import-untyped]

from win_shortcut._known_folder_id import KnownFolderId

def get_known_folder(folderid: str) -> Path:
    """
    Returns full path (as a `pathlib.Path` object) of a known folder identified by its `KNOWNFOLDERID`. Raises `OSError` if an error happens.

    Note that not all known folders have a path associated with them. Calling `get_known_folder()` with such a `KNOWNFOLDERID` will result in an `OSError` being raised.

    Arguments:
    - `folderid: str`: GUID (`KNOWNFOLDERID`) of the folder you want to query. It can be specified as a string, or one of the predefined values from `win_shortcut.KnownFolderId` can be used. See [Microsoft's documentation](https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid) for the meaning of the predefined values.
    """

    output = ctypes.c_wchar_p()
    try:
        ret = ctypes.windll.shell32.SHGetKnownFolderPath(GUID(folderid), 0, None, ctypes.byref(output))
        if ret != 0:
            raise ctypes.WinError(ret)
        return Path(ctypes.wstring_at(output))
    finally:
        ctypes.oledll.ole32.CoTaskMemFree(output)

def get_desktop_folder() -> Path:
    """
    Returns full path of the Desktop folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.Desktop)`.
    """

    return get_known_folder(KnownFolderId.Desktop)

def get_start_menu_folder() -> Path:
    """
    Returns full path of the Start Menu folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.StartMenu)`.
    """

    return get_known_folder(KnownFolderId.StartMenu)

def get_startup_folder() -> Path:
    """
    Returns full path of the Startup folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.Startup)`.
    """

    return get_known_folder(KnownFolderId.Startup)

def get_windows_folder() -> Path:
    """
    Returns full path of the Windows folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.Windows)`.
    """

    return get_known_folder(KnownFolderId.Windows)

def get_system_folder() -> Path:
    """
    Returns full path of the System folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.System)`.
    """

    return get_known_folder(KnownFolderId.System)

def get_program_files_folder() -> Path:
    """
    Returns full path of the Program Files folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.ProgramFiles)`.
    """

    return get_known_folder(KnownFolderId.ProgramFiles)
