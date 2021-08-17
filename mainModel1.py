from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter import *
from tkinter.filedialog import askopenfilename
import json #invite jason
import configparser
from configparser import ConfigParser
import shutil
from pypresence import Presence
import os
from tinytag import TinyTag
# Variables --------------------------------------------------------------------
print("loading gui...")

config = ConfigParser()

version = "2021.3.17"
window_width = "1024"
window_height = "768"
label_height = 11

GREY = "#202020"
DARK_GRAY = "#3c3836"
WHITE = "#fbf1c7"
GREEN = "#98971a"
LIGHT_GREEN = "#b8bb26"
RED = "#cc241d"
LIGHT_RED = "#fb4934"
BLUE = "#458588"
LIGHT_BLUE = "#83a598"
YELLOW = "#d79921"
LIGHT_YELLOW = "#fabd2f"
AQAU = "#689d6a"
LIGHT_AQUA = "#8ec07c"
PURPLE = "#b16286"
LIGHT_PURPLE = "#d3869b"
"""
#RPC
client_id = '811576313688621088'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop
RPC.update(state="Converting songs", details="BeatSaber to ADHS*MASTER converter",large_image="avatar",buttons=[{"label": "GitHub", "url": "https://github.com/sa-koitchio/beatsaber-to-adhs"}])
"""
#no sus. amogus

notesLeft=[]       #type 0
notesMidLeft=[]    #type 1
notesMidRight=[]   #type 2
notesRight=[]      #type 3

baseFolder = ""
BPM = 0
BPS = 0
lengthOfBeat = 0
infofile = ""
tag = ""
songLength = 0
jsongName = ""
jartistName = ""
# Window settings --------------------------------------------------------------
window = Tk()
window.title("beatsaber-to-adhs {}".format(version))
window.geometry("{}x{}".format(window_width, window_height))
window.configure(bg=GREY)
window.option_add('*Font', 'Consolas 15')


# Functions --------------------------------------------------------------------
def openFile():
    # Check  for input metadata

    if inputName.get() == "":
        #hasen't been set.
        labelName.configure(background=RED)
        inputName.configure(background=LIGHT_RED)
        editLabel("Please input a song name and artist.")
    else:
        labelName.configure(background=BLUE)
        inputName.configure(background=LIGHT_BLUE)

    if inputArtist.get() == "":
        #hasen't been set.
        labelArtist.configure(background=RED)
        inputArtist.configure(background=LIGHT_RED)
        editLabel("Please input a song name and artist.")
    else:
        labelArtist.configure(background=BLUE)
        inputArtist.configure(background=LIGHT_BLUE)

    if inputBPM.get() == 0:
        #hasen't been set.
        inputBPM.configure(background=RED)
        inputBPM.configure(background=LIGHT_RED)
        editLabel("Please input BPM")
    else:
        inputBPM.configure(background=BLUE)
        inputBPM.configure(background=LIGHT_BLUE)



    try:
        filename = askopenfilename() # Show an "Open" dialog box and return the path to the selected file
        editLabel("Opened "+filename)
        # Open the jason
        with open(filename, "r") as myfile:
            levelData = myfile.read()
    except:
        editLabel("Error while loading file.")
        return

    #read bs folder
    baseFolder = os.path.normpath(filename + os.sep + os.pardir)

    print(baseFolder)
    #open info.dat
    try:

        if os.path.isfile(baseFolder+ os.sep+'info.dat'):
            infofile = open(baseFolder+os.sep+'info.dat')

        elif os.path.isfile(baseFolder+ os.sep+'Info.dat'):
            infofile = open(baseFolder+os.sep+'Info.dat')

        jsondata = json.load(infofile)

        BPM = jsondata["_beatsPerMinute"]
        jsongName = jsondata["_songName"]
        jartistName = jsondata["_songAuthorName"]

        # open song file and try to read length.

        if os.path.isfile(baseFolder+ os.sep+'song.ogg'):
            tag = TinyTag.get(baseFolder+ os.sep+'song.ogg')
            songLength = tag.duration
            songLength = round( tag.duration + 5)

        elif os.path.isfile(baseFolder+ os.sep+'song.egg'):
            tag = TinyTag.get(baseFolder+ os.sep+'song.egg')
            songLength = round( tag.duration + 5)




        print("BPM: "+ str(BPM))
        print("Song name: "+ str(jsongName))
        print("Artist: "+str(jartistName))
        print("Duration: "+str(songLength))

        #Calculate BPS

    except:
        BPM = inputBPM.get()
        editLabel("Error while loading info file.")
        songLength = inputSongLen.get()

    BPS = int(BPM)/60
    lengthOfBeat = 1/BPS


    # Get JASON from data
    try:
        levelObj = json.loads(levelData)
        editLabel("Loaded level data.")
    except:
        editLabel("File is no json.")
        return

    notesArray = levelObj["_notes"]
    noteCount = len(notesArray)

    # Iterate through the notesArray
    for note in notesArray:
        type = note["_lineIndex"]
        time = note["_time"]

        if type == 0:
            #far left:
            addTime = calcAddTime(time,lengthOfBeat)
            if not addTime in notesLeft:
                notesLeft.append(addTime)
            continue

        elif type == 1:
            #middle left:
            addTime = calcAddTime(time,lengthOfBeat)
            if not addTime in notesMidRight:
                notesMidRight.append(addTime)
            continue

        elif type == 2:
            #middle right:
            addTime = calcAddTime(time,lengthOfBeat)
            if not addTime in notesMidRight:
                notesMidRight.append(addTime)
            continue

        elif type == 3:
            #far right
            addTime = calcAddTime(time,lengthOfBeat)
            if not addTime in notesRight:
                notesRight.append(addTime)
            continue

        else:
            #Jibberish
            editLabel("Janky note position!")

    editLabel("Finished iterating.")


    if jsongName == "":
        jsongName = inputName.get()

    if jartistName == "":
        jartistName = inputArtist.get()

    # Add a new section and some values
    config.add_section('Map')
    config.set('Map', 'songName', str(jsongName))
    config.set('Map', 'songArtist', str(jartistName))
    config.set('Map', 'leftNotes', str(notesLeft))
    config.set('Map', 'upNotes', str(notesMidRight))
    config.set('Map', 'rightNotes', str(notesRight))
    config.set('Map', 'noteMoveSpeed', str(inputNoteSpeed.get()))
    config.set('Map', 'songLength', str(songLength))
    config.set('Map', 'converted',str(1))
    #config.set('Map', 'notesRight', str(notesRight))

    # Save to a file
    outputfile = "map.ini"
    try:
        with open(baseFolder+os.sep+outputfile, 'w') as configfile:
            config.write(configfile)
        editLabel("Finished writing song.")


    except:
        editLabel("Could not write file.")
        return

    jsongName = ""
    jartistName = ""
    BPM = 0
    BPS = 0
    lengthOfBeat = 0
    baseFolder = ""


