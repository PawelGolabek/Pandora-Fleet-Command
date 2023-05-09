from src.shipCombat import putTracer, createRocket,laser
from src.ammunitionType import *
import src.naglowek as naglowek

############################## SYSTEMS #############################################
class system(object):
    def __init__(self,name = "system",minEnergy=0,maxEnergy=5,energy=0, maxCooldown = 2000, cooldown = 0, mass = 10, cost = 0):
        self.name = name
        self.minEnergy = minEnergy
        self.maxEnergy = maxEnergy
        self.energy = energy
        self.maxCooldown = maxCooldown
        self.cooldown = cooldown
        self.mass = mass
        self.cost = cost
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        pass
    def activate(self,ship,var,gameRules,uiMetrics):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class none(system):
    def __init__ (self,name = "noneSystem",minEnergy=0,maxEnergy=0,energy=0, maxCooldown = 10, cooldown = 0, mass = 0, cost = 0):
        super(none,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        pass
    def activate(self,ship,var,gameRules,uiMetrics):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
    
class throttleBrake1(system):
    def __init__ (self,name = "Throttle Brake I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 3000, cooldown = 0, mass = 10, cost = 80):
        super(throttleBrake1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and True):
            i=100
            while(ship1.hp != ship1.maxHp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown=self.maxCooldown
    def activate(self,ship,var,gameRules,uiMetrics):
        value = ship.maxSpeed/4
        ship.speed = ship.maxSpeed - self.energy*value
        putTracer(ship,var,gameRules,uiMetrics)
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
    

class hullRepairSystem1(system):
    def __init__ (self,name = "Anti Missle System I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 3000, cooldown = 0, mass = 10, cost = 100):
        super(hullRepairSystem1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and True):
            i=40
            while(ship1.hp != ship1.maxHp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown=self.maxCooldown
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class hullRepairSystem2(system):
    def __init__ (self,name = "Anti Missle System II",minEnergy=0,maxEnergy=10,energy=0, maxCooldown = 2000, cooldown = 0, mass = 20, cost = 150):
        super(hullRepairSystem2,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and ship1.hp != ship1.maxHp):
            i=60
            while(ship1.hp != ship1.maxAp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown=self.maxCooldown
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class antiMissleSystem1(system):
    def __init__ (self,name = "Anti Missle System II",minEnergy=0,maxEnergy=10,energy=0, maxCooldown = 15000, cooldown = 0, mass = 10, cost = 80):
        super(antiMissleSystem1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            minDist = 9999999
            range = ship1.detectionRange
            closestEnemyMissle = 0
            range = range * range
            for missle in var.currentMissles:
                if(not missle.owner == ship1.owner and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist ):
                        minDist = dist
                        closestEnemyMissle = missle
            if(closestEnemyMissle and minDist < range):
                currentLaser = laser()
                currentLaser.xPos = ship1.xPos
                currentLaser.yPos = ship1.yPos
                currentLaser.targetXPos = closestEnemyMissle.xPos
                currentLaser.targetYPos = closestEnemyMissle.yPos
                currentLaser.color = "magenta"
                currentLaser.ttl = 100
                (var.lasers).append(currentLaser)
                (var.currentMissles).remove(closestEnemyMissle)
                self.cooldown = self.maxCooldown
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost


class antiMissleSystem2(system):
    def __init__ (self,name = "Anti Missle System II",minEnergy=0,maxEnergy=10,energy=0, maxCooldown = 12000, cooldown = 0, mass = 25, cost = 80):
        super(antiMissleSystem2,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            minDist = 9999999
            range = ship1.detectionRange
            closestEnemyMissle = 0
            range = range * range
            for missle in var.currentMissles:
                if(not missle.owner == ship1.owner and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist ):
                        minDist = dist
                        closestEnemyMissle = missle

            if(closestEnemyMissle and minDist < range):
                currentLaser = laser()
                currentLaser.xPos = ship1.xPos
                currentLaser.yPos = ship1.yPos
                currentLaser.targetXPos = closestEnemyMissle.xPos
                currentLaser.targetYPos = closestEnemyMissle.yPos
                currentLaser.color = "magenta"
                currentLaser.ttl = 100
                (var.lasers).append(currentLaser)
                (var.currentMissles).remove(closestEnemyMissle)
                self.cooldown = self.maxCooldown
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost


class type1aCannon1(system):
    def __init__ (self,name = "Type1a Cannon I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 10000, cooldown = 0, mass = 10, cost = 40):
        super(type1aCannon1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            if(shoot(var,self,ship1,ammunition_type.type1adefault,ships,uiMetrics)):
                self.cooldown = self.maxCooldown

    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class type2aCannon1(system):
    def __init__ (self,name = "Type2a Cannon I",minEnergy=0,maxEnergy=6,energy=0, maxCooldown = 3000, cooldown = 0, mass = 15, cost = 65):
        super(type2aCannon1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            if(shoot(var,self,ship1,ammunition_type.type2adefault,ships,uiMetrics)):
                self.cooldown = self.maxCooldown

    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class type3aCannon1(system):
    def __init__ (self,name = "Type3a Cannon I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 17000, cooldown = 0, mass = 30, cost = 160):
        super(type3aCannon1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            if(shoot(var,self,ship1,ammunition_type.type3adefault,ships,uiMetrics)):
                self.cooldown = self.maxCooldown
        
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class gattlingLaser1(system):
    def __init__ (self,name = "Gattling Laser I",minEnergy=0,maxEnergy=9,energy=0, maxCooldown = 600, cooldown = 0, mass = 10, cost = 100):
        super(gattlingLaser1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics): 
        if(self.cooldown <= 0):
            if(shoot(var,self,ship1,ammunition_type.laser1adefault,ships,uiMetrics)):
                self.cooldown = self.maxCooldown
        
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class gattlingLaser2(system):
    def __init__ (self,name = "Gattling Laser II",minEnergy=2,maxEnergy=8,energy=0, maxCooldown = 400, cooldown = 0, mass = 15, cost = 110):
        super(gattlingLaser2,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            if(shoot(var,self,ship1,ammunition_type.laser1adefault,ships,uiMetrics)):
                self.cooldown = self.maxCooldown
        
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class highEnergyLaser1(system):
    def __init__ (self,name = "High Energy Laser I",minEnergy=4,maxEnergy=8,energy=0, maxCooldown = 8000, cooldown = 0, mass = 10, cost = 50):
        super(highEnergyLaser1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            if (shoot(var,self,ship1,ammunition_type.highEnergyLaser1,ships,uiMetrics)):
                self.cooldown = self.maxCooldown
        
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

class kinetic1(system):
    def __init__ (self,name = "Kinetic cannon I",minEnergy=0,maxEnergy=7,energy=0,maxCooldown=1000,cooldown=0,mass=30, cost = 60):
        super(kinetic1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown, mass, cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            if(shoot(var,self,ship1,ammunition_type.kinetic1,ships,uiMetrics)):
                self.cooldown = self.maxCooldown
        if(self.cooldown == (self.maxCooldown - 5) or self.cooldown == (self.maxCooldown - 10)):
            shoot(var,self,ship1,ammunition_type.kinetic1,ships,uiMetrics)    # optional extra shots
        
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost

def shoot(var,system,ship,ammunitionType,ships,uiMetrics,offsetX=0,offsetY=0):
    shipToShoot = 0
    minDist2 = 999999999
    for ship2 in ships:
        if(not ship.owner == ship2.owner): # add teams if needed            for element in list:
            list = []
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos
            ghostShip.y = ship.yPos
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos + uiMetrics.canvasWidth
            ghostShip.y = ship.yPos
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos - uiMetrics.canvasWidth
            ghostShip.y = ship.yPos
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos 
            ghostShip.y = ship.yPos + uiMetrics.canvasHeight
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos - var.left
            ghostShip.y = ship.yPos - uiMetrics.canvasHeight
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos - uiMetrics.canvasWidth
            ghostShip.y = ship.yPos - uiMetrics.canvasHeight
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos + uiMetrics.canvasWidth
            ghostShip.y = ship.yPos - uiMetrics.canvasHeight
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos - uiMetrics.canvasWidth
            ghostShip.y = ship.yPos + uiMetrics.canvasHeight
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = ship.xPos + uiMetrics.canvasWidth
            ghostShip.y = ship.yPos + uiMetrics.canvasHeight
            list.append(ghostShip)
            for element in list:
                distance2 = (element.x-ship2.xPos)*(element.x-ship2.xPos) + (element.y-ship2.yPos)*(element.y-ship2.yPos)
                if(ship2.visible == True and distance2 < (ship.detectionRange*ship.detectionRange) and distance2 < minDist2):
                    minDist2 = distance2
                    shipToShoot = ship2
    if(shipToShoot):
        createRocket(var,ship,shipToShoot,ammunitionType,offsetX,offsetY)
        return True
    return False

def declareGlobalSystems():
    naglowek.systemLookup = {           #for system creation
    "throttleBrake1": throttleBrake1,
    "type1aCannon1": type1aCannon1,
    "type2aCannon1": type2aCannon1,
    "type3aCannon1": type3aCannon1,
    "antiMissleSystem1": antiMissleSystem1,
    "antiMissleSystem2": antiMissleSystem2,
    "gattlingLaser1": gattlingLaser1,
    "gattlingLaser2": gattlingLaser2,
    "highEnergyLaser1": highEnergyLaser1,
    "hullRepairSystem1": hullRepairSystem1,
    "hullRepairSystem2": hullRepairSystem2,
    "kinetic1": kinetic1,
    "system": system,
    "none": none,
    }
    naglowek.allSystemsList = [           #for dropdown menus
        'none',
        "throttleBrake1",
        "type1aCannon1",
        "type2aCannon1",
        "type3aCannon1",
        "antiMissleSystem1",
        "antiMissleSystem2",
        "gattlingLaser1",
        "gattlingLaser2",
        "highEnergyLaser1",
        "hullRepairSystem1",
        "hullRepairSystem2",
        "kinetic1",
        "system",
        ]
    (naglowek.systemStatsBlueprints).throttleBrake1 = throttleBrake1()           
    (naglowek.systemStatsBlueprints).type1aCannon1 = type1aCannon1()
    (naglowek.systemStatsBlueprints).type2aCannon1 = type2aCannon1()
    (naglowek.systemStatsBlueprints).type3aCannon1 = type3aCannon1()
    (naglowek.systemStatsBlueprints).antiMissleSystem1 = antiMissleSystem1()
    (naglowek.systemStatsBlueprints).antiMissleSystem2 = antiMissleSystem2()
    (naglowek.systemStatsBlueprints).gattlingLaser1 = gattlingLaser1()
    (naglowek.systemStatsBlueprints).gattlingLaser2 = gattlingLaser2()
    (naglowek.systemStatsBlueprints).highEnergyLaser1 = highEnergyLaser1()
    (naglowek.systemStatsBlueprints).hullRepairSystem1 = hullRepairSystem1()
    (naglowek.systemStatsBlueprints).hullRepairSystem2 = hullRepairSystem2()
    (naglowek.systemStatsBlueprints).kinetic1 = kinetic1()
    (naglowek.systemStatsBlueprints).system = system()
    (naglowek.systemStatsBlueprints).none = none()

    naglowek.systemStats = {                                                  #to lookup statistics without creating
        'none': (naglowek.systemStatsBlueprints).none,
        "throttleBrake1": (naglowek.systemStatsBlueprints).throttleBrake1,
        "type1aCannon1": (naglowek.systemStatsBlueprints).type1aCannon1,
        "type2aCannon1": (naglowek.systemStatsBlueprints).type2aCannon1,
        "type3aCannon1": (naglowek.systemStatsBlueprints).type3aCannon1,
        "antiMissleSystem1": (naglowek.systemStatsBlueprints).antiMissleSystem1,
        "antiMissleSystem2": (naglowek.systemStatsBlueprints).antiMissleSystem2,
        "gattlingLaser1": (naglowek.systemStatsBlueprints).gattlingLaser1,
        "gattlingLaser2": (naglowek.systemStatsBlueprints).gattlingLaser2,
        "highEnergyLaser1": (naglowek.systemStatsBlueprints).highEnergyLaser1,
        "hullRepairSystem1": (naglowek.systemStatsBlueprints).hullRepairSystem1,
        "hullRepairSystem2": (naglowek.systemStatsBlueprints).hullRepairSystem2,
        "kinetic1": (naglowek.systemStatsBlueprints).kinetic1,
        "system": (naglowek.systemStatsBlueprints).system 
    }

