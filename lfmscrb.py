#!/bin/python3

#     This file is part of "costagabbie's last.fm scrobbler".
#     This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
import os
import csv
import pylast
import time
import argparse
from math import floor
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

def main():
    #Check if the spam switch is present
    print(f"[INFO] Starting scrobbler at {datetime.utcnow()}")
    parser = argparse.ArgumentParser(description="costagabbie's last.fm scrobbler v:1.1")
    parser.add_argument('-s', '--spam', action= 'store_true',dest='spam', help='Wait just long enough to have a valid scrobble.',default=False)
    parser.add_argument('-p', '--playlist', dest='playlist', help='playlist file in csv format.',default='tracklist.csv', type=str)
    parser.add_argument('-l', '--loop', dest='loop', help='how many time the playlist should be looped, 0 means infinite.',default=0, type=int)
    args= parser.parse_args()
    iterCount = 0
    print(f"[INFO] Trying to open {args.playlist}.")
    #Opening the tracklist
    
    while(True):
        print(f"[Info] Iteration {iterCount+1} starting at {datetime.utcnow()}")    
        # Going through each song entry in the tracklist
        if os.path.exists(args.playlist):
            csv_file = open('tracklist.csv', 'r') 
            reader = csv.reader(csv_file,delimiter=';')
        else:
            print(f"[ERROR] Cannot find the file {args.playlist}")
            exit()
        for row in reader:
            # If the song is less than 30 seconds it don't count as scrobble so we go to the next song
            if int(row[3]) < 30:
                print(f"[WARNING]{row[0]}={row[1]} is shorter than 30 seconds({row[3]} seconds), so it can't be scrobbled!")
                continue
            # Get the time that we started to play the song
            timestamp = time.time()
            # Prepare for sending a Now Playing request
            network.get_user(username)
            if args.spam:
                # If we are in spam mode, we should wait for at least half of the song length to scrobble
                print(f"[INFO] Now Playing {row[0]} - {row[1]} (Album: {row[2]}) at {datetime.utcnow()}")
                # Sending the now playing request
                network.update_now_playing(row[1],row[0],row[2])
                print(f"[INFO] Waiting for {str(floor(int(row[3])/2)+1)} seconds to scrobble.")
                # Waiting for half of the song + 1 second
                time.sleep(floor(int(row[3])/2)+1)
            else:
                # We are not in spam mode so we wait the full length of the song before scrobble
                print(f"[INFO] Now Playing {row[0]} - {row[1]} (Album: {row[2]})")
                network.update_now_playing(row[1],row[0],row[2])
                print(f"[INFO] Waiting for {row[3]} seconds to scrobble.")
                time.sleep(int(row[3]))
            # Now that we 'listened' to the song (or at least half of it on spam mode) we can scrobble
            print(f"[INFO] Trying to scrobble {row[0]} - {row[1]} (Album: {row[2]}) at{str(timestamp)}")
            network.scrobble(artist=row[1], title=row[0], timestamp=timestamp,album=row[2])
        iterCount = iterCount +1
        # If we are in a non-infinite mode and the iteration count is enough
        if (args.loop > 0) and (iterCount >= args.loop):
            # We played everything so bye bye.    
            print("All done, exiting now.")
            exit()
if __name__ == '__main__':  
    main()
