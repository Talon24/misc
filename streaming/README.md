# Music displayer

This program ready the currently played song and writes it to a file that can be watched via streamlabs or obs.

## Requirements

* A file called `licenses.txt` - This should contain all the incompetech licenses. Replace and expand the example.
* A file called `music.txt` - This is the file that should be watched by the streaming software. It will be generated if not already there.
* Python - to run the script

## Currently Supported Players

* Winamp
* Foobar

### Winamp

Winamp is the default mode. It works without a config file or when defined in the config file

```
player=winamp
```

### Foobar2000
For use with foobar, you have to change the player in the config file and you have to set the `foobar title` value.

```
player=foobar
foobar title=<copy-paste here>
```

For `foobar title`, you need to specify how the window title for your Foobar2000 is generated. If you didn't change it, the default is already preset in the example config file. You can look up your settings in Foobar under

`File` -> `Preferences` -> `Display` -> `Default User Interface`

then copy the `Window title` field into the config file.

## Hints
Be sure that the mp3 tags in the file match the title in the license text, so the title that your player displays ca be mapped to the correct license.
