import naglowek

def declareGlobalThrusters():
    naglowek.allThrustersList = [
        'none',
        "lightThrusters1",
        ]
class thrusters(object):
    def __init__(self,name = "thrusters", mass = 10):
        self.mass = mass
        self.name = name
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class none(thrusters):
    def __init__ (self,name = "none", mass = 0):
        super(none,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class lightThrusters1(thrusters):
    def __init__ (self,name = "lightThrusters1", mass = 10):
        super(lightThrusters1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.directionalThrust += 40
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.directionalThrust -= 40
    
def declareGlobalThrusters():
    naglowek.allThrustersList = [
        'none',
        "lightThrusters1",
        ]
    (naglowek.thrustersStatsBlueprints).none = none()
    (naglowek.thrustersStatsBlueprints).lightThrusters1 = lightThrusters1()

    naglowek.thrustersStats = {
        'none':(naglowek.thrustersStatsBlueprints).none,
        "lightThrusters1":(naglowek.thrustersStatsBlueprints).lightThrusters1

    }