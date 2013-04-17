# python 2.7
import eyed3
import os
import sys
import argparse

parser = argparse.ArgumentParser ()
parser.add_argument("-m", "--modify", action="store_true")
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument("-f", "--file")
action.add_argument("-d", "--directory")
args = parser.parse_args()

def ProcessFile (file, modify):
    try:
        audiofile = eyed3.load(file)
        print ("Artist=[%s],Album=[%s],Title=[%s]" % (audiofile.tag.artist, audiofile.tag.album, audiofile.tag.title))
        if (modify):
            (audiofile.tag.title, audiofile.tag.artist) = (audiofile.tag.artist, audiofile.tag.album)
            audiofile.tag.save()
    except Exception as e:
        print ("Error opening file %s" % file)
        print ("Exception was %s" % e)

if (args.file != None):
    ProcessFile (args.file, args.modify)
else:
    for file in os.listdir (args.directory):
        ProcessFile ("%s\\%s" % (args.directory, file), args.modify)

