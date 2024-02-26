import src.settings as settings

class engine(object):
    def __init__(self,name = "engine",mass = 10, cost = 0):
        self.name = name
        self.mass = mass
        self.cost = cost
        self.description = ("Default text")

class none(engine):
    def __init__ (self,name = "None",mass = 0, cost = 0):
        super(none,self).__init__(name,mass,cost)
        self.description = ("No engine. This option must be changed in order to complete the ship.")
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 0
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 0

class recycledDrive(engine):
    def __init__ (self,name = "Recycled Drive",mass = 80,cost = 10):
        super(recycledDrive,self).__init__(name,mass,cost)
        self.description = ("Recycled Drive: \nMain Drive \n\
Mass: {} \nCost: {}").format(self.mass,self.cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 10
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 10


class lightPropeller(engine):
    def __init__ (self,name = "Light Propeller",mass = 10,cost = 100):
        super(lightPropeller,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 50
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 50

class mediumPropeller(engine):
    def __init__ (self,name = "Medium Propeller",mass = 20,cost = 150):
        super(mediumPropeller,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 80
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 80

class hardPropeller(engine):
    def __init__ (self,name = "Hard Propeller",mass = 20,cost = 200):
        super(hardPropeller,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 110
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 110

class dualJet(engine):
    def __init__ (self,name = "Dual Jet",mass = 80,cost = 400):
        super(dualJet,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 100
        ship.directionalThrust += 40
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 100
        ship.directionalThrust -= 40

class quadJet(engine):
    def __init__ (self,name = "Quad Jet",mass = 80,cost = 800):
        super(quadJet,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 160
        ship.directionalThrust += 80
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 160
        ship.directionalThrust -= 80

class hexaJet(engine):
    def __init__ (self,name = "Hexa Jet",mass = 140,cost = 1000):
        super(hexaJet,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.mainThrust += 220
        ship.directionalThrust += 120
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.mainThrust -= 220
        ship.directionalThrust -= 120
    
def declareGlobalEngines():
    settings.allEnginesList = [
        'none',
        "Recycled Drive",
        "Light Propeller",
        "Medium Propeller",
        "Hard Propeller",
        "Dual Jet",
        "Quad Jet",
        "Hexa Jet"
        ]
    (settings.engineStatsBlueprints).none = none()
    (settings.engineStatsBlueprints).recycledDrive = recycledDrive()
    (settings.engineStatsBlueprints).lightPropeller = lightPropeller()
    (settings.engineStatsBlueprints).mediumPropeller = mediumPropeller()
    (settings.engineStatsBlueprints).hardPropeller = hardPropeller()
    (settings.engineStatsBlueprints).dualJet = dualJet()
    (settings.engineStatsBlueprints).quadJet = quadJet()
    (settings.engineStatsBlueprints).hexaJet = hexaJet()

    settings.engineStats = {
        'none':(settings.engineStatsBlueprints).none,
        'Recycled Drive':(settings.engineStatsBlueprints).recycledDrive,
        "Light Propeller":(settings.engineStatsBlueprints).lightPropeller,
        "Medium Propeller":(settings.engineStatsBlueprints).mediumPropeller,
        "Hard Propeller":(settings.engineStatsBlueprints).hardPropeller,
        "Dual Jet":(settings.engineStatsBlueprints).dualJet,
        "Quad Jet":(settings.engineStatsBlueprints).quadJet,
        "Hexa Jet":(settings.engineStatsBlueprints).hexaJet,

    }