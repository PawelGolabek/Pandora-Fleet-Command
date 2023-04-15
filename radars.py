import naglowek

def declareGlobalRadars():
    naglowek.allRadarsList = [
        'none',
        "shortPulseRadar1",
        ]

class radar(object):
    def __init__(self,name = "radar",mass = 10):
        self.mass = mass
        self.name = name

class none(radar):
    def __init__ (self,name = "none",mass = 0):
        super(none,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class shortPulseRadar1(radar):
    def __init__ (self,name = "shortPulseRadar1",mass = 10):
        super(shortPulseRadar1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.detectionRange += 30
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 30
        ship.mass -= self.mass
    
def declareGlobalRadars():
    naglowek.allRadarsList = [
        'none',
        "shortPulseRadar1",
        ]
    (naglowek.radarStatsBlueprints).none = none()
    (naglowek.radarStatsBlueprints).shortPulseRadar1 = shortPulseRadar1()

    naglowek.radarStats = {
        'none':(naglowek.radarStatsBlueprints).none,
        "shortPulseRadar1":(naglowek.radarStatsBlueprints).shortPulseRadar1

    }