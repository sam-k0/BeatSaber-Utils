import os

rootdir = "C:\\Users\\kooba\\Downloads"

for baseFolder, dirs, files in os.walk(rootdir):
    for file in files:
        #Fill map data array
            print(baseFolder)
            os.remove(baseFolder+os.sep+file)
