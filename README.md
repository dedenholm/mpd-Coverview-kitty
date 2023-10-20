# mpd-Coverview-kitty
fetches coverart for current playing mpd song and displays it in kitty terminal.

written in python.

## Features

- using idle until player state change feature, enables low cpu usage.
- fetches album art first from folder.jpeg, cover.png, etc, if none is found it uses mutagen to look for embedded cover art, if all else fails it displays a fallback coverart.
- no fetching album art from online databases, as ive never experienced a reliable implementation of that.
## Installation
- download Coverview folder to a location of your choosing
- edit `/path/to/mpd/music/library` in coverview_x.x.py
- edit `/location/of/coverview/.aartminip.png` and `/location/of/coverview/.placeholder.png` to reflect your install location
## Usage

launch with python in kitty

`kitty python /path/to/coverview_0.9.1.py`


## Acknowledgements
this project startet with hacking off the album art display portion of 
[Miniplayer](https://github.com/GuardKenzie/miniplayer/tree/main), with significant modifications. 

## Dependencies

kitty

python 3

python-pixcat-git

python-mpd2

python-pillow
