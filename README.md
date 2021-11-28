![bonfire](bonfire.jpg)

# bonfire
Tiny CLI tool to save and restore snapshots of your computer's application state.

## Motivation
Do you often find yourself opening the same set of apps everyday to get your day started? Are you ever in the middle of working on a project, you have your code editor open, a million chrome tabs plus your software and realize you need to close it all and switch contexts but don't want to lose everything you had open?

Look no further than _bonfire_! _Bonfire_ allows you to set restoration checkpoints, keeping track of which apps you had open and what you were working on so that you can easily re-open them and continue working without hassle.

Whitelist which applications you want _bonfire_ to track, rename your bonfire restore points and create custom keybindings to speed up your workflow. 

## Getting Started
_Bonfire_ is built with [Python](https://www.python.org/) so you'll need [python 3.6+](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/).
Next clone the repo:
```
git clone https://github.com/benjaminkostiuk/bonfire
```

### Installation
If you want to install the _bonfire_ CLI in a virtual environment you can use Python [venv](https://docs.python.org/3/library/venv.html). 
```
mkdir venv
python -m venv venv
venv\Scripts\activate.bat
```
To install the _bonfire_ CLI from the root of the repository run:
```
pip install .
```

### Usage
```shell
Usage: bonfire [OPTIONS] COMMAND [ARGS]...

Options:
  -q, --quiet    Silence the output
  -v, --verbose  Make the output verbose
  --help         Show this message and exit.

Commands:
  extinguish  Extinguish a bonfire, deleting the save point.
  light       Light a bonfire saving application state.
  list        List lit bonfires.
  rename      Rename a bonfire.
  restore     Restore to a bonfire save point.
```
### Commands
#### Light
```
Usage: bonfire light [NICKNAME]
```
Light a bonfire to save the current application state. Bonfire will only track those processes you have whitelisted in your configuration.
Optionally, you can also give the bonfire a nickname.

#### List
```
Usage: bonfire list
```
List all lit bonfires, along with their creation timestamp, id, nickname and a short list of the applications they are keeping track of.

#### Rename
```
Usage: bonfire rename ID NICKNAME
```
Rename a lit bonfire, or provide an unamed bonfire a nickname. You do so by specifying the id of the bonfire you want to nickname or rename.

#### Restore
```
Usage: bonfire restore [OPTIONS] ID

Options:
  -n, --use-name  Use the bonfire nickname instead of the id
```
Restore to a bonfire save point, repening all application state saved by that bonfire. You can either specify the bonfire by id or nickname with the `-n` flag.

#### Extinguish
```
Usage: bonfire extinguish [IDS]...
```
Extinguish one or more bonfires, deleting their save points. You can specify which bonfires to delete by their ids.

### Configuration
Configure the application whitelist and other options in [config.json](./store/config.json).

## License
See [LICENSE](LICENSE)

Made as part of McMaster Computer Science Society Hack-vember 2021.


