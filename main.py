from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter import *
from tkinter.filedialog import askopenfilename
import json #invite jason
import configparser
from configparser import ConfigParser

# Variables --------------------------------------------------------------------
config = ConfigParser()

version = "2021.3.17"
window_width = "600"
window_height = "600"
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



#no sus. amogus

notesLeft=[]       #type 0
notesMidLeft=[]    #type 1
notesMidRight=[]   #type 2
notesRight=[]      #type 3


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


    if inputName.get() == "" or inputArtist.get() == "":
        return

    try:
        filename = askopenfilename() # Show an "Open" dialog box and return the path to the selected file
        editLabel("Opened "+filename)
        # Open the jason
        with open(filename, "r") as myfile:
            levelData = myfile.read()
    except:
        editLabel("Error while loading file.")
        return

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
            notesLeft.append(round(time*1000))
            continue

        elif type == 1:
            #middle left:
            notesMidLeft.append(round(time*1000))
            continue

        elif type == 2:
            #middle right:
            notesMidRight.append(round(time*1000))
            continue

        elif type == 3:
            #far right
            notesRight.append(round(time*1000))
            continue

        else:
            #Jibberish
            editLabel("Janky note position!")

    editLabel("Finished iterating.")

    # Add a new section and some values
    config.add_section('Map')
    config.set('Map', 'songName', str(inputName.get()))
    config.set('Map', 'songArtist', str(inputArtist.get()))
    config.set('Map', 'notesLeft', str(notesLeft))
    config.set('Map', 'notesMidLeft', str(notesMidLeft))
    config.set('Map', 'notesMidRight', str(notesMidRight))
    config.set('Map', 'notesRight', str(notesRight))

    # Save to a file
    try:
        with open('map.ini', 'w') as configfile:
            config.write(configfile)
        editLabel("Finished writing song.")
    except:
        editLabel("Could not write file.")
        return





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


buttonLoad = Button(text="Open file and convert",
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


# Pack all contents to window --------------------------------------------------
info.pack()
#get song name
labelName.pack()
inputName.pack()
#get artist
labelArtist.pack()
inputArtist.pack()

#convert Button
buttonLoad.pack()
#log
textBox.pack()

# Run program ------------------------------------------------------------------
window.mainloop()
