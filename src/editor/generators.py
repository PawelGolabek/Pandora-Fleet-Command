
import src.settings as settings

def declareGlobalGenerators():
    settings.allGeneratorsList = [
        'none',
        "reactor",
        ]

class generator(object):
    def __init__(self,name = "generator", mass = 10, cost = 0):
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
        ship.maxEnergy += 10
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 10

class extendedReactor(generator):
    def __init__ (self,name = "Extended Reactor",mass = 20, cost = 240):
        super(extendedReactor,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += 15
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 15


class fusionReactor(generator):
    def __init__ (self,name = "Fusion Reactor",mass = 20, cost = 480):
        super(fusionReactor,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += 20
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 20


class zeroPowerSurger(generator):
    def __init__ (self,name = "Zero Power Surger",mass = 20, cost = 720):
        super(zeroPowerSurger,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += 25
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 25


class voidCharger(generator):
    def __init__ (self,name = "Void Charger",mass = 20, cost = 1480):
        super(voidCharger,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += 35
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 35
    
def declareGlobalGenerators():
    (settings.generatorStatsBlueprints).none = none()
    (settings.generatorStatsBlueprints).reactor = reactor()
    (settings.generatorStatsBlueprints).extendedReactor = extendedReactor()
    (settings.generatorStatsBlueprints).fusionReactor = fusionReactor()
    (settings.generatorStatsBlueprints).zeroPowerSurger = zeroPowerSurger()
    (settings.generatorStatsBlueprints).voidCharger = voidCharger()
    settings.allGeneratorsList = [
        (settings.generatorStatsBlueprints).none.name,
        (settings.generatorStatsBlueprints).reactor.name,
        (settings.generatorStatsBlueprints).extendedReactor.name,
        (settings.generatorStatsBlueprints).fusionReactor.name,
        (settings.generatorStatsBlueprints).zeroPowerSurger.name,
        (settings.generatorStatsBlueprints).voidCharger.name
        ]
    settings.generatorStats = {
        (settings.generatorStatsBlueprints).none.name: (settings.generatorStatsBlueprints).none,
        (settings.generatorStatsBlueprints).reactor.name: (settings.generatorStatsBlueprints).reactor,
        (settings.generatorStatsBlueprints).extendedReactor.name: (settings.generatorStatsBlueprints).extendedReactor,
        (settings.generatorStatsBlueprints).fusionReactor.name : (settings.generatorStatsBlueprints).fusionReactor,
        (settings.generatorStatsBlueprints).zeroPowerSurger.name : (settings.generatorStatsBlueprints).zeroPowerSurger,
        (settings.generatorStatsBlueprints).voidCharger.name : (settings.generatorStatsBlueprints).voidCharger

    }