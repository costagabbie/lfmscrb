# costagabbie's last.fm scrobbler
Last.fm simple python scrobbler using pylast

# Dependencies
For lfmscrb.py : 
  `colorama`  : https://pypi.org/project/colorama/
  `pylast`    : https://pypi.org/project/pylast/
For tlbuilder.py :
  `tinytag`   : https://pypi.org/project/tinytag/

# Setup
You will need to insert your last.fm API KEY and API SECRET in the code of lfmscrn.py, also your username and password.
# Usage
lfmscrb.py    : execute it and it will open the file `tracklist.csv` in its directory and pretend to play the song and scrobble it to last.fm
You can use the `-s` flag to make it play only enough of the song to be classified as an valid scrobble accordingly to the documentation of last.fm API(https://www.last.fm/api/scrobbling).
tlbuilder.py  : it will open a pathlist.txt file in its directory and this file should contain one folder per line, these folder must contain audio files with IDv3 flags, the program will extract the info and create a `tracklist.csv` file for use with `lfmscrb.py`.
# Disclaimer
I'm not responsible for whatever happens to your Last.fm account, i don't know if they will ban, but judging how many k-pop scrobbles some individuals have, i may assume that it wasn't scrobbled in a legit way.
