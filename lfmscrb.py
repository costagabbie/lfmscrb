#!/bin/python3

#     This file is part of "costagabbie's last.fm scrobbler".
#     This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 


import csv
import pylast
import time
from math import floor
from colorama import init, Fore, Back, Style
from datetime import datetime

API_KEY="REPLACE WITH YOUR API KEY" 
API_SECRET="REPLACE WITH YOUR API SECRET"
username = "REPLACE WITH YOUR USERNAME"
password_hash = pylast.md5("REPLACE WITH YOUR PASSWORD")
network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

#
# CSV FILE(trackinfo.csv) FIELDS
#  0      1     2      3
# title,artist,album,length in seconds
#

init(autoreset=True)
print(Style.BRIGHT + Back.BLACK + Fore.CYAN+"costagabbie's Last.fm Auto Scrobbler version 1.0.0.0\n")

def main():
    #Check if the spam switch is present
    if sys.argv[1] == "-s":
        spam = True
        print(Style.BRIGHT + Back,BLACK + Fore.RED+"Starting in spam mode, scrobbles will be done as fast as possible!\n")
    else:
        spam : False
    print(Style.BRIGHT + Back.BLACK + Fore.CYAN+"[INFO]"+Style.BRIGHT + Back.BLACK + Fore.WHITE+"Trying to open trackinfo.csv.\n")
    #Opening the tracklist
    csv_file = open('tracklist.csv', 'r') 
    reader = csv.reader(csv_file,delimiter=';')
    # Going through each song entry in the tracklist
    for row in reader:
        # If the song is less than 30 seconds it don't count as scrobble so we go to the next song
        if row[3] < 30:
            print(Style.BRIGHT + Back,BLACK + Fore.YELLOW + "[WARNING] This song is shorter than 30 seconds, so it can't be scrobbled! \n")
            continue
        # Get the time that we started to play the song
        timestamp = time.time()
        # Prepare for sending a Now Playing request
        lastfm_user = network.get_user(username)
        if spam:
            # If we are in spam mode, we should wait for at least half of the song length to scrobble
            print(Style.BRIGHT + Back.BLACK + Fore.GREEN+"[INFO]"+Fore.WHITE+'Now Playing '+row[0]+'-'+row[1]+'(Album: '+row[2]+')')
            # Sending the now playing request
            network.update_now_playing(row[1],row[0],row[2])
            print(Style.BRIGHT + Back.BLACK + "[INFO]"+Style.BRIGHT + Back.BLACK + Fore.WHITE+"Waiting for half of "+row[3]+" seconds to scrobble.\n")
            # Waiting for half of the song + 1 second
            time.sleep(floor(int(row[3])/2)+1)
        else:
            # We are not in spam mode so we wait the full length of the song before scrobble
            print(Style.BRIGHT + Back.BLACK + Fore.GREEN+"[INFO]"+Fore.WHITE+'Now Playing '+row[0]+'-'+row[1]+'(Album: '+row[2]+')')
            network.update_now_playing(row[1],row[0],row[2])
            print(Style.BRIGHT + Back.BLACK + "[INFO]"+Style.BRIGHT + Back.BLACK + Fore.WHITE+"Waiting for "+row[3]+" seconds to scrobble.\n")
            time.sleep(int(row[3]))
        # Now that we 'listened' to the song (or at least half of it on spam mode) we can scrobble
        print(Style.BRIGHT + Back.BLACK + Fore.CYAN+"[INFO]"+Style.BRIGHT + Back.BLACK + Fore.WHITE+"Trying to scrobble "+title+"-"+artist+"("+row[2]+") at "+str(timestamp)+".\n")
        network.scrobble(artist=row[1], title=row[0], timestamp=timestamp,album=row[2])
    # We played the whole tracklist so bye bye.
    print(Style.BRIGHT + Back.BLACK + Fore.CYAN+"[INFO]"+Style.BRIGHT + Back.BLACK + Fore.WHITE+"All done, exiting now. \n")
if __name__ == '__main__':  
    main()
