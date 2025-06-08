# win-shortcut

`win-shortcut` is a library that lets you create Windows shortcuts easily. It's main entry point is the `create_shortcut()` function, but it also contains a bunch of other utilities that may be handy when creating shortcuts.

## Package contents

### Creating shortcuts: `win_shortcut.create_shortcut()`

Create a shortcut (`.lnk` file) at a specified location, running the specified command (optionally with command-line arguments).

Arguments (all of them except `path` and `cmd` are optional):
- `path: Path` - Path to the created shortcut.
- `cmd: Sequence[str | Path]` - Command to run. `cmd[0]` must be the path to an executable file. It is recommended to use `shutil.which()` or `pathext.which()` to produce `cmd[0]`.
- `icon: tuple[Path, int]` - Icon to use for the shortcut. The first value is the path to the file containing the icon, the second one is the index of the icon within the file. If unspecified or set to `None`, defaults to first icon within the target executable.
- `description: str`: Description string, shown in the "Comment" field of the "Properties" dialog. If unspecified or set to `None`, defaults to the empty string.
- `window_style: win_shortcut.WindowStyle`: Sets how the target executable should be started. Must be one of `win_shortcut.WindowStyle.NORMAL`, `win_shortcut.WindowStyle.MINIMZED`, or `win_shortcut.WindowStyle.MAXIMIZED`. If unspecified or set to `None`, defaults to `win_shortcut.WindowStyle.NORMAL`.
- `working_directory: Optional[Path]`: If specified, the current working directory will be changed to the specified directory when running the target executable. If unspecified or set to `None`, the target executable will be run in whichever directory is the current working directory at the time.

The function is implemented using Windows COM API calls, so it may raise `OSError` on failure.

### Querying known folders

Windows has a concept called "known folders", which are special folders identified by GUIDs called `KNOWNFOLDERID`. Known folders include the Windows folder, the user's Desktop, Start Menu etc.

Known folders are often used to place shortcuts in.

#### `win_shortcut.get_known_folder()`

Returns full path (as a `pathlib.Path` object) of a known folder identified by its `KNOWNFOLDERID`. Raises `OSError` if an error happens.

Note that not all known folders have a path associated with them. Calling `get_known_folder()` with such a `KNOWNFOLDERID` will result in an `OSError` being raised.

Arguments:
- `folderid: str`: GUID (`KNOWNFOLDERID`) of the folder you want to query. It can be specified as a string, or one of the predefined values from `win_shortcut.KnownFolderId` can be used. See [Microsoft's documentation](https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid) for the meaning of the predefined values.

#### `win_shortcut.get_desktop_folder()`

Returns full path of the Desktop folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.Desktop)`.

#### `win_shortcut.get_start_menu_folder()`

Returns full path of the Start Menu folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.StartMenu)`.

#### `win_shortcut.get_startup_folder()`

Returns full path of the Startup folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.Startup)`.

#### `win_shortcut.get_windows_folder()`

Returns full path of the Windows folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.Windows)`.

#### `win_shortcut.get_system_folder()`

