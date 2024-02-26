import os
from pathlib import Path
import sys,os
import re

import src.naglowek as naglowek


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]



def declareGlobalMaps():
    naglowek.mapOptions = [
    "anarchyRim",
    "asteroidField",
    "drillingStation",
    "rogueStation",
    "voidWithin",
    "sol25",
    "hadesPortal",
    ]
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    filePath = os.path.join(cwd, "campaignMissions\\")
    os.walk(filePath)
    naglowek.campaignOptions = os.listdir(filePath)
    (naglowek.campaignOptions).sort(key=natural_keys)

    filePath = os.path.join(cwd, "maps\\")
    os.walk(filePath)
    naglowek.mapOptions = os.listdir(filePath)

  #  naglowek.campaignOptions = ["1. Exiled-To-Make-A-Stand","2. Warcries-That-Shred-The-Clouds","3. Destination-For-Past-That-Never-Was","4. The-Void-Within","5. Burn-Those-Who-Opose-Us"]