


def calcBeatLen(bpm: int):
    BPS = int(bpm)/60
    lengthOfBeat = 1/BPS
    return lengthOfBeat

def calcTimePos(lengthOfBeat: int, timestamp: int, offset: int):
    calcTime = timestamp*lengthOfBeat
    calcTime = round(calcTime*1000)
    return calcTime+offset



