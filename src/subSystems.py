import src.naglowek as naglowek

class subsystem(object):
    def __init__(self,name = "subsystem", mass = 10):
        self.name = name
        self.mass = mass
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class none(subsystem):
    def __init__ (self,name = "noneSystem",mass = 0):
        super(none,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
    def onRemoving(self,ship):
        ship.mass -= self.mass

class armorPlate1(subsystem):
    def __init__ (self,name = "armorPlate1",mass = 45):
        super(armorPlate1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.ap += 30
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.ap -= 30

class extendedSensors(subsystem):
    def __init__ (self,name = "extendedSensors",mass = 5):
        super(extendedSensors,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.detectionRange += 15
        ship.maxEnergy -= 1
        ship.minEnergyConsumption += 1
        ship.maxEnergyConsumption += 1
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.detectionRange -= 15
        ship.maxEnergy += 1
        ship.minEnergyConsumption -= 1
        ship.maxEnergyConsumption -= 1

class shieldCell1(subsystem):
    def __init__ (self,name = "shieldCell1",mass = 15):
        super(shieldCell1,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.shields += 1
        ship.maxShields += 1
        ship.maxEnergy -= 1
        ship.minEnergyConsumption += 1
        ship.maxEnergyConsumption += 1
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.shields -= 1
        ship.maxShields -= 1
        ship.maxEnergy += 1
        ship.minEnergyConsumption -= 1
        ship.maxEnergyConsumption -= 1

class energyExtension(subsystem):
    def __init__ (self,name = "energyExtension",mass = 5):
        super(energyExtension,self).__init__(name,mass)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.maxEnergy += 1
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.maxEnergy -= 1

def declareGlobalSubsystems():
    naglowek.allSubsystemsList = [
        'none',
        'armorPlate',
        'extendedSensors',
        'energyExtension',
        'shieldCell1'
        ]
    (naglowek.subsystemStatsBlueprints).none = none()
    (naglowek.subsystemStatsBlueprints).armorPlate1 = armorPlate1()
    (naglowek.subsystemStatsBlueprints).extendedSensors = extendedSensors()
    (naglowek.subsystemStatsBlueprints).energyExtension = energyExtension()
    (naglowek.subsystemStatsBlueprints).shieldCell1 = shieldCell1()
    naglowek.subsystemStats = {
        'none': (naglowek.subsystemStatsBlueprints).none,
        'armorPlate': (naglowek.subsystemStatsBlueprints).armorPlate1,
        'extendedSensors': (naglowek.subsystemStatsBlueprints).extendedSensors,
        'energyExtension': (naglowek.subsystemStatsBlueprints).energyExtension,
        'shieldCell1': (naglowek.subsystemStatsBlueprints).shieldCell1
    }


class subsystem(object):
    def __init__(self,globalVar,name = "subsystem",minEnergy=0,maxEnergy=5,energy=0, maxCooldown = 200, cooldown = 0):
        self.var = globalVar
        self.name = name
        self.minEnergy = minEnergy
        self.maxEnergy = maxEnergy
        self.energy = energy
        self.maxCooldown = maxCooldown
        self.cooldown = cooldown
    def trigger(self,var,ship1,ships,shipLookup):
        pass
    def activate(self,ship,var,gameRules,uiMetrics):
        pass
