import src.naglowek as naglowek

class subsystem(object):
    def __init__(self,name = "Subsystem", mass = 10, cost = 0):
        self.name = name
        self.mass = mass
        self.cost = cost
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class none(subsystem):
    def __init__ (self,name = "none",mass = 0, cost = 0):
        super(none,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class armorPlate1(subsystem):
    def __init__ (self,name = "Armor Plate",mass = 45, cost = 20):
        super(armorPlate1,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.ap += 30
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.ap -= 30

class extendedSensors(subsystem):
    def __init__ (self,name = "Extended Sensors",mass = 5, cost = 30):
        super(extendedSensors,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.detectionRange += 30
        ship.maxEnergy -= 1
        ship.minEnergyConsumption += 1
        ship.maxEnergyConsumption += 1
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.detectionRange -= 30
        ship.maxEnergy += 1
        ship.minEnergyConsumption -= 1
        ship.maxEnergyConsumption -= 1

class shieldCell1(subsystem):
    def __init__ (self,name = "Shield Cell I",mass = 15, cost = 40):
        super(shieldCell1,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.shields += 1
        ship.maxShields += 1
        ship.maxEnergy -= 1
        ship.minEnergyConsumption += 1
        ship.maxEnergyConsumption += 1
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.shields -= 1
        ship.maxShields -= 1
        ship.maxEnergy += 1
        ship.minEnergyConsumption -= 1
        ship.maxEnergyConsumption -= 1

class shieldCell2(subsystem):
    def __init__ (self,name = "Shield Cell II",mass = 15, cost = 50):
        super(shieldCell2,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.shields += 5
        ship.maxShields += 1
        ship.maxEnergy -= 2
        ship.minEnergyConsumption += 2
        ship.maxEnergyConsumption += 2
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.shields -= 5
        ship.maxShields -= 1
        ship.maxEnergy += 2
        ship.minEnergyConsumption -= 2
        ship.maxEnergyConsumption -= 2

class energyExtension1(subsystem):
    def __init__ (self,name = "Energy Extension I ",mass = 5, cost = 20):
        super(energyExtension1,self).__init__(name,mass,cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += 1
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= 1

def declareGlobalSubsystems():
    (naglowek.subsystemStatsBlueprints).none = none()
    (naglowek.subsystemStatsBlueprints).armorPlate1 = armorPlate1()
    (naglowek.subsystemStatsBlueprints).extendedSensors = extendedSensors()
    (naglowek.subsystemStatsBlueprints).energyExtension1 = energyExtension1()
    (naglowek.subsystemStatsBlueprints).shieldCell1 = shieldCell1()
    (naglowek.subsystemStatsBlueprints).shieldCell2 = shieldCell2()
    naglowek.allSubsystemsList = [
        (naglowek.subsystemStatsBlueprints).none.name ,
        (naglowek.subsystemStatsBlueprints).armorPlate1.name ,
        (naglowek.subsystemStatsBlueprints).extendedSensors.name ,
        (naglowek.subsystemStatsBlueprints).energyExtension1.name ,
        (naglowek.subsystemStatsBlueprints).shieldCell1.name ,
        (naglowek.subsystemStatsBlueprints).shieldCell2.name 
        ]
    naglowek.subsystemStats = {
        (naglowek.subsystemStatsBlueprints).none.name : (naglowek.subsystemStatsBlueprints).none,
        (naglowek.subsystemStatsBlueprints).armorPlate1.name: (naglowek.subsystemStatsBlueprints).armorPlate1,
        (naglowek.subsystemStatsBlueprints).extendedSensors.name : (naglowek.subsystemStatsBlueprints).extendedSensors,
        (naglowek.subsystemStatsBlueprints).energyExtension1.name : (naglowek.subsystemStatsBlueprints).energyExtension1,
        (naglowek.subsystemStatsBlueprints).shieldCell1.name : (naglowek.subsystemStatsBlueprints).shieldCell1,
        (naglowek.subsystemStatsBlueprints).shieldCell2.name : (naglowek.subsystemStatsBlueprints).shieldCell2
    }


class subsystem(object):
    def __init__(self,globalVar,name = "subsystem",minEnergy=0,maxEnergy=5,energy=0, maxCooldown = 200, cooldown = 0, cost = 0):
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
