

import src.settings as settings

class subsystem(object):
    def __init__(self,name = "Subsystem", mass = 10, cost = 0):
        self.name = name
        self.mass = mass
        self.cost = cost
        self.description = ("Default text")
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class none(subsystem):
    def __init__ (self,name = "none",mass = 0, cost = 0):
        super(none,self).__init__(name,mass,cost)
        self.description = ("No subsystem \n\
mass: {}\ncost: {}\
").format(self.mass,self.cost)

    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class armorPlate1(subsystem):
    def __init__ (self,name = "Armor Plate",mass = 45, cost = 20):
        super(armorPlate1,self).__init__(name,mass,cost)
        self.armorBonus = 30
        self.description = ("Armor plate:\nAdds +{} to your ship armor \n\
mass: {}\ncost: {}\
").format(self.armorBonus,self.mass,self.cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.ap += self.armorBonus
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.ap -= self.armorBonus

class extendedSensors(subsystem):
    def __init__ (self,name = "Extended Sensors",mass = 5, cost = 100):
        super(extendedSensors,self).__init__(name,mass,cost)
        self.energyCons = 1
        self.detectionBoost = 10
        self.description = ("Extended Sensors:\nAdds +{} to your ship sensor range \nfor {} energy consumption \n\
mass: {}\ncost: {}\
").format(self.detectionBoost,self.energyCons,self.mass,self.cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.detectionRange += self.detectionBoost
        ship.maxEnergy -= self.energyCons
        ship.minEnergyConsumption += self.energyCons
        ship.maxEnergyConsumption += self.energyCons
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.detectionRange -= self.detectionBoost
        ship.maxEnergy += self.energyCons
        ship.minEnergyConsumption -= self.energyCons
        ship.maxEnergyConsumption -= self.energyCons

class shieldCell1(subsystem):
    def __init__ (self,name = "Shield Cell I",mass = 15, cost = 40):
        super(shieldCell1,self).__init__(name,mass,cost)
        self.energyCons = 2
        self.shieldBoost = 1
        self.description = ("Shield Cell I:\nAdds +{} shields to your ship \nfor {} energy consumption \n\
mass: {}\ncost: {}\
").format(self.shieldBoost,self.energyCons,self.mass,self.cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.shields += self.shieldBoost
        ship.maxShields += self.shieldBoost
        ship.maxEnergy -= self.energyCons
        ship.minEnergyConsumption += self.energyCons
        ship.maxEnergyConsumption += self.energyCons
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.shields -= self.shieldBoost
        ship.maxShields -= self.shieldBoost
        ship.maxEnergy += self.energyCons
        ship.minEnergyConsumption -= self.energyCons
        ship.maxEnergyConsumption -= self.energyCons

class shieldCell2(subsystem):
    def __init__ (self,name = "Shield Cell II",mass = 15, cost = 200):
        super(shieldCell2,self).__init__(name,mass,cost)
        self.energyCons = 5
        self.shieldBoost = 2
        self.description = ("Shield Cell II:\nAdds +{} to your ship shields \nfor {} energy consumption \n\
mass: {}\ncost: {}\
").format(self.shieldBoost, self.energyCons,self.mass,self.cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.shields += self.shieldBoost
        ship.maxShields += self.shieldBoost
        ship.maxEnergy -= self.energyCons
        ship.minEnergyConsumption += self.energyCons
        ship.maxEnergyConsumption += self.energyCons
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.shields -= self.shieldBoost
        ship.maxShields -= self.shieldBoost
        ship.maxEnergy += self.energyCons
        ship.minEnergyConsumption -= self.energyCons
        ship.maxEnergyConsumption -= self.energyCons

class energyExtension1(subsystem):
    def __init__ (self,name = "Energy Extension I",mass = 5, cost = 20):
        super(energyExtension1,self).__init__(name,mass,cost)
        self.energyExt = 1
        self.description = ("Energy Extension I:\nAdds +{} maximum energy to your ship\n\
mass: {}\ncost: {}\
").format(self.energyExt,self.mass,self.cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += self.energyExt
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= self.energyExt

class energyExtension2(subsystem):
    def __init__ (self,name = "Energy Extension II",mass = 5, cost = 120):
        super(energyExtension2,self).__init__(name,mass,cost)
        self.energyExt = 3
        self.description = ("Energy Extension II:\nAdds +{} maximum energy to your ship\n\
mass: {}\ncost: {}\
").format(self.energyExt,self.mass,self.cost)
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy += self.energyExt
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy -= self.energyExt

def declareGlobalSubsystems():
    (settings.subsystemStatsBlueprints).none = none()
    (settings.subsystemStatsBlueprints).armorPlate1 = armorPlate1()
    (settings.subsystemStatsBlueprints).extendedSensors = extendedSensors()
    (settings.subsystemStatsBlueprints).energyExtension1 = energyExtension1()
    (settings.subsystemStatsBlueprints).energyExtension2 = energyExtension2()
    (settings.subsystemStatsBlueprints).shieldCell1 = shieldCell1()
    (settings.subsystemStatsBlueprints).shieldCell2 = shieldCell2()
    settings.allSubsystemsList = [
        (settings.subsystemStatsBlueprints).none.name ,
        (settings.subsystemStatsBlueprints).armorPlate1.name ,
        (settings.subsystemStatsBlueprints).extendedSensors.name ,
        (settings.subsystemStatsBlueprints).energyExtension1.name ,
        (settings.subsystemStatsBlueprints).energyExtension2.name ,
        (settings.subsystemStatsBlueprints).shieldCell1.name ,
        (settings.subsystemStatsBlueprints).shieldCell2.name 
        ]
    settings.subsystemStats = {
        (settings.subsystemStatsBlueprints).none.name : (settings.subsystemStatsBlueprints).none,
        (settings.subsystemStatsBlueprints).armorPlate1.name: (settings.subsystemStatsBlueprints).armorPlate1,
        (settings.subsystemStatsBlueprints).extendedSensors.name : (settings.subsystemStatsBlueprints).extendedSensors,
        (settings.subsystemStatsBlueprints).energyExtension1.name : (settings.subsystemStatsBlueprints).energyExtension1,
        (settings.subsystemStatsBlueprints).energyExtension2.name : (settings.subsystemStatsBlueprints).energyExtension2,
        (settings.subsystemStatsBlueprints).shieldCell1.name : (settings.subsystemStatsBlueprints).shieldCell1,
        (settings.subsystemStatsBlueprints).shieldCell2.name : (settings.subsystemStatsBlueprints).shieldCell2
    }