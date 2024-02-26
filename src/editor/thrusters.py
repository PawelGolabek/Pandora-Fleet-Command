import src.settings as settings

def declareGlobalThrusters():
    settings.allThrustersList = [
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
    def __init__ (self,name = "none", mass = 0, cost = 0):
        super(none,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class basicThrusters(thrusters):
    def __init__ (self,name = "Basic Thrusters", mass = 10, cost = 10):
        super(basicThrusters,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.directionalThrust += 10
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.directionalThrust -= 10

class lightThrusters(thrusters):
    def __init__ (self,name = "Light Thrusters", mass = 40, cost = 40):
        super(lightThrusters,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.directionalThrust += 50
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.directionalThrust -= 50

class mediumThrusters(thrusters):
    def __init__ (self,name = "Medium Thrusters", mass = 60, cost = 80):
        super(mediumThrusters,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.directionalThrust += 70
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.directionalThrust -= 70

class hardThrusters(thrusters):
    def __init__ (self,name = "Hard Thrusters", mass = 80, cost = 160):
        super(hardThrusters,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.directionalThrust += 90
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.directionalThrust -= 90
    
def declareGlobalThrusters():
    (settings.thrustersStatsBlueprints).none = none()
    (settings.thrustersStatsBlueprints).basicThrusters = basicThrusters()
    (settings.thrustersStatsBlueprints).lightThrusters = lightThrusters()
    (settings.thrustersStatsBlueprints).mediumThrusters = mediumThrusters()
    (settings.thrustersStatsBlueprints).hardThrusters = hardThrusters()
    settings.allThrustersList = [ 
        (settings.thrustersStatsBlueprints).none.name,
        (settings.thrustersStatsBlueprints).basicThrusters.name,
        (settings.thrustersStatsBlueprints).lightThrusters.name,
        (settings.thrustersStatsBlueprints).mediumThrusters.name,
        (settings.thrustersStatsBlueprints).hardThrusters.name,
        ]

    settings.thrustersStats = {
        (settings.thrustersStatsBlueprints).none.name:(settings.thrustersStatsBlueprints).none,
        (settings.thrustersStatsBlueprints).basicThrusters.name : (settings.thrustersStatsBlueprints).basicThrusters,
        (settings.thrustersStatsBlueprints).lightThrusters.name:(settings.thrustersStatsBlueprints).lightThrusters,
        (settings.thrustersStatsBlueprints).mediumThrusters.name:(settings.thrustersStatsBlueprints).mediumThrusters,
        (settings.thrustersStatsBlueprints).hardThrusters.name : (settings.thrustersStatsBlueprints).hardThrusters,

    }