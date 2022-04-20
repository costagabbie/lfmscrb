#!/usr/bin/env python3

#Imports
from tinytag import TinyTag
from datetime import datetime
import sys
import os
import fnmatch

pathlistfile = "pathlist.txt"
destfilename = "tracklist.csv"
pathlist = open(pathlistfile,"r")
csv_file = open(destfilename, 'w')
allowedext = ['.mp3','.m4a','.ogg','.mp4','.flac','.alac']

print("Python Scrobbler tracklist builder v: 1.0.0.0\n")
def main():
    print("Iterating through the songs path list.\n")
    with open(pathlistfile,"r") as openfileobject:
        for f in openfileobject:
            print("Reading directory files.\n")
            fname = f[:-1]
            items = os.listdir(fname)
            for name in items:
                aux = os.path.splitext(name)
                if aux[1] in allowedext:
                    print("Reading file "+name+"\n")
                    tag = TinyTag.get(fname+'/'+name)
                    print("Adding "+name+"("+tag.artist+"/"+tag.album+") to the list.\n")
                    csv_file.write(tag.title+";"+tag.artist+";"+tag.album+";"+str(int(tag.duration))+"\n")
                else:
                    print(name+" skipped from the list(not on allowed extensions).\n")
            print(f+" is done.\n")
        print("Everything done.\n")
    csv_file.close

if __name__ == '__main__':
    main()