def calcAddTime(_time,_lob):
    calcTime = _time*_lob
    calcTime = round(calcTime*60)
    return calcTime;

# Edit Label
def editLabel(status):
    text_len = len(textBox.cget("text").rstrip().split("\n"))
    if text_len > label_height:
        text = "\n".join(textBox.cget("text").rstrip().split("\n")[1:])
        textBox.configure(text="{}\n{}".format(text, status))
    else:
        textBox.configure(text="{}\n{}".format(textBox.cget("text").rstrip(), status))


# Window contents --------------------------------------------------------------
info = Label(text="BeatSaber to ADHS",
                width=window_width,
                height="3",
                background=GREY,
                foreground=WHITE,
                cursor = "pirate")


buttonLoad = Button(text="Open BeatSaber file and convert",
                    width=window_width,
                    height="3",
                    background=GREEN,
                    activebackground=GREEN,
                    foreground=WHITE,
                    activeforeground=WHITE,
                    bd=0,
                    command=openFile)


textBox = Label(text="Status messages will appear here",
                width=window_width,
                background=GREY,
                foreground=WHITE)


labelName = Label(text="Input song name:",
                width=window_width,
                height="2",
                background=BLUE,
                foreground=WHITE)


inputName = Entry(width=window_width,
                background=LIGHT_BLUE,
                foreground=WHITE,
                selectbackground=RED,
                relief=FLAT,
                justify=CENTER)


labelArtist = Label(text="Input artist name:",
                width=window_width,
                height="2",
                background=BLUE,
                foreground=WHITE)


inputArtist = Entry(width=window_width,
                background=LIGHT_BLUE,
                foreground=WHITE,
                selectbackground=RED,
                relief=FLAT,
                justify=CENTER)

labelBPM = Label(text="Input BPM:",
                width=window_width,
                height="2",
                background=BLUE,
                foreground=WHITE)


inputBPM = Entry(width=window_width,
                background=LIGHT_BLUE,
                foreground=WHITE,
                selectbackground=RED,
                relief=FLAT,
                justify=CENTER)



labelSongLen = Label(text="Input song length (seconds):",
                width=window_width,
                height="2",
                background=BLUE,
                foreground=WHITE)


inputSongLen = Entry(width=window_width,
                background=LIGHT_BLUE,
                foreground=WHITE,
                selectbackground=RED,
                relief=FLAT,
                justify=CENTER)


labelNoteSpeed = Label(text="Input note speed:",
                width=window_width,
                height="2",
                background=BLUE,
                foreground=WHITE)


inputNoteSpeed = Entry(width=window_width,
                background=LIGHT_BLUE,
                foreground=WHITE,
                selectbackground=RED,
                relief=FLAT,
                justify=CENTER)

# Pack all contents to window --------------------------------------------------
info.pack()
#get song name
labelName.pack()
inputName.pack()
#get artist
labelArtist.pack()
inputArtist.pack()

labelBPM.pack()
inputBPM.pack()

labelSongLen.pack()
inputSongLen.pack()

labelNoteSpeed.pack()
inputNoteSpeed.pack()
#convert Button
buttonLoad.pack()
#log
textBox.pack()

# Run program ------------------------------------------------------------------
window.mainloop()
