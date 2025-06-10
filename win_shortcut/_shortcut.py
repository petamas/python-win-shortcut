__all__ = [
    'create_shortcut',
    'WindowStyle',
]

import ctypes
from enum import IntEnum
from pathlib import Path
from typing import Optional, Sequence

import comtypes.client
import comtypes.hresult
import comtypes.shelllink
import comtypes.persist
import mslex

class WindowStyle(IntEnum):
    NORMAL = comtypes.shelllink.SW_SHOWNORMAL
    MAXIMIZED = comtypes.shelllink.SW_SHOWMAXIMIZED
    MINIMIZED = comtypes.shelllink.SW_SHOWMINNOACTIVE

def create_shortcut(
    path: Path,
    cmd: Sequence[str|Path],
    *,
    icon: Optional[tuple[Path, int]] = None,
    description: Optional[str] = None,
    window_style: Optional[WindowStyle] = None,
    working_directory: Optional[Path] = None
) -> None:
    """
    Create a shortcut (`.lnk` file) at a specified location, running the specified command (optionally with command-line arguments).

    Arguments (all of them except `path` and `cmd` are optional):
    - `path: Path` - Path to the created shortcut.
    - `cmd: Sequence[str | Path]` - Command to run. `cmd[0]` must be the path to an executable file. It is recommended to use `shutil.which()` or `pathext.which()` to produce `cmd[0]`.
    - `icon: tuple[Path, int]` - Icon to use for the shortcut. The first value is the path to the file containing the icon, the second one is the index of the icon within the file. If unspecified or set to `None`, defaults to first icon within the target executable.
    - `description: str`: Description string, shown in the "Comment" field of the "Properties" dialog. If unspecified or set to `None`, defaults to the empty string.
    - `window_style: win_shortcut.WindowStyle`: Sets how the target executable should be started. Must be one of `win_shortcut.WindowStyle.NORMAL`, `win_shortcut.WindowStyle.MINIMZED`, or `win_shortcut.WindowStyle.MAXIMIZED`. If unspecified or set to `None`, defaults to `win_shortcut.WindowStyle.NORMAL`.
    - `working_directory: Optional[Path]`: If specified, the current working directory will be changed to the specified directory when running the target executable. If unspecified or set to `None`, the target executable will be run in whichever directory is the current working directory at the time.

    The function is implemented using Windows COM API calls, so it may raise `OSError` on failure.
    """

    if description is None:
        description = ''
    if window_style is None:
        window_style = WindowStyle.NORMAL


    shell_link: comtypes.shelllink.IShellLinkW = comtypes.client.CreateObject(comtypes.shelllink.ShellLink)

    shell_link.SetPath(str(cmd[0]))
    shell_link.SetArguments(mslex.join([str(arg) for arg in cmd[1:]], for_cmd=False))

    if icon is None:
        shell_link.SetIconLocation('', 0)
    else:
        shell_link.SetIconLocation(str(icon[0]), icon[1])

    shell_link.SetDescription(description)

    shell_link.ShowCmd = window_style.value

    if working_directory is not None:
        shell_link.SetWorkingDirectory(str(working_directory))

    persist_file: comtypes.persist.IPersistFile = shell_link.QueryInterface(comtypes.persist.IPersistFile)
    ret = persist_file.Save(str(path.absolute()), True)

    if ret != comtypes.hresult.S_OK:
        # https://learn.microsoft.com/en-us/windows/win32/api/objidl/nf-objidl-ipersistfile-save says:
        # > If the object was successfully saved, the return value is S_OK.
        # > Otherwise, it is S_FALSE.
        # > This method can also return various storage errors.

        if ret==comtypes.hresult.S_FALSE:
            # By default, S_FALSE would be treated as ERROR_INVALID_FUNCTION, because both have the value of 0x1, so we map it to ERROR_CANNOT_MAKE instead
            raise ctypes.WinError(82, 'IPersistFile::Save() returned S_FALSE')
        else:
            raise ctypes.WinError(ret)
