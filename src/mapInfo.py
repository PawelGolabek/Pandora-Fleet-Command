import os
from pathlib import Path
import sys,os

import src.naglowek as naglowek

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

    filePath = os.path.join(cwd, "maps\\")
    os.walk(filePath)
    naglowek.mapOptions = os.listdir(filePath)

  #  naglowek.campaignOptions = ["1. Exiled-To-Make-A-Stand","2. Warcries-That-Shred-The-Clouds","3. Destination-For-Past-That-Never-Was","4. The-Void-Within","5. Burn-Those-Who-Opose-Us"]