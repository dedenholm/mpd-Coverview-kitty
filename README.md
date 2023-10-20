# mpd-Coverview-kitty
Fetches coverart for current playing mpd song and displays it in kitty terminal.

Written in python.

## Features

- using idle-until-player-state-change feature, enables low cpu usage.
- fetches album art first from folder.jpeg, cover.png, etc, if none is found it uses mutagen to look for embedded cover art, if all else fails it displays a fallback image
- no fetching album art from online databases, as ive never experienced a reliable implementation of that.
## Installation
- install all dependencies, using pip or your package manager of choice
- download Coverview folder to a location of your choosing
- edit `/path/to/mpd/music/library` in coverview_x.x.py
- edit `/location/of/coverview/.aartminip.png` and `/location/of/coverview/.placeholder.png` to reflect your install location

## Usage

launch with python in kitty

`kitty python /path/to/coverview_0.9.1.py`

you can either create your own .desktop file for launching with rofi, or use a keybinding for launching it

## Acknowledgements

this project started with hacking off the album art display portion of 
[Miniplayer](https://github.com/GuardKenzie/miniplayer/tree/main), with significant modifications. 


## Dependencies
mpd

kitty

python 3

python-mutagen

python-pixcat-git

python-mpd2

python-pillow

## Screenshots

![alt text](https://github.com/dedenholm/mpd-Coverview-kitty/blob/main/Screenshots/Screenshot_3.png "suggested usage")
![alt text](https://github.com/dedenholm/mpd-Coverview-kitty/blob/main/Screenshots/Screenshot_4.png "suggested usage")
![alt text](https://github.com/dedenholm/mpd-Coverview-kitty/blob/main/Screenshots/Screenshot_2.png "only the program")
