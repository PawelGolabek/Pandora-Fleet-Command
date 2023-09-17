import src.naglowek as naglowek

def declareGlobalRadars():
    naglowek.allRadarsList = [
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

class shortPulseRadar(radar):
    def __init__ (self,name = "shortPulseRadar",mass = 10,cost = 20):
        super(shortPulseRadar,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.detectionRange += 30
        ship.cost += self.cost
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 30
        ship.cost -= self.cost
        ship.mass -= self.mass

class longPulseRadar(radar):
    def __init__ (self,name = "longPulseRadar",mass = 10,cost = 80):
        super(longPulseRadar,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.detectionRange += 50
        ship.cost += self.cost
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.detectionRange -= 50
        ship.cost -= self.cost
        ship.mass -= self.mass
    
def declareGlobalRadars():
    (naglowek.radarStatsBlueprints).none = none()
    (naglowek.radarStatsBlueprints).shortPulseRadar = shortPulseRadar()
    (naglowek.radarStatsBlueprints).longPulseRadar = longPulseRadar()
    naglowek.allRadarsList = [
        (naglowek.radarStatsBlueprints).none.name,
        (naglowek.radarStatsBlueprints).shortPulseRadar.name,
        (naglowek.radarStatsBlueprints).longPulseRadar.name
        ]
    naglowek.radarStats = {
        (naglowek.radarStatsBlueprints).none.name: (naglowek.radarStatsBlueprints).none,
        (naglowek.radarStatsBlueprints).shortPulseRadar.name : (naglowek.radarStatsBlueprints).shortPulseRadar,
        (naglowek.radarStatsBlueprints).longPulseRadar.name : (naglowek.radarStatsBlueprints).longPulseRadar

    }