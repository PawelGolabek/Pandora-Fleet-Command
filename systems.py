from shipCombat import *
from ammunitionType import *

############################## SYSTEMS #############################################
class system(object):
    def __init__(self,globalVar,name = "system",minEnergy=0,maxEnergy=5,energy=0, maxCooldown = 200, cooldown = 0):
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

class throttleBrake1(system):
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
        putTracer(ship,var,gameRules,uiMetrics)
        pass
    

class hullRepairSystem1(system):
    def __init__ (self,globalVar,name = "Anti Missle System I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 300, cooldown = 0):
        super(hullRepairSystem1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        if(self.cooldown <= 0 and True):
            i=40
            while(ship1.hp != ship1.maxHp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown=self.maxCooldown

class hullRepairSystem2(system):
    def __init__ (self,globalVar,name = "Anti Missle System II",minEnergy=0,maxEnergy=10,energy=0, maxCooldown = 200, cooldown = 0):
        super(hullRepairSystem2,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        if(self.cooldown <= 0 and ship1.hp != ship1.maxHp):
            i=60
            while(ship1.hp != ship1.maxAp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown=self.maxCooldown

class antiMissleSystem1(system):
    def __init__ (self,globalVar,name = "Anti Missle System II",minEnergy=0,maxEnergy=10,energy=0, maxCooldown = 200, cooldown = 0):
        super(antiMissleSystem1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)
    def trigger(self,var,ship1,ships,shipLookup):
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


class antiMissleSystem2(system):
    def __init__ (self,globalVar,name = "Anti Missle System II",minEnergy=0,maxEnergy=10,energy=0, maxCooldown = 200, cooldown = 0):
        super(antiMissleSystem2,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)
    def trigger(self,var,ship1,ships,shipLookup):
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


class type1aCannon1(system):
    def __init__ (self,globalVar,name = "Type1a Cannon I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 1000, cooldown = 0):
        super(type1aCannon1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        shoot(var,self,ship1,ammunition_type.type1adefault,ships)

class type2aCannon1(system):
    def __init__ (self,globalVar,name = "Type2a Cannon I",minEnergy=0,maxEnergy=6,energy=0, maxCooldown = 300, cooldown = 0):
        super(type2aCannon1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        shoot(var,self,ship1,ammunition_type.type2adefault,ships)

class type3aCannon1(system):
    def __init__ (self,globalVar,name = "Type3a Cannon I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 1700, cooldown = 0):
        super(type3aCannon1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        shoot(var,self,ship1,ammunition_type.type3adefault,ships)

class gattlingLaser1(system):
    def __init__ (self,globalVar,name = "Gattling Laser I",minEnergy=0,maxEnergy=9,energy=0, maxCooldown = 60, cooldown = 0):
        super(gattlingLaser1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        shoot(var,self,ship1,ammunition_type.laser1adefault,ships)

class gattlingLaser2(system):
    def __init__ (self,globalVar,name = "Gattling Laser II",minEnergy=2,maxEnergy=8,energy=0, maxCooldown = 40, cooldown = 0):
        super(gattlingLaser2,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        shoot(var,self,ship1,ammunition_type.laser1adefault,ships)

class highEnergyLaser1(system):
    def __init__ (self,globalVar,name = "High Energy Laser I",minEnergy=4,maxEnergy=8,energy=0, maxCooldown = 800, cooldown = 0):
        super(highEnergyLaser1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        shoot(var,self,ship1,ammunition_type.highEnergyLaser1,ships)

class kinetic1(system):
    def __init__ (self,globalVar,name = "Kinetic cannon I",minEnergy=0,maxEnergy=7,energy=0, maxCooldown = 5, cooldown = 0):
        super(kinetic1,self).__init__(globalVar,name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,var,ship1,ships,shipLookup):
        shoot(var,self,ship1,ammunition_type.kinetic1,ships)
        shoot(var,self,ship1,ammunition_type.kinetic1,ships,10,10)
        shoot(var,self,ship1,ammunition_type.kinetic1,ships,-10,-10)
        shoot(var,self,ship1,ammunition_type.kinetic1,ships,0,10)


system_lookup = {
    "throttleBrake1": throttleBrake1,
    "type1aCannon1": type1aCannon1,
    "type2aCannon1": type2aCannon1,
    "type3aCannon1": type3aCannon1,
    "antiMissleSystem1": antiMissleSystem1,
    "antiMissleSystem2": antiMissleSystem2,
    "gattlingLaser1": gattlingLaser1,
    "gattlingLaser2": gattlingLaser2,
    "highEnergyLaser1": highEnergyLaser1,
    "kinetic1": kinetic1,
    "system": system,
    }
def shoot(var,system,ship1,ammunitionType,ships,offsetX=0,offsetY=0):    #newer than manageShots without strange interval system
        if(system.cooldown <= 0 and True):
            shipToShoot = 0
            minDist2 = 999999999
            for ship2 in ships:
                if(not ship1.owner == ship2.owner): # add teams if needed
                    distance2 = pow(ship1.xPos-ship2.xPos, 2)+pow(ship1.yPos-ship2.yPos, 2)
                    if(ship2.visible == TRUE and distance2 < (ship1.detectionRange*ship1.detectionRange) and distance2 < minDist2):
                        minDist2 = distance2
                        shipToShoot = ship2
            if(shipToShoot):
                createRocket(var,ship1,shipToShoot,ammunitionType,offsetX,offsetY)
                system.cooldown = system.maxCooldown
                    #     print(ship1.name + " fired " +
                    #           str(ship1.typesOfAmmunition[ship1.ammunitionChoice].name))
