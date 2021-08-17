import os
import shutil
import configparser
from configparser import ConfigParser
import json #invite jason
from tinytag import TinyTag

config = ConfigParser()
rootdir = 'C:\\Users\\kooba\\OneDrive\\Dokumente\\dataDumper'

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

def calcAddTime(_time,_lob):
    calcTime = _time*_lob
    calcTime = round(calcTime*60)
    return calcTime;

def findMapfile(baseFolder):
    mapAlreadyFound = False
    foundMapFile = ""
    if os.path.isfile(baseFolder+ os.sep +"ExpertStandard.dat") or os.path.isfile(baseFolder+ os.sep +"Expert.dat") :
        mapAlreadyFound = True
        if os.path.isfile(baseFolder+ os.sep +"ExpertStandard.dat"):
            foundMapFile = "ExpertStandard.dat"
        elif os.path.isfile(baseFolder+ os.sep +"Expert.dat"):
            foundMapFile = "Expert.dat"

    if os.path.isfile(baseFolder+ os.sep +"HardStandard.dat") or  os.path.isfile(baseFolder+ os.sep +"Hard.dat") and mapAlreadyFound == False:
        mapAlreadyFound = True
        if os.path.isfile(baseFolder+ os.sep +"HardStandard.dat"):
            foundMapFile = "HardStandard.dat"
        elif os.path.isfile(baseFolder+ os.sep +"Hard.dat"):
            foundMapFile = "Hard.dat"

    if os.path.isfile(baseFolder+ os.sep +"ExpertPlusStandard.dat") or os.path.isfile(baseFolder+ os.sep +"ExpertPlus.dat") and mapAlreadyFound == False:
        mapAlreadyFound = True
        if os.path.isfile(baseFolder+ os.sep +"ExpertPlusStandard.dat"):
            foundMapFile = "ExpertPlusStandard.dat"
        elif os.path.isfile(baseFolder+ os.sep +"ExpertPlus.dat"):
            foundMapFile = "ExpertPlus.dat"

    if os.path.isfile(baseFolder+ os.sep +"NormalStandard.dat") or os.path.isfile(baseFolder+ os.sep +"Normal.dat") and mapAlreadyFound == False:
        mapAlreadyFound = True
        if os.path.isfile(baseFolder+ os.sep +"NormalStandard.dat"):
            foundMapFile = "NormalStandard.dat"
        elif os.path.isfile(baseFolder+ os.sep +"Normal.dat"):
            foundMapFile = "Normal.dat"

    if os.path.isfile(baseFolder+ os.sep +"EasyStandard.dat") or os.path.isfile(baseFolder+ os.sep +"Easy.dat") and mapAlreadyFound == False:
        mapAlreadyFound = True
        if os.path.isfile(baseFolder+ os.sep +"EasyStandard.dat"):
            foundMapFile = "EasyStandard.dat"
        elif os.path.isfile(baseFolder+ os.sep +"Easy.dat"):
            foundMapFile = "Easy.dat"


    print("<< Mapfile "+ foundMapFile)
    return foundMapFile

def handleSongFile(file):
    if file.endswith(".ogg"):                                                           # load ogg
        tag = TinyTag.get(baseFolder+ os.sep+file)
        songLength = tag.duration
        songLength = round( tag.duration + 5)

    elif file.endswith(".egg"):                                                         # Rename egg to ogg
        tag = TinyTag.get(baseFolder+ os.sep+file)
        songLength = round( tag.duration + 5)
    
    try:
        os.rename(baseFolder+ os.sep+file,baseFolder+ os.sep+'song.ogg')
    except:
        print("Couldn't rename "+baseFolder+ os.sep+file)

    if (file.endswith(".jpg") and not os.path.isfile(baseFolder+ os.sep+'cover.jpg')):  # Rename cover
        try:
            os.rename(baseFolder+ os.sep+file,baseFolder+ os.sep+'cover.jpg')
        except:
            print("Couldnt rename cover.")
    return songLength

for baseFolder, dirs, files in os.walk(rootdir):
    mapAlreadyFound = False   
    foundMapFile = ""
    
    foundMapFile = findMapfile(baseFolder)

    notesLeft=[]       #type 0
    notesMidLeft=[]    #type 1
    notesMidRight=[]   #type 2
    notesRight=[]      #type 3


    for file in files: 
        completepath = os.path.join(baseFolder,file)
        infofile = ""
        print(baseFolder)
        
        

        if file.endswith("info.dat") or file.endswith("Info.dat"):                                                           # Load info.dat
            
            __file = open(os.path.join(baseFolder,file))
            jsondata = json.load(__file)
            BPM = jsondata["_beatsPerMinute"]
            jsongName = jsondata["_songName"]
            jartistName = jsondata["_songAuthorName"]

            BPS = int(BPM)/60
            lengthOfBeat = 1/BPS

        # open song file and try to read length.

        

    
        with open(baseFolder+ os.sep + foundMapFile, "r") as mapfile:
            levelData = mapfile.read()
            levelObj = json.loads(levelData)

            notesArray = levelObj["_notes"]

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

                    
    # Add a new section and some values
    config.add_section('Map')
    config.set('Map', 'songName', str(jsongName))
    config.set('Map', 'songArtist', str(jartistName))
    config.set('Map', 'leftNotes', str(notesLeft))
    config.set('Map', 'upNotes', str(notesMidRight))
    config.set('Map', 'rightNotes', str(notesRight))
    config.set('Map', 'noteMoveSpeed', str(5))
    config.set('Map', 'songLength', str(songLength))
    config.set('Map', 'converted',str(1))
    #config.set('Map', 'notesRight', str(notesRight))

    # Save to a file
    outputfile = "map.ini"
    try:
        with open(baseFolder+os.sep+outputfile, 'w') as configfile:
            config.write(configfile)
    except:
        print("Couldnt write file...")

    print("BPM: "+ str(BPM))
    print("Song name: "+ str(jsongName))
    print("Artist: "+str(jartistName))
    print("Duration: "+str(songLength))

       
      
    
    
        
            
    
        

        