Returns full path of the System folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.System)`.

#### `win_shortcut.get_program_files_folder()`

Returns full path of the Program Files folder. Shorthand for `win_shortcut.get_known_folder(win_shortcut.KnownFolderId.ProgramFiles)`.

### Handling short paths: `win_shortcut.get_short_path()`

Returns the short (8.3) path form (as a `pathlib.Path` object) of the specified path. This can be useful for getting around path length limitations and quoting issues (short paths contain no spaces).

Note that not all NTFS volumes have short paths enabled. In that case, `get_short_path()` will simply return the path it was given.

Arguments:
- `path: Path`: File or directory path to query the short form of.

### Classic icons: `win_shortcut.pifmgr`

`pifmgr.dll` has been part of Windows since time immemorial. It contains 38 retro icons (image courtesy of [mvps.org](https://mvps.org/serenitymacros/iconlist.html)):

![Icons in pifmgr.dll](images/pifmgr.png)

The `win_shortcut.pifmgr` object exposes the following constants that can be used as the `icon` argument of `create_shortcut()`:

* `win_shortcut.pifmgr.MS_DOS = (PIFMGR_DLL, 0)`
* `win_shortcut.pifmgr.UMBRELLA = (PIFMGR_DLL, 1)`
* `win_shortcut.pifmgr.TOY_BLOCK = (PIFMGR_DLL, 2)`
* `win_shortcut.pifmgr.NEWSPAPER = (PIFMGR_DLL, 3)`
* `win_shortcut.pifmgr.APPLE = (PIFMGR_DLL, 4)`
* `win_shortcut.pifmgr.LIGHTNING = (PIFMGR_DLL, 5)`
* `win_shortcut.pifmgr.EUPHONIUM = (PIFMGR_DLL, 6)`
* `win_shortcut.pifmgr.BEACH_BALL = (PIFMGR_DLL, 7)`
* `win_shortcut.pifmgr.LIGHTBULB = (PIFMGR_DLL, 8)`
* `win_shortcut.pifmgr.COLUMN = (PIFMGR_DLL, 9)`
* `win_shortcut.pifmgr.MONEY = (PIFMGR_DLL, 10)`
* `win_shortcut.pifmgr.COMPUTER = (PIFMGR_DLL, 11)`
* `win_shortcut.pifmgr.KEYBOARD = (PIFMGR_DLL, 12)`
* `win_shortcut.pifmgr.FILING_CABINET = (PIFMGR_DLL, 13)`
* `win_shortcut.pifmgr.BOOK = (PIFMGR_DLL, 14)`
* `win_shortcut.pifmgr.PAPERS_WITH_CLIP = (PIFMGR_DLL, 15)`
* `win_shortcut.pifmgr.PAPER_WITH_CRAYON = (PIFMGR_DLL, 16)`
* `win_shortcut.pifmgr.PENCIL = (PIFMGR_DLL, 17)`
* `win_shortcut.pifmgr.PAPER_WITH_PENCIL = (PIFMGR_DLL, 18)`
* `win_shortcut.pifmgr.DICE = (PIFMGR_DLL, 19)`
* `win_shortcut.pifmgr.WINDOWS = (PIFMGR_DLL, 20)`
* `win_shortcut.pifmgr.SEARCH = (PIFMGR_DLL, 21)`
* `win_shortcut.pifmgr.DOMINO = (PIFMGR_DLL, 22)`
* `win_shortcut.pifmgr.CARDS = (PIFMGR_DLL, 23)`
* `win_shortcut.pifmgr.FOOTBALL = (PIFMGR_DLL, 24)`
* `win_shortcut.pifmgr.DOCTORS_BAG = (PIFMGR_DLL, 25)`
* `win_shortcut.pifmgr.WIZARD_HAT = (PIFMGR_DLL, 26)`
* `win_shortcut.pifmgr.RACECAR = (PIFMGR_DLL, 27)`
* `win_shortcut.pifmgr.SHIP = (PIFMGR_DLL, 28)`
* `win_shortcut.pifmgr.PLANE = (PIFMGR_DLL, 29)`
* `win_shortcut.pifmgr.BOAT = (PIFMGR_DLL, 30)`
* `win_shortcut.pifmgr.TRAFFIC_LIGHT = (PIFMGR_DLL, 31)`
* `win_shortcut.pifmgr.RABBIT = (PIFMGR_DLL, 32)`
* `win_shortcut.pifmgr.RADAR = (PIFMGR_DLL, 33)`
* `win_shortcut.pifmgr.SWORDS = (PIFMGR_DLL, 34)`
* `win_shortcut.pifmgr.SHIELD_WITHSWORD = (PIFMGR_DLL, 35)`
* `win_shortcut.pifmgr.MACE = (PIFMGR_DLL, 36)`
* `win_shortcut.pifmgr.DYNAMITE = (PIFMGR_DLL, 37)`

## Licensing

This library is licensed under the MIT license.
