import src.naglowek as naglowek

def declareGlobalGenerators():
    naglowek.allGeneratorsList = [
        'none',
        "reactor",
        ]

class generator(object):
    def __init__(self,name = "generator", mass = 10, cost = 0):
        self.mass = mass
        self.name = name
        self.cost = cost
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class none(generator):
    def __init__ (self,name = "none",mass = 0, cost = 0):
        super(none,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class reactor(generator):
    def __init__ (self,name = "reactor",mass = 10, cost = 100):
        super(reactor,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy -= 6
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 6

class extendedReactor(generator):
    def __init__ (self,name = "Extended Reactor",mass = 20, cost = 240):
        super(extendedReactor,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += 10
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 10
    
def declareGlobalGenerators():
    (naglowek.generatorStatsBlueprints).none = none()
    (naglowek.generatorStatsBlueprints).reactor = reactor()
    (naglowek.generatorStatsBlueprints).extendedReactor = extendedReactor()
    naglowek.allGeneratorsList = [
        (naglowek.generatorStatsBlueprints).none.name,
        (naglowek.generatorStatsBlueprints).reactor.name,
        (naglowek.generatorStatsBlueprints).extendedReactor.name
        ]
    naglowek.generatorStats = {
        (naglowek.generatorStatsBlueprints).none.name: (naglowek.generatorStatsBlueprints).none,
        (naglowek.generatorStatsBlueprints).reactor.name: (naglowek.generatorStatsBlueprints).reactor,
        (naglowek.generatorStatsBlueprints).extendedReactor.name: (naglowek.generatorStatsBlueprints).extendedReactor

    }