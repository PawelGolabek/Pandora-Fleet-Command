import src.naglowek as naglowek

class engine(object):
    def __init__(self,name = "engine",mass = 10, cost = 0):
        self.name = name
        self.mass = mass
        self.cost = cost
        self.description = ("Default text")

class none(engine):
    def __init__ (self,name = "none",mass = 0, cost = 0):
        super(none,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 0
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 0

class lightPropellant(engine):
    def __init__ (self,name = "lightPropellant",mass = 10,cost = 200):
        super(lightPropellant,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 50
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 50

class mediumPropellant(engine):
    def __init__ (self,name = "mediumPropellant",mass = 20,cost = 300):
        super(mediumPropellant,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 80
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 80
    
def declareGlobalEngines():
    naglowek.allEnginesList = [
        'none',
        "lightPropellant",
        "mediumPropellant",
        ]
    (naglowek.engineStatsBlueprints).none = none()
    (naglowek.engineStatsBlueprints).lightPropellant = lightPropellant()
    (naglowek.engineStatsBlueprints).mediumPropellant= mediumPropellant()

    naglowek.engineStats = {
        'none':(naglowek.engineStatsBlueprints).none,
        "lightPropellant":(naglowek.engineStatsBlueprints).lightPropellant,
        "mediumPropellant":(naglowek.engineStatsBlueprints).mediumPropellant

    }