import src.settings as settings

def declareGlobalRadars():
    settings.allRadarsList = [
        'none',
        "shortPulseRadar",
        ]

class radar(object):
    def __init__(self,name = "radar",mass = 10,cost = 0):
        self.mass = mass
        self.name = name
        self.cost = cost
        self.description = ("Default text")

class none(radar):
    def __init__ (self,name = "none",mass = 0,cost = 0):
        super(none,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class recycledSensors(radar):
    def __init__ (self,name = "Recycled Sensors",mass = 50,cost = 20):
        super(recycledSensors,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.detectionRange += 40
        ship.cost += self.cost
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 40
        ship.cost -= self.cost
        ship.mass -= self.mass


class shortPulseRadar(radar):
    def __init__ (self,name = "Short Pulse Radar",mass = 50,cost = 80):
        super(shortPulseRadar,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.detectionRange += 110
        ship.cost += self.cost
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 110
        ship.cost -= self.cost
        ship.mass -= self.mass

class longPulseRadar(radar):
    def __init__ (self,name = "Long Pulse Radar",mass = 50,cost = 160):
        super(longPulseRadar,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.detectionRange += 130
        ship.cost += self.cost
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 130
        ship.cost -= self.cost
        ship.mass -= self.mass

class swiftTrackRadar(radar):
    def __init__ (self,name = "Swift Track Radar",mass = 10,cost = 160):
        super(swiftTrackRadar,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.detectionRange += 100
        ship.cost += self.cost
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 100
        ship.cost -= self.cost
        ship.mass -= self.mass


class hyperPulseRadar(radar):
    def __init__ (self,name = "Hyper Pulse Radar",mass = 50,cost = 1200):
        super(hyperPulseRadar,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.detectionRange += 300
        ship.cost += self.cost
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 300
        ship.cost -= self.cost
        ship.mass -= self.mass
    
def declareGlobalRadars():
    (settings.radarStatsBlueprints).none = none()
    (settings.radarStatsBlueprints).shortPulseRadar = shortPulseRadar()
    (settings.radarStatsBlueprints).longPulseRadar = longPulseRadar()
    (settings.radarStatsBlueprints).recycledSensors = recycledSensors()
    (settings.radarStatsBlueprints).swiftTrackRadar = swiftTrackRadar()
    (settings.radarStatsBlueprints).hyperPulseRadar = hyperPulseRadar()
    settings.allRadarsList = [
        (settings.radarStatsBlueprints).none.name,
        (settings.radarStatsBlueprints).shortPulseRadar.name,
        (settings.radarStatsBlueprints).longPulseRadar.name,
        (settings.radarStatsBlueprints).recycledSensors.name,
        (settings.radarStatsBlueprints).swiftTrackRadar.name,
        (settings.radarStatsBlueprints).hyperPulseRadar.name,
        ]
    settings.radarStats = {
        (settings.radarStatsBlueprints).none.name: (settings.radarStatsBlueprints).none,
        (settings.radarStatsBlueprints).shortPulseRadar.name : (settings.radarStatsBlueprints).shortPulseRadar,
        (settings.radarStatsBlueprints).longPulseRadar.name : (settings.radarStatsBlueprints).longPulseRadar,
        (settings.radarStatsBlueprints).recycledSensors.name : (settings.radarStatsBlueprints).recycledSensors,
        (settings.radarStatsBlueprints).swiftTrackRadar.name : (settings.radarStatsBlueprints).swiftTrackRadar,
        (settings.radarStatsBlueprints).hyperPulseRadar.name : (settings.radarStatsBlueprints).hyperPulseRadar,

    }