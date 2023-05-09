import src.naglowek as naglowek

def declareGlobalThrusters():
    naglowek.allThrustersList = [
        'none',
        "lightThrusters",
        ]
class thrusters(object):
    def __init__(self,name = "thrusters", mass = 10, cost = 10):
        self.mass = mass
        self.name = name
        self.cost = cost
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class none(thrusters):
    def __init__ (self,name = "none", mass = 0, cost = 10):
        super(none,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class lightThrusters(thrusters):
    def __init__ (self,name = "lightThrusters", mass = 10, cost = 60):
        super(lightThrusters,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.directionalThrust += 40
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.directionalThrust -= 40

class mediumThrusters(thrusters):
    def __init__ (self,name = "mediumThrusters", mass = 10, cost = 80):
        super(mediumThrusters,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.directionalThrust += 40
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.directionalThrust -= 40
    
def declareGlobalThrusters():
    naglowek.allThrustersList = [
        'none',
        "lightThrusters",
        "mediumThrusters"
        ]
    (naglowek.thrustersStatsBlueprints).none = none()
    (naglowek.thrustersStatsBlueprints).lightThrusters = lightThrusters()
    (naglowek.thrustersStatsBlueprints).mediumThrusters = mediumThrusters()

    naglowek.thrustersStats = {
        'none':(naglowek.thrustersStatsBlueprints).none,
        "lightThrusters":(naglowek.thrustersStatsBlueprints).lightThrusters,
        "mediumThrusters":(naglowek.thrustersStatsBlueprints).mediumThrusters

    }