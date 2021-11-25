![bonfire](bonfire.jpg)

# bonfire
Save and restore snapshots of your computer's application state.

## What is
Do you often find yourself opening the same set of apps everyday to get your day started? Are you ever in the middle of working on a project, you have your code editor open, a million chrome tabs plus your software and realize you need to close it all and switch contexts but don't want to lose everything you had open?

Look no further than _bonfire_! _Bonfire_ allows you to set restoration checkpoints, keeping track of which apps you had open and what you were working on so that you can easily re-open them and continue working without hassle.

Whitelist which applications you want _bonfire_ to track, rename your bonfire restore points and create custom keybindings to speed up your workflow. 

## How to
```shell
Usage: bonfire [OPTIONS] COMMAND [ARGS]...

Options:
  -q, --quiet    Silence the output
  -v, --verbose  Make the output verbose
  --help         Show this message and exit.

Commands:
  extinguish  Extinguish a bonfire, deleting the save point
  light       Light a bonfire saving application state
  list        List lit bonfires
  rename      Rename a bonfire
  restore     Restore application state to a bonfire save point
```

## License
See [LICENSE](LICENSE)

Made as part of McMaster Computer Science Society Hacktober 2021.


