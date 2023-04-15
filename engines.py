import naglowek

class engine(object):
    def __init__(self,name = "engine",mass = 10):
        self.mass = mass
        self.name = name

class none(engine):
    def __init__ (self,name = "none",mass = 0):
        super(none,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class lightPropellant1(engine):
    def __init__ (self,name = "lightPropellant1",mass = 10):
        super(lightPropellant1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.mainThrust += 50
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.mainThrust -= 50

class mediumPropellant1(engine):
    def __init__ (self,name = "mediumPropellant1",mass = 20):
        super(mediumPropellant1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.mainThrust += 80
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.mainThrust -= 80
    
def declareGlobalEngines():
    naglowek.allEnginesList = [
        'none',
        "lightPropellant1",
        "mediumPropellant1",
        ]
    (naglowek.engineStatsBlueprints).none = none()
    (naglowek.engineStatsBlueprints).lightPropellant1 = lightPropellant1()
    (naglowek.engineStatsBlueprints).mediumPropellant1= mediumPropellant1()

    naglowek.engineStats = {
        'none':(naglowek.engineStatsBlueprints).none,
        "lightPropellant1":(naglowek.engineStatsBlueprints).lightPropellant1,
        "mediumPropellant1":(naglowek.engineStatsBlueprints).mediumPropellant1

    }