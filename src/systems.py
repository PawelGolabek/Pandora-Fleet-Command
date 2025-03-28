from tkinter import IntVar, StringVar
from src.shipCombat import putTracer, createRocket,laser
from src.ammunitionType import *
import src.naglowek as naglowek

############################## SYSTEMS #############################################
class system(object):
    def __init__(self, id = 0, name = "system", category = 'module', minEnergy=0, maxEnergy=5,energy=0,
                           maxCooldown = 2000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 0, cooling = 2):
        self.id = id
        self.name = name
        self.category = category
        self.minEnergy = minEnergy
        self.maxEnergy = maxEnergy
        self.energy = energy
        self.integrity = integrity
        self.maxIntegrity = maxIntegrity
        self.maxCooldown = maxCooldown
        self.cooldown = cooldown
        self.mass = mass
        self.cost = cost
        self.cooling = cooling
        self.heat = 0.0
        self.coolUnits = 0
        self.heatUnits = 0
        self.heatDamageTicks = 0
        self.description = "default text"
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

class weapon(system):
    def __init__(self, id = 0,  name = "system", category = 'weapon', target = 0, minEnergy=0, maxEnergy=5,energy=0,
                     maxCooldown = 2000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 0, cooling = 2):
        super(weapon,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling) 
        self.target = target   
        self.ASButton = 0
        self.alphaStrike = False
        self.shotThisTurn = False
        self.description = "default weapon text"
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
    def setTarget(self,root,var1):
        self.target = (self.targetDict[self.variable.get()])
    def setTargetStr(self,var1):
        self.target = var1
    def setAS(self):
        self.alphaStrike = not self.alphaStrike


class mixedSystem(system):
    def __init__(self, id = 0,  name = "system", category = 'weapon', minEnergy=0, maxEnergy=5,energy=0,
                     maxCooldown = 2000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 0, cooling = 2):
        super(mixedSystem,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling) 
        self.ASButton = 0
        self.alphaStrike = False
        self.shotThisTurn = False
        self.description = "default mixed module text"
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
    def setAS(self):
        self.alphaStrike = not self.alphaStrike


