# Cortile Addons
[![Release](https://github.com/leukipp/cortile-addons/actions/workflows/release.yml/badge.svg)](https://github.com/leukipp/cortile-addons/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/cortile?label=PyPI%20Package)](https://pypi.org/project/cortile)

Python bindings for the linux auto tiling manager cortile.

Cortile provides auto tiling for XFCE, LXDE, LXQt, KDE and GNOME (Mate, Deepin, Cinnamon, Budgie) based desktop environments.
There is build in support for Openbox, Fluxbox, IceWM, Xfwm, KWin, Marco, Muffin, Mutter and other EWMH compliant window managers using the X11 window system.

This package only provides the python bindings and does not contain the cortile release binary.
To use this package, you need to install the [binary](https://github.com/leukipp/cortile/releases) from the main repository. For more details, please refer to the cortile [README.md](https://github.com/leukipp/cortile?tab=readme-ov-file#addons) file.

## Installation [![installation](https://img.shields.io/badge/pip-%20Python%20-red?style=flat-square)](#installation-)
To get started, install it via `pip`:
```bash
pip install cortile
```

### Usage
If cortile is installed and running as described [here](https://github.com/leukipp/cortile?tab=readme-ov-file#installation-), the python bindings will connect to the running instance, allowing you to fully communicate with cortile using python:

```python
from cortile import Cortile

# connects to the running cortile instance
ct = Cortile()
...
```

## Documentation [![documentation](https://img.shields.io/badge/docstring-%20PEP%20257%20-yellow?style=flat-square)](#documentation-)
Documentation is provided through docstring literals, which appear immediately after the definition of a method, class, or module.
While all methods and classes include docstrings, the primary interface for interacting with a running cortile instance is the `Cortile()` class, which is documented here:

<details><summary>class Cortile()</summary><div>

<a id="cortile/cortile.Cortile.__init__"></a>

#### \_\_init\_\_

```python
def __init__(log: int = Logger.LEVELS.WARN)
```

Initialize the cortile connector.

This main class wraps methods of the base connector and should be
used as primary interface to communicate with a running cortile instance.

**Arguments**:

- `log`: Logging level, default is warn

<a id="cortile/cortile.Cortile.log"></a>

#### log

```python
@property
def log() -> Logger
```

Return the logger instance.

**Returns**:

Logger instance that writes to syslog

<a id="cortile/cortile.Cortile.listen"></a>

#### listen

```python
def listen(callback: Callable[[Dict], None] | None) -> None
```

Start listening for events.

**Arguments**:

- `callback`: Function to call when an event is received

<a id="cortile/cortile.Cortile.wait"></a>

#### wait

```python
def wait(sleep: float = 0.5) -> None
```

Keeps the process running for the connector to listen.

**Arguments**:

- `sleep`: Time to sleep in between, default is 0.5 seconds

<a id="cortile/cortile.Cortile.close"></a>

#### close

```python
def close() -> None
```

Close the connection gracefully.

<a id="cortile/cortile.Cortile.get_active_layout"></a>

#### get\_active\_layout

```python
def get_active_layout() -> Dict | None
```

Get the active layout for the current desktop and screen.

**Returns**:

Active layout with tiling enabled or None

<a id="cortile/cortile.Cortile.get_active_layouts"></a>

#### get\_active\_layouts

```python
def get_active_layouts() -> Iterator[Dict]
```

Get the active layouts from the workspaces.

**Returns**:

Iterator of active layouts with tiling enabled

<a id="cortile/cortile.Cortile.get_active_client"></a>

#### get\_active\_client

```python
def get_active_client() -> Dict | None
```

Get the current focused client window.

**Returns**:

Active client or None

<a id="cortile/cortile.Cortile.get_active_clients"></a>

#### get\_active\_clients

```python
def get_active_clients() -> Iterator[Dict]
```

Get information of clients on the current active screen.

**Returns**:

Iterator of tracked clients on the current screen

<a id="cortile/cortile.Cortile.get_active_workspace"></a>

#### get\_active\_workspace

```python
def get_active_workspace() -> int | None
```

Get the current active workspace.

**Returns**:

Active workspace index or None

<a id="cortile/cortile.Cortile.get_active_screen"></a>

#### get\_active\_screen

```python
def get_active_screen() -> int | None
```

Get the current active screen.

**Returns**:

Active screen index or None

<a id="cortile/cortile.Cortile.get_workspace_count"></a>

#### get\_workspace\_count

```python
def get_workspace_count() -> int | None
```

Get the number of workspaces.

**Returns**:

Number of workspaces or None

<a id="cortile/cortile.Cortile.get_screen_count"></a>

#### get\_screen\_count

```python
def get_screen_count() -> int | None
```

Get the number of screens.

**Returns**:

Number of screens or None

<a id="cortile/cortile.Cortile.get_workspace_dimensions"></a>

#### get\_workspace\_dimensions

```python
def get_workspace_dimensions() -> List[Dict]
```

Get the dimensions of all workspaces.

**Returns**:

LTR sorted list of workspace dimensions or None

<a id="cortile/cortile.Cortile.get_screen_dimensions"></a>

#### get\_screen\_dimensions

```python
def get_screen_dimensions() -> List[Dict]
```

Get the dimensions of all screens.

**Returns**:

LTR sorted list of screen dimensions or None

<a id="cortile/cortile.Cortile.get_clients"></a>

#### get\_clients

```python
def get_clients() -> List[Dict]
```

Get all the clients information.

**Returns**:

List of tracked clients or None

<a id="cortile/cortile.Cortile.get_windows"></a>

#### get\_windows

```python
def get_windows() -> Dict | None
```

Get all the windows information.

**Returns**:

List of tracked window ids or None

<a id="cortile/cortile.Cortile.desktop_switch"></a>

#### desktop\_switch

```python
def desktop_switch(desktop: int) -> bool
```

Switch to a different desktop.

**Arguments**:

- `desktop`: Index of the desktop to switch to

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.window_activate"></a>

#### window\_activate

```python
def window_activate(id: int) -> bool
```

Activate a window by its id.

**Arguments**:

- `id`: Id of the window to activate

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.window_to_desktop"></a>

#### window\_to\_desktop

```python
def window_to_desktop(id: int, desktop: int) -> bool
```

Move a window to a different desktop.

**Arguments**:

- `id`: Id of the window to move
- `desktop`: Index of the desktop to move the window to

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.window_to_position"></a>

#### window\_to\_position

```python
def window_to_position(id: int, x: int, y: int) -> bool
```

Move a window to a specific position.

**Arguments**:

- `id`: Id of the window to move
- `x`: X coordinate to move the window to
- `y`: Y coordinate to move the window to

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.window_to_screen"></a>

#### window\_to\_screen

```python
def window_to_screen(id: int, screen: int) -> bool
```

Move a window to a different screen.

**Arguments**:

- `id`: Id of the window to move
- `screen`: Index of the screen to move the window to

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_enable"></a>

#### action\_execute\_enable

```python
def action_execute_enable(desktop: int, screen: int) -> bool
```

Execute the 'enable' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_disable"></a>

#### action\_execute\_disable

```python
def action_execute_disable(desktop: int, screen: int) -> bool
```

Execute the 'disable' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_toggle"></a>

#### action\_execute\_toggle

```python
def action_execute_toggle(desktop: int, screen: int) -> bool
```

Execute the 'toggle' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_decoration"></a>

#### action\_execute\_decoration

```python
def action_execute_decoration(desktop: int, screen: int) -> bool
```

Execute the 'decoration' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_restore"></a>

#### action\_execute\_restore

```python
def action_execute_restore(desktop: int, screen: int) -> bool
```

Execute the 'restore' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_cycle_next"></a>

#### action\_execute\_cycle\_next

```python
def action_execute_cycle_next(desktop: int, screen: int) -> bool
```

Execute the 'cycle_next' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_cycle_previous"></a>

#### action\_execute\_cycle\_previous

```python
def action_execute_cycle_previous(desktop: int, screen: int) -> bool
```

Execute the 'cycle_previous' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_layout_vertical_left"></a>

#### action\_execute\_layout\_vertical\_left

```python
def action_execute_layout_vertical_left(desktop: int, screen: int) -> bool
```

Execute the 'layout_vertical_left' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_layout_vertical_right"></a>

#### action\_execute\_layout\_vertical\_right

```python
def action_execute_layout_vertical_right(desktop: int, screen: int) -> bool
```

Execute the 'layout_vertical_right' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_layout_horizontal_top"></a>

#### action\_execute\_layout\_horizontal\_top

```python
def action_execute_layout_horizontal_top(desktop: int, screen: int) -> bool
```

Execute the 'layout_horizontal_top' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_layout_horizontal_bottom"></a>

#### action\_execute\_layout\_horizontal\_bottom

```python
def action_execute_layout_horizontal_bottom(desktop: int, screen: int) -> bool
```

Execute the 'layout_horizontal_bottom' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_layout_maximized"></a>

#### action\_execute\_layout\_maximized

```python
def action_execute_layout_maximized(desktop: int, screen: int) -> bool
```

Execute the 'layout_maximized' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_layout_fullscreen"></a>

#### action\_execute\_layout\_fullscreen

```python
def action_execute_layout_fullscreen(desktop: int, screen: int) -> bool
```

Execute the 'layout_fullscreen' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_master_make"></a>

#### action\_execute\_master\_make

```python
def action_execute_master_make(desktop: int, screen: int) -> bool
```

Execute the 'master_make' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_master_make_next"></a>

#### action\_execute\_master\_make\_next

```python
def action_execute_master_make_next(desktop: int, screen: int) -> bool
```

Execute the 'master_make_next' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_master_make_previous"></a>

#### action\_execute\_master\_make\_previous

```python
def action_execute_master_make_previous(desktop: int, screen: int) -> bool
```

Execute the 'master_make_previous' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_master_increase"></a>

#### action\_execute\_master\_increase

```python
def action_execute_master_increase(desktop: int, screen: int) -> bool
```

Execute the 'master_increase' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_master_decrease"></a>

#### action\_execute\_master\_decrease

```python
def action_execute_master_decrease(desktop: int, screen: int) -> bool
```

Execute the 'master_decrease' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_slave_increase"></a>

#### action\_execute\_slave\_increase

```python
def action_execute_slave_increase(desktop: int, screen: int) -> bool
```

Execute the 'slave_increase' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_slave_decrease"></a>

#### action\_execute\_slave\_decrease

```python
def action_execute_slave_decrease(desktop: int, screen: int) -> bool
```

Execute the 'slave_decrease' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_proportion_increase"></a>

#### action\_execute\_proportion\_increase

```python
def action_execute_proportion_increase(desktop: int, screen: int) -> bool
```

Execute the 'proportion_increase' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_proportion_decrease"></a>

#### action\_execute\_proportion\_decrease

```python
def action_execute_proportion_decrease(desktop: int, screen: int) -> bool
```

Execute the 'proportion_decrease' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_window_next"></a>

#### action\_execute\_window\_next

```python
def action_execute_window_next(desktop: int, screen: int) -> bool
```

Execute the 'window_next' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_window_previous"></a>

#### action\_execute\_window\_previous

```python
def action_execute_window_previous(desktop: int, screen: int) -> bool
```

Execute the 'window_previous' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

<a id="cortile/cortile.Cortile.action_execute_reset"></a>

#### action\_execute\_reset

```python
def action_execute_reset(desktop: int, screen: int) -> bool
```

Execute the 'reset' action.

**Arguments**:

- `desktop`: Index of the desktop
- `screen`: Index of the screen

**Returns**:

True if successful, False otherwise

</div></details>

## Examples [![examples](https://img.shields.io/badge/scripts-%20Examples%20-blue?style=flat-square)](#examples-)
To help you get started quickly, example scripts are available in the [examples](https://github.com/leukipp/cortile-addons/tree/main/examples) folder.

These scripts demonstrate various use cases and can serve as a practical guide to utilizing the full potential of cortile through python.
Feel free to explore these resources to make the most out of your cortile setup.

## Integrating [![integrating](https://img.shields.io/github/go-mod/go-version/leukipp/cortile?label=go&style=flat-square)](#integrating-)
You can execute a script on demand or trigger it by any other external means.
To ensure a script is activated every time cortile starts, place it in a folder named addons within the cortile configuration directory, e.g. `~/.config/cortile/addons/`.

Any executable script (`chmod +x script_name.py`) in this folder will automatically run when cortile starts.
The script will execute with the same user permission and environment as cortile, so python and additional required dependencies (`pip packages`) must be available in this environment.

Any output from python’s `print()` function or error logs within the script will appear in the terminal where cortile is running. Depending on the log level, additional log messages from the script will be written to the system log (`cat /var/log/syslog`).

### Compatibility
Since the python integration relies on internal cortile properties and the provided interfaces via dbus, it’s crucial that all custom scripts are compatible with the running cortile instance.

This table provides the officially supported combination of versions:
| Addons (Python) | Cortile (go) |
| --------------- | ------------ |
| v1.0.0          | v2.5.1       |

## Contributing [![contributing](https://img.shields.io/github/issues-pr-closed/leukipp/cortile-addons?style=flat-square)](#contributing-)
Contributions into the [examples](https://github.com/leukipp/cortile-addons/tree/main/examples) folder are greatly welcomed!

If you have a script that could benefit the community, please submit a pull request.
Include a brief explanation of the script in the header comment (refer to existing files for guidance).
The script should be runnable or serve at least as a useful skeleton for others.

## License [![license](https://img.shields.io/github/license/leukipp/cortile-addons?style=flat-square)](#license-)
[MIT](https://github.com/leukipp/cortile-addons/blob/main/LICENSE)
