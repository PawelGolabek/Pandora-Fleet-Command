import naglowek

def declareGlobalSubsystems():
    naglowek.allSubsystemsList = [
        'none',
        'armorPlate',
        'extendedSensors',
        'energyExtension'
        ]

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

class throttleBrake1(subsystem):
    def __init__ (self,globalVar,name = "Throttle Brake I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 300, cooldown = 0):
        super(throttleBrake1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        if(self.cooldown <= 0 and True):
            i=100
            while(ship1.hp != ship1.maxHp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown=self.maxCooldown
    def activate(self,ship,var,gameRules,uiMetrics):
        value = ship.maxSpeed/4
        ship.speed = ship.maxSpeed - self.energy*value
        pass
    