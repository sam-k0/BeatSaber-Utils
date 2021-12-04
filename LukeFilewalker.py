import os
import shutil
import configparser
from configparser import ConfigParser
import json #invite jason
from tinytag import TinyTag
from PIL import Image
import sys

rootdir = "C:\\Users\\kooba\\Downloads\\Beatmaps"#'C:\\Users\\kooba\\OneDrive\\Dokumente\\dataDumper'
config = ConfigParser()

if(len(sys.argv) >= 2):
    rootdir = sys.argv[1]
    print("Startup argument found. Using rootdir "+sys.argv[1])

totalConverted = 0

ERASE_COVERS = 0

#func 

def calcAddTime(_time,_lob):
    calcTime = _time*_lob
    calcTime = round(calcTime*60)
    
    return calcTime


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


    print("|--Mapfile "+ foundMapFile+" Found file:"+str(int(mapAlreadyFound))+"  || "+baseFolder)
    return foundMapFile

def loadInfoDat(file):
    data = []
    if file.endswith("info.dat") or file.endswith("Info.dat"):                                                           # Load info.dat
            
        __file = open(os.path.join(file))
        jsondata = json.load(__file)
        data.append(file)
        data.append(jsondata["_beatsPerMinute"])
        data.append(jsondata["_songName"])
        data.append(jsondata["_songAuthorName"])

        
        return data



for baseFolder, dirs, files in os.walk(rootdir):
    #Define song variables
    try:
        print(":"+baseFolder)
        notesLeft=[]       #type 0
        notesMidLeft=[]    #type 1
        notesMidRight=[]   #type 2
        notesRight=[]      #type 3
        # Song beats
        BPM = 0
        BPS = 0
        lengthOfBeat = 0
        #file
        infofile = ""
        mapfile = ""
        tag = ""
        songLength = 0
        jsongName = ""
        jartistName = ""
        totalConverted += 1

        #                                              ------------------0--------1-----2----------3--------4-------5
        infoDatData = ["INFODAT",0,"SONGNAME","AUTHOR",0,"EXPERTDAT"] #[Info.dat, BPM, SONGNAME, AUTHOR, SONGLEN, LEVELDAT]

        # Get mapfile preferred
        
        infoDatData[5] = findMapfile(baseFolder)
    except:
        print("err. 112")
    

    if baseFolder == "C:\\Users\\kooba\\OneDrive\\Dokumente\\dataDumper":
        continue

    for file in files: 
        #Fill map data array
        if file.endswith("map.ini"):
            os.remove(baseFolder+os.sep+file)

        if file.endswith("info.dat") or file.endswith("Info.dat"):                                                           # Load info.dat
            __file = open(os.path.join(baseFolder,file))
            jsondata = json.load(__file)
            infoDatData[0]=(file)
            infoDatData[1]=(jsondata["_beatsPerMinute"])
            infoDatData[2]=(jsondata["_songName"])
            infoDatData[3]=(jsondata["_songAuthorName"])

            BPS = int(infoDatData[1])/60
            lengthOfBeat = 1/BPS
        
        if file.endswith(".egg"):
            #do stuff
            tag = TinyTag.get(baseFolder+ os.sep+file)
            infoDatData[4] = round( tag.duration + 5)
            #Try to rename the .egg to ogg
            try:
                os.rename(baseFolder+ os.sep+file,baseFolder+ os.sep+'song.ogg')
            except:
                print("Couldn't rename "+baseFolder+ os.sep+file)

        elif file.endswith(".ogg"):
            #do more stuff
            tag = TinyTag.get(baseFolder+ os.sep+file)
            infoDatData[4] = round( tag.duration + 5)

        if (file.endswith(".jpg") and not os.path.isfile(baseFolder+ os.sep+'cover.jpg')):  # Rename cover
            try:
                #try resize img
                basewidth = 240
                img = Image.open(baseFolder+os.sep+file)
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                img.save(baseFolder+os.sep+"cover.jpg")
                #os.rename(baseFolder+ os.sep+file,baseFolder+ os.sep+'cover.jpg')
            except:
                print("Couldnt rename cover.")
        elif(file.endswith("cover.jpg")):
            try:
                os.rename(baseFolder+os.sep+file,baseFolder+os.sep+"0121233process.jpg")

                basewidth = 240
                img = Image.open(baseFolder+os.sep+"0121233process.jpg")
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                img.save(baseFolder+os.sep+"cover.jpg")
            except:
                print("Something went wrong while resizing cover image.")
                



        if (file.endswith(".jpg")):
            if ERASE_COVERS == 1:
                try:
                    os.remove(baseFolder+os.sep+file)
                except:
                    print("couldnt remove cover")
                


    # Get the notes
    
    if not os.path.isfile(baseFolder+ os.sep + infoDatData[5]):
        continue
    
    with open(baseFolder+ os.sep + infoDatData[5], "r") as mapfile:
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
    try:
        config.add_section('Map')
    except:
        print("Map is set!")

    lowercaseName = infoDatData[2]
    lowercaseName = lowercaseName#.lower()
    config.set('Map', 'songName', str(lowercaseName))
    config.set('Map', 'songArtist', str(infoDatData[3]))
    config.set('Map', 'leftNotes', str(notesLeft))
    config.set('Map', 'upNotes', str(notesMidRight))
    config.set('Map', 'rightNotes', str(notesRight))
    config.set('Map', 'noteMoveSpeed', str(5))
    config.set('Map', 'songLength', str(infoDatData[4]))
    config.set('Map', 'converted',str(1))
    #config.set('Map', 'notesRight', str(notesRight))

    # Save to a file
    outputfile = "map.ini"
    try:
        with open(baseFolder+os.sep+outputfile, 'w') as configfile:
            config.write(configfile)
    except:
        print("Couldnt write file...")

 
 
print("Total maps converted: "+str(totalConverted))
