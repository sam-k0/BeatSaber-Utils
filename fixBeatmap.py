## this is to fix broken beatmap folders.
import os
import shutil
import json
from typing import Dict #invite jason

rootdir = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels"#'C:\\Users\\kooba\\OneDrive\\Dokumente\\dataDumper'



# main

for baseFolder, dirs, files in os.walk(rootdir):
    for file in files:
        

        if file.lower().endswith("info.dat"):
            #do stuff
            data = dict()
            with open(baseFolder+ os.sep +file) as infofile:
                data = infofile.read()
                jobj = json.loads(data)

                songfilename = jobj["_songFilename"]
                coverfilename = jobj["_coverImageFilename"]
                # rename accordingly
                print("Songfile: "+songfilename + "/ "+"cover:"+coverfilename)
                
                for _baseFolder, _dirs, _files in os.walk(baseFolder):
                    for __file in _files:
                        if __file.endswith(".ogg") or __file.endswith(".egg"):
                            try:
                                os.rename(_baseFolder+ os.sep+__file,_baseFolder+ os.sep+songfilename)
                            except:
                                print("Couldn't rename "+_baseFolder+ os.sep+__file)
                        
                        if __file.endswith(".jpg") or __file.endswith(".png"):
                            try:
                                os.rename(_baseFolder+ os.sep+__file,_baseFolder+ os.sep+coverfilename)
                            except:
                                print("Couldn't rename "+_baseFolder+ os.sep+__file)
        
                """
                if fileInDir.endswith(".ogg") or fileInDir.endswith(".egg"):
                    try:
                        os.rename(baseFolder+ os.sep+fileInDir,baseFolder+ os.sep+songfilename)
                    except:
                        print("Couldn't rename "+baseFolder+ os.sep+fileInDir)
                
                if fileInDir.endswith(".jpg") or fileInDir.endswith(".png"):
                    try:
                        os.rename(baseFolder+ os.sep+fileInDir,baseFolder+ os.sep+coverfilename)
                    except:
                        print("Couldn't rename "+baseFolder+ os.sep+fileInDir)"""

               