class none(weapon):
    def __init__ (self, id = 0,  name = "noneSystem", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=0, energy=0,
                     maxCooldown = 10, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 0, cost = 0, cooling = 2):
        super(none,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = "no system in slot"

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        pass
    def activate(self,ship,var,gameRules,uiMetrics):
        pass
class throttleBrake1(system):
    def __init__ (self, id = 0, name = "Throttle Brake I", category = 'module', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 3000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 80, cooling = 2):
        super(throttleBrake1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Throttle Brake I:\nAllows you to slow down your \nship to make tighter turns \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nmass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        return
    def activate(self,ship,var,gameRules,uiMetrics):
        value = ship.maxSpeed/4
        ship.speed = ship.maxSpeed - self.energy*value
        putTracer(ship,var,gameRules,uiMetrics)
        pass


class stealth1(mixedSystem):
    def __init__ (self, id = 0, name = "Stealth I", category = 'mixed', minEnergy=1, maxEnergy=5, energy=0,
                     maxCooldown = 27000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 50, cost = 200, cooling = 2):
        super(stealth1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Stealth Generator I:\nMakes incoming missles loose their \ntarget and renders the ship \ncompletely invisible for a \nbrief ammount of time\n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nmass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            for missle in var.currentMissles:
                minDist = 9999999
                if(not missle.owner == ship1.owner and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist and missle.damage > 100 ):
                        minDist = dist
                        ship1.stealth = 300
                        for missle in var.currentMissles:
                            if(missle.target == ship1.id):
                                missle.looseTarget()
                        self.cooldown = self.maxCooldown
        return
    def activate(self,ship,var,gameRules,uiMetrics):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.minEnergyConsumption += self.minEnergy
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.minEnergyConsumption -= self.minEnergy

class stealth2(mixedSystem):
    def __init__ (self, id = 0, name = "Stealth II", category = 'mixed', minEnergy=2, maxEnergy=7, energy=0,
                     maxCooldown = 35000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 50, cost = 200, cooling = 2):
        super(stealth2,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Stealth Generator I:\nMakes incoming missles loose their \ntarget and renders the ship \ncompletely invisible for a \nbrief ammount of time\n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nmass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            for missle in var.currentMissles:
                minDist = 9999999
                if(not missle.owner == ship1.owner and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist and missle.damage > 100 ):
                        minDist = dist
                        ship1.stealth = 700
                        for missle in var.currentMissles:
                            if(missle.target == ship1.id):
                                missle.looseTarget()
                        self.cooldown = self.maxCooldown
        return
    def activate(self,ship,var,gameRules,uiMetrics):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.minEnergyConsumption += self.minEnergy
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.minEnergyConsumption -= self.minEnergy

class hullRepairSystem1(system):
    def __init__ (self, id = 0,  name = "Hull Repair I", category = 'module', minEnergy=0, maxEnergy=3,energy=0,
                     maxCooldown = 3000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 100, cooling = 2):
        super(hullRepairSystem1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Hull Repair System I:\nAllows you to repair damage dealt to your ship's Hull \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nmass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0):
            i=40
            while(ship1.hp != ship1.maxHp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown = self.maxCooldown

class hullRepairSystem2(system):
    def __init__ (self, id = 0, name = "Hull Repair II", category = 'module',minEnergy=0,maxEnergy=10,energy=0,
                     maxCooldown = 2000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 20, cost = 150, cooling = 2):
        super(hullRepairSystem2,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Hull Repair System II:\nAllows you to repair damage dealt to your ship's Hull \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nmass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and ship1.hp != ship1.maxHp):
            i=60
            while(ship1.hp != ship1.maxAp and i>0):
                ship1.hp+=1
                i-=1
            self.cooldown=self.maxCooldown

class antiMissleSystem1(system):
    def __init__ (self, id = 0, name = "Anti Missle I", category = 'module', minEnergy=0, maxEnergy=10, energy=0,
                     maxCooldown = 13000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 80, cooling = 2):
        super(antiMissleSystem1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Anti Missle System I: \nShoots down incoming enemy missles \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nmass: {}\ncost: {}").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            minDist = 9999999
            range = ship1.detectionRange
            closestEnemyMissle = 0
            range = range * range
            for missle in var.currentMissles:
                if(not missle.owner == ship1.owner and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist and missle.damage > 100):
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
    def __init__ (self, id = 0, name = "Anti Missle II", category = 'module', minEnergy=0, maxEnergy=10, energy=0,
                     maxCooldown = 12000, integrity = 400, cooldown = 0, maxIntegrity = 400, mass = 25, cost = 80, cooling = 2):
        super(antiMissleSystem2,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost)
        self.description = ("Anti Missle System II: \nShoots down incoming enemy missles \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            minDist = 9999999
            range = ship1.detectionRange
            closestEnemyMissle = 0
            range = range * range
            for missle in var.currentMissles:
                if(not missle.owner == ship1.owner and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist and missle.damage > 100 ):
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


class bolter1(weapon):
    def __init__ (self, id = 0, name = "Bolter1", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 3000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 40, cooling = 2):
        super(bolter1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Bolter I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
missle damage: 90 \n\
missle heat damage: 7.5 \
\nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.bolter,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 5

class bolter1C(bolter1):
    def __init__ (self, id = 0, name = "Bolter IC", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 3000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 40, cooling = 8):
        super(bolter1C,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Bolter IC: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
missle damage: 90 \n\
missle heat damage: 7.5 \
\nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)


class missleLauncher1(weapon):
    def __init__ (self, id = 0, name = "Missle Launcher I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=6, energy=0,
                     maxCooldown = 3000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 15, cost = 65, cooling = 2):
        super(missleLauncher1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Missle Launcher I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
missle damage: 160 \n\
missle heat damage: 10 \
\nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.missle,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 10

class atomicCannon1(weapon):
    def __init__ (self, id = 0, name = "Atomic Cannon I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 17000, integrity = 700, maxIntegrity = 700, cooldown = 0, mass = 30, cost = 160, cooling = 1):
        super(atomicCannon1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Atomic Cannon I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
missle damage: 1000 \n\
missle heat damage: 50\
\nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.nuke,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 100


class atomicCannon2(weapon):
    def __init__ (self, id = 0, name = "Atomic Cannon II", category = 'weapon', target = 'none', minEnergy=3, maxEnergy=5, energy=0,
                     maxCooldown = 17000, integrity = 1200, maxIntegrity = 1200, cooldown = 0, mass = 60, cost = 300, cooling = 4):
        super(atomicCannon2,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Atomic Cannon II: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
missle damage: 1000 \n\
missle heat damage: 50\
\nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.nuke,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 200



class incirination1Cannon1(weapon):
    def __init__ (self, id = 0, name = "Incirination I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=2, energy=0,
                     maxCooldown = 4000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 30, cost = 160, cooling = 5):
        super(incirination1Cannon1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Incirination Cannon I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
missle damage: 10 \n\
missle heat damage: 400\
\nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)


    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.incirination1adefault,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 120

class incirination1Cannon1C(incirination1Cannon1):
    def __init__ (self, id = 0, name = "Incirination I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=2, energy=0,
                     maxCooldown = 4000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 30, cost = 160, cooling = 12):
        super(incirination1Cannon1C,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Incirination Cannon IC: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
missle damage: 10 \n\
missle heat damage: 400\
\nmass: {}\ncost: {}\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)


class gattlingLaser1(weapon):
    def __init__ (self, id = 0, name = "Gattling Laser I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=9, energy=0,
                     maxCooldown = 600, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 100, cooling = 4):
        super(gattlingLaser1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Gattling Laser I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \n\
laser damage: 1 \n\
laser heat damage: 6 \n\
mass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)


    def trigger(self,var,ship1,ships,shipLookup,uiMetrics): 
        if(self.cooldown <= 0.0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.laser1adefault,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 20

class gattlingLaser1C(gattlingLaser1):
    def __init__ (self, id = 0, name = "Gattling Laser Ic", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=9, energy=0,
                     maxCooldown = 600, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 100, cooling = 12):
        super(gattlingLaser1C,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling) 
        self.description = ("Gattling Laser IC: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \n\
laser damage: 1 \n\
laser heat damage: 6 \n\
mass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)


class gattlingLaser2(weapon):
    def __init__ (self, id = 0, name = "Gattling Laser II", category = 'weapon', target = 'none', minEnergy=2, maxEnergy=8, energy=0,
                     maxCooldown = 400, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 15, cost = 110, cooling = 4):
        super(gattlingLaser2,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Gattling Laser II: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
laser damage: 1 \n\
laser heat damage: 6 \n\
mass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.laser1adefault,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 18
        
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.minEnergyConsumption += self.minEnergy
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.minEnergyConsumption -= self.minEnergy

class highEnergyLaser1(weapon):
    def __init__ (self, id = 0,  name = "High Energy Laser I", category = 'weapon', target = 'none', minEnergy=4, maxEnergy=8, energy=0,
                     maxCooldown = 8000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 50, cooling = 6):
        super(highEnergyLaser1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("High Energy Laser I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \n\
laser damage: 10 \n\
laser heat damage: 200 \n\
mass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if (shoot(var,self,ship1,ammunition_type.highEnergyLaser1,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 120

class kinetic1(weapon):
    def __init__ (self, id = 0, name = "Kinetic cannon I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=7, energy=0,
                     maxCooldown=300, integrity = 300, maxIntegrity = 300, cooldown=0, mass=30, cost = 60, cooling = 2):
        super(kinetic1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Kinetic Cannon I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \n\
kinetic damage: 2 \n\
kinetic heat damage: 1.2 \n\
mass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.kinetic1,ships,uiMetrics,shipLookup)):
                self.cooldown = self.maxCooldown
                self.heat += 5
        if(self.cooldown == (self.maxCooldown - 5) or self.cooldown == (self.maxCooldown - 10)):
            shoot(var,self,ship1,ammunition_type.kinetic1,ships,uiMetrics,shipLookup)
            self.heat += 5


class kinetic2(kinetic1):
    def __init__ (self, id = 0, name = "Kinetic cannon II", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=7, energy=0,
                     maxCooldown=200, integrity = 800, maxIntegrity = 300, cooldown=0, mass=30, cost = 150, cooling = 4):
        super(kinetic2,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Kinetic Cannon II: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \n\
kinetic damage: 2 \n\
kinetic heat damage: 1.2 \n\
mass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)


class kinetic3(kinetic1):
    def __init__ (self, id = 0, name = "Kinetic cannon III", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=7, energy=0,
                     maxCooldown=100, integrity = 800, maxIntegrity = 300, cooldown=0, mass=30, cost = 250, cooling = 6):
        super(kinetic3,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Kinetic Cannon III: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \n\
kinetic damage: 2 \n\
kinetic heat damage: 1.2 \n\
mass: {}\ncost: {}\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling,self.mass,self.cost)


def checkAlphaStrikeReadiness(ship):
    for system in ship.systemSlots:
        if(system.category == 'weapon'):
            if(not system.alphaStrike or system.cooldown <= 0 or system.shotThisTurn):
                continue
            else:
                return False
    return True

def shoot(var,system,ship,ammunitionType,ships,uiMetrics,shipLookup,offsetX=0,offsetY=0):
    shipToShoot = 0
    minDist2 = 999999999
    break1 = False
    ready = True
    if(system.alphaStrike):
        ready = checkAlphaStrikeReadiness(ship)
    if(ready):
        for ship2 in ships:
            if(not ship.owner == ship2.owner): # add teams if needed
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
                    x = element.x
                    y = element.y
                    enemyX = ship2.xPos
                    enemyY = ship2.yPos
                    distance2 = (x-enemyX)*(x-enemyX) + (y-enemyY)*(y-enemyY)
                    if(ship2.visible == True and distance2 < (ship.detectionRange*ship.detectionRange)):
                        if(distance2 < minDist2):
                            minDist2 = distance2
                            shipToShoot = ship2
                        if(ship2.name == ship.target):
                            if(ship.targetOnly):
                                shipToShoot = ship2
                                break1 = True
                                break
                            minDist2 = distance2
                if(break1):
                    break
        if(not(ship2.name == ship.target) and ship.targetOnly):
            shipToShoot = 0
        if(shipToShoot):
            system.shotThisTurn = True
            if(shipToShoot.name == ship.target):
                createRocket(var,ship,shipToShoot,system.target,ammunitionType,offsetX,offsetY)
            else:
                createRocket(var,ship,shipToShoot,-1,ammunitionType,offsetX,offsetY)
            return True
        return False
    else:
        return False

def declareGlobalSystems():
    naglowek.systemLookup = {           #for system creation
    "throttleBrake1": throttleBrake1,
    "stealth1": stealth1,
    "stealth2": stealth2,
    "bolter1": bolter1,
    "bolter1C": bolter1C,
    "missleLauncher1": missleLauncher1,
    "atomicCannon1": atomicCannon1,
    "atomicCannon2": atomicCannon2,
    "incirination1Cannon1": incirination1Cannon1,
    "incirination1Cannon1C": incirination1Cannon1C,
    "antiMissleSystem1": antiMissleSystem1,
    "antiMissleSystem2": antiMissleSystem2,
    "gattlingLaser1": gattlingLaser1,
    "gattlingLaser2": gattlingLaser2,
    "gattlingLaser1C": gattlingLaser1C,
    "highEnergyLaser1": highEnergyLaser1,
    "hullRepairSystem1": hullRepairSystem1,
    "hullRepairSystem2": hullRepairSystem2,
    "kinetic1": kinetic1,
    "kinetic2": kinetic2,
    "kinetic3": kinetic3,
    "system": system,
    "none": none,
    }
    naglowek.allSystemsList = [           #for dropdown menus in editor
        'none',
        "throttleBrake1",
        "stealth1",
        "stealth2",
        "bolter1",
        "missleLauncher1",
        "atomicCannon1",
        "atomicCannon2",
        "incirination1Cannon1",
        "antiMissleSystem1",
        "antiMissleSystem2",
        "gattlingLaser1",
        "gattlingLaser2",
        "highEnergyLaser1",
        "hullRepairSystem1",
        "hullRepairSystem2",
        "kinetic1",
        "kinetic2",
        "kinetic3",
        ]
    (naglowek.systemStatsBlueprints).throttleBrake1 = throttleBrake1()  
    (naglowek.systemStatsBlueprints).stealth1 = stealth1()         
    (naglowek.systemStatsBlueprints).stealth2 = stealth2()         
    (naglowek.systemStatsBlueprints).bolter1 = bolter1()
    (naglowek.systemStatsBlueprints).missleLauncher1 = missleLauncher1()
    (naglowek.systemStatsBlueprints).atomicCannon1 = atomicCannon1()
    (naglowek.systemStatsBlueprints).atomicCannon2 = atomicCannon2()
    (naglowek.systemStatsBlueprints).incirination1Cannon1 = incirination1Cannon1()
    (naglowek.systemStatsBlueprints).antiMissleSystem1 = antiMissleSystem1()
    (naglowek.systemStatsBlueprints).antiMissleSystem2 = antiMissleSystem2()
    (naglowek.systemStatsBlueprints).gattlingLaser1 = gattlingLaser1()
    (naglowek.systemStatsBlueprints).gattlingLaser2 = gattlingLaser2()
    (naglowek.systemStatsBlueprints).highEnergyLaser1 = highEnergyLaser1()
    (naglowek.systemStatsBlueprints).hullRepairSystem1 = hullRepairSystem1()
    (naglowek.systemStatsBlueprints).hullRepairSystem2 = hullRepairSystem2()
    (naglowek.systemStatsBlueprints).kinetic1 = kinetic1()
    (naglowek.systemStatsBlueprints).kinetic2 = kinetic2()
    (naglowek.systemStatsBlueprints).kinetic3 = kinetic3()
    (naglowek.systemStatsBlueprints).system = system()
    (naglowek.systemStatsBlueprints).none = none()

    naglowek.systemStats = {                                                  #to lookup statistics without creating
        'none': (naglowek.systemStatsBlueprints).none,
        "throttleBrake1": (naglowek.systemStatsBlueprints).throttleBrake1,
        "stealth1": (naglowek.systemStatsBlueprints).stealth1,
        "stealth2": (naglowek.systemStatsBlueprints).stealth2,
        "bolter1": (naglowek.systemStatsBlueprints).bolter1,
        "missleLauncher1": (naglowek.systemStatsBlueprints).missleLauncher1,
        "atomicCannon1": (naglowek.systemStatsBlueprints).atomicCannon1,
        "atomicCannon2": (naglowek.systemStatsBlueprints).atomicCannon2,
        "incirination1Cannon1":(naglowek.systemStatsBlueprints).incirination1Cannon1,
        "antiMissleSystem1": (naglowek.systemStatsBlueprints).antiMissleSystem1,
        "antiMissleSystem2": (naglowek.systemStatsBlueprints).antiMissleSystem2,
        "gattlingLaser1": (naglowek.systemStatsBlueprints).gattlingLaser1,
        "gattlingLaser2": (naglowek.systemStatsBlueprints).gattlingLaser2,
        "highEnergyLaser1": (naglowek.systemStatsBlueprints).highEnergyLaser1,
        "hullRepairSystem1": (naglowek.systemStatsBlueprints).hullRepairSystem1,
        "hullRepairSystem2": (naglowek.systemStatsBlueprints).hullRepairSystem2,
        "kinetic1": (naglowek.systemStatsBlueprints).kinetic1,
        "kinetic2": (naglowek.systemStatsBlueprints).kinetic2,
        "kinetic3": (naglowek.systemStatsBlueprints).kinetic3,
        "system": (naglowek.systemStatsBlueprints).system 
    }

