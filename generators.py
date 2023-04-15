import naglowek

def declareGlobalGenerators():
    naglowek.allGeneratorsList = [
        'none',
        "reactor1",
        ]

def declareGlobalGenerators():
    naglowek.allGeneratorsList = [
        'none',
        "reactor1",
        ]

class generator(object):
    def __init__(self,name = "generator", mass = 10):
        self.mass = mass
        self.name = name
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class none(generator):
    def __init__ (self,name = "none",mass = 0):
        super(none,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class reactor1(generator):
    def __init__ (self,name = "reactor1",mass = 10):
        super(reactor1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.maxEnergy -= 6
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.maxEnergy -= 6

class extendedReactor1(generator):
    def __init__ (self,name = "extendedReactor1",mass = 20):
        super(extendedReactor1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.maxEnergy += 10
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.maxEnergy -= 10
    
def declareGlobalGenerators():
    naglowek.allGeneratorsList = [
        'none',
        "reactor1",
        "extendedReactor1"
        ]
    (naglowek.generatorStatsBlueprints).none = none()
    (naglowek.generatorStatsBlueprints).reactor1 = reactor1()
    (naglowek.generatorStatsBlueprints).extendedReactor1 = extendedReactor1()

    naglowek.generatorStats = {
        'none':(naglowek.generatorStatsBlueprints).none,
        "reactor1":(naglowek.generatorStatsBlueprints).reactor1,
        "extendedReactor1": (naglowek.generatorStatsBlueprints).extendedReactor1

    }