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
        self.description = ("Default text")
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
    (naglowek.thrustersStatsBlueprints).none = none()
    (naglowek.thrustersStatsBlueprints).lightThrusters = lightThrusters()
    (naglowek.thrustersStatsBlueprints).mediumThrusters = mediumThrusters()
    naglowek.allThrustersList = [ 
        (naglowek.thrustersStatsBlueprints).none.name,
        (naglowek.thrustersStatsBlueprints).lightThrusters.name,
        (naglowek.thrustersStatsBlueprints).mediumThrusters.name,
        ]

    naglowek.thrustersStats = {
        (naglowek.thrustersStatsBlueprints).none.name:(naglowek.thrustersStatsBlueprints).none,
        (naglowek.thrustersStatsBlueprints).lightThrusters.name:(naglowek.thrustersStatsBlueprints).lightThrusters,
        (naglowek.thrustersStatsBlueprints).mediumThrusters.name:(naglowek.thrustersStatsBlueprints).mediumThrusters

    }