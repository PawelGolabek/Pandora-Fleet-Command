from tkinter import IntVar, StringVar
import winsound
from functools import partial
import simpleaudio as sa
import tkinter as tk
import tkinter.ttk as ttk


from src.editor.ammunitionType import *
import src.settings as settings
from src.objects.ship import decoyShip
from src.shipCombat import putTracer, createRocket,laser

def loadSounds(var):
    var.bolterSound = sa.WaveObject.from_wave_file("sounds/bolter.wav")
    var.kineticSound = sa.WaveObject.from_wave_file("sounds/kinetic.wav")
    
def play_sound(var):
    if(var.audioOn):
        var.bolterSound.play()
    #play_obj.wait_done()

def play_sound_kinetic(var):
    if(var.audioOn):
        var.kineticSound.play()
    #play_obj.wait_done()

def play_sound_flare(var):
    if(var.audioOn):
        x=10
   #     var.flareSound.play()          # not in game yet
    #play_obj.wait_done()

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
        self.audioVar = 0
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        pass
    def activate(self,ship,var,gameRules,uiMetrics,uiElements):
        pass
    def onAdding(self,ship):
        ship.maxEnergy -= self.minEnergy
        ship.mass += self.mass
        ship.cost += self.cost
    def onRemoving(self,ship):
        ship.maxEnergy += self.minEnergy
        ship.mass -= self.mass
        ship.cost -= self.cost
    def showInfo(self,event):
        window = tk.Toplevel()
        window.config(bg="#1e1e1e")
        label = ttk.Label(window, style = 'Grey.TLabel', text=(self.description))
        window.config(width = 300,height = 500)
        def closeWindow(window):
            window.destroy()
        closeWindowCommand = partial(closeWindow,window)
        frame = tk.Frame(window)
        frame.config(bg="#4582ec", width=2, height=2,padx=1)
        button = tk.Button(frame, text = "Ok",command=closeWindowCommand)
        button.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
        label.place(x = 100, y = 0)
        frame.place(relx=0.5, rely=1,anchor=tk.S)
        button.pack()


class weapon(system):
    def __init__(self, id = 0,  name = "system", category = 'weapon', target = "no target", minEnergy=0, maxEnergy=5,energy=0,
                     maxCooldown = 2000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 0, cooling = 2):
        super(weapon,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling) 
        self.target = target   
        self.ASButton = 0
        self.alphaStrike = False
        self.hold = False
        self.delay = False
        self.desynchronise = False
        self.shotThisTurn = False
        self.description = "default weapon text"
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        pass
    def activate(self,ship,var,gameRules,uiMetrics,uiElements):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy -= self.minEnergy
        ship.minEnergyConsumption += self.minEnergy
        ship.maxEnergyConsumption += self.maxEnergy
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy += self.minEnergy
        ship.minEnergyConsumption -= self.minEnergy
        ship.maxEnergyConsumption -= self.maxEnergy
    def setTarget(self,root,var1):
        self.target = (self.targetDict[self.variable.get()])
    def setTargetStr(self,var1):
        self.target = var1
    def setAS(self):
        self.alphaStrike = not self.alphaStrike
    def setDesynchronise(self):
        self.desynchronise = not self.desynchronise
    def setHold(self):
        self.hold = not self.hold
    def setDelay(self):
        self.delay = not self.delay


class mixedSystem(system):
    def __init__(self, id = 0,  name = "system", category = 'weapon', minEnergy=0, maxEnergy=5,energy=0,
                     maxCooldown = 2000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 0, cooling = 2):
        super(mixedSystem,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling) 
        self.ASButton = 0
        self.alphaStrike = False
        self.shotThisTurn = False
        self.description = "default mixed module text"
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        pass
    def activate(self,ship,var,gameRules,uiMetrics,uiElements):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergyConsumption += self.maxEnergy
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergyConsumption -= self.maxEnergy
    def setAS(self):
        self.alphaStrike = not self.alphaStrike


class none(weapon):
    def __init__ (self, id = 0,  name = "noneSystem", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=0, energy=0,
                     maxCooldown = 10, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 0, cost = 0, cooling = 2):
        super(none,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = "no system in slot"

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        pass
    def activate(self,ship,var,gameRules,uiMetrics,uiElements):
        pass

    
class throttleBrake1(system):
    def __init__ (self, id = 0, name = "Throttle Brake I", category = 'module', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 3000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 80, cooling = 2):
        super(throttleBrake1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Throttle Brake I:\nAllows you to slow\n down your ship to\nmake tighter turns \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \nmass: {}\ncost: {}\n").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        return
    def activate(self,ship,var,gameRules,uiMetrics,uiElements):
        value = ship.maxSpeed/4
        ship.speed = ship.maxSpeed - self.energy*value
        putTracer(ship,var,gameRules,uiMetrics)
        pass


class stealth1(mixedSystem):
    def __init__ (self, id = 0, name = "Stealth I", category = 'mixed', minEnergy=1, maxEnergy=5, energy=0,
                     maxCooldown = 27000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 50, cost = 400, cooling = 2):
        super(stealth1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Stealth Generator I:\nMakes incoming missles loose their \ntarget and renders the ship \ncompletely invisible for a \nbrief ammount of time\n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \nmass: {}\ncost: {}\n\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and ship1.stealth == 0):
            for missle in var.currentMissles:
                minDist = 9999999
                if(missle.target == ship1.id and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist and missle.damage >= 90 ):
                        minDist = dist
                        ship1.stealth = 300
                        for missle in var.currentMissles:
                            if(missle.target == ship1.id):
                                missle.looseTarget()
                        self.cooldown = self.maxCooldown
        return
    def activate(self,ship,var,gameRules,uiMetrics,uiElements):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy -= self.minEnergy
        ship.minEnergyConsumption += self.minEnergy
        ship.maxEnergyConsumption += self.maxEnergy
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost
        ship.maxEnergy += self.minEnergy
        ship.minEnergyConsumption -= self.minEnergy
        ship.maxEnergyConsumption -= self.maxEnergy

class stealth2(mixedSystem):
    def __init__ (self, id = 0, name = "Stealth II", category = 'mixed', minEnergy=2, maxEnergy=7, energy=0,
                     maxCooldown = 35000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 50, cost = 500, cooling = 2):
        super(stealth2,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Stealth Generator I:\nMakes incoming missles loose their \ntarget and renders the ship \ncompletely invisible for a \nbrief ammount of time\n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \nmass: {}\ncost: {}\n\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and ship1.stealth == 0):
            for missle in var.currentMissles:
                minDist = 9999999
                if(missle.target == ship1.id and not missle.sort == "laser"):
                    xDist = missle.xPos - ship1.xPos
                    yDist = missle.yPos - ship1.yPos
                    dist = xDist * xDist + yDist * yDist
                    if(minDist > dist and missle.damage >= 90 ):
                        minDist = dist
                        ship1.stealth = 700
                        for missle in var.currentMissles:
                            if(missle.target == ship1.id):
                                missle.looseTarget()
                        self.cooldown = self.maxCooldown
        return
    def activate(self,ship,var,gameRules,uiMetrics,uiElements):
        pass
    def onAdding(self,ship):
        ship.mass += self.mass
        ship.cost += self.cost
        ship.maxEnergy -= self.minEnergy
        ship.minEnergyConsumption += self.minEnergy
        ship.maxEnergyConsumption += self.maxEnergy
    def onRemoving(self,ship):
        ship.mass -= self.mass
        ship.cost -= self.cost        
        ship.maxEnergy += self.minEnergy
        ship.minEnergyConsumption -= self.minEnergy
        ship.maxEnergyConsumption -= self.maxEnergy

class hullRepairSystem1(system):
    def __init__ (self, id = 0,  name = "Hull Repair I", category = 'module', minEnergy=0, maxEnergy=3,energy=0,
                     maxCooldown = 3000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 100, cooling = 2):
        super(hullRepairSystem1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Hull Repair System I:\nAllows you to repair damage dealt to your ship's Hull \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \nmass: {}\ncost: {}\n\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0):
            ticks = 40
            while(ship1.hp != ship1.maxHp and ticks>0):
                ship1.hp += 1
                ticks-=1
            self.cooldown = self.maxCooldown

class hullRepairSystem2(system):
    def __init__ (self, id = 0, name = "Hull Repair II", category = 'module',minEnergy=0,maxEnergy=10,energy=0,
                     maxCooldown = 2000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 20, cost = 150, cooling = 2):
        super(hullRepairSystem2,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Hull Repair System II:\nAllows you to repair damage dealt to your ship's Hull \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \nmass: {}\ncost: {}\n\
").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and ship1.hp != ship1.maxHp):
            ticks = 60
            while(ship1.hp != ship1.maxHp and ticks > 0):
                ship1.hp+=1
                ticks -= 1
            self.cooldown=self.maxCooldown

class antiMissleSystem1(system):
    def __init__ (self, id = 0, name = "Anti Missle I", category = 'module', minEnergy=0, maxEnergy=10, energy=0,
                     maxCooldown = 13000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 140, cooling = 2):
        super(antiMissleSystem1,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Anti Missle System I: \nShoots down incoming\nenemy missles \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \nmass: {}\ncost: {}\n").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
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
                    if(minDist > dist and missle.damage >= 90):
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
                     maxCooldown = 12000, integrity = 400, cooldown = 0, maxIntegrity = 400, mass = 25, cost = 180, cooling = 2):
        super(antiMissleSystem2,self).__init__(id,name,category,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost)
        self.description = ("Anti Missle System II: \nShoots down incoming\nenemy missles \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \nmass: {}\ncost: {}\n\
        ").format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)
    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
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
                    if(minDist > dist and missle.damage >= 90 ):
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

class flare1(weapon):
    def __init__ (self, id = 0, name = "Flare1", category = 'weapon', target = 'none', minEnergy=1, maxEnergy=1, energy=0,
                     maxCooldown = 7000, integrity = 100, maxIntegrity = 100, cooldown = 0, mass = 10, cost = 10, cooling = 5):
        super(flare1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Flare I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {} \nmass: {}\ncost: {}\n\
        " + ammunition_type.flare.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.flare,ships,uiMetrics,shipLookup,uiElements)):
                # Call the function to play the sound
                play_sound_flare(var)
                self.cooldown = self.maxCooldown
                self.heat += 5


class bolter1(weapon):
    def __init__ (self, id = 0, name = "Bolter1", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 3000, integrity = 600, maxIntegrity = 600, cooldown = 0, mass = 10, cost = 40, cooling = 3):
        super(bolter1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Bolter I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {} \nmass: {}\ncost: {}\n\
        " + ammunition_type.bolter.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.bolter,ships,uiMetrics,shipLookup,uiElements)):
                # Call the function to play the sound
                play_sound(var)
                self.cooldown = self.maxCooldown
                self.heat += 5

class bolter1C(bolter1):
    def __init__ (self, id = 0, name = "Bolter IC", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 3000, integrity = 600, maxIntegrity = 600, cooldown = 0, mass = 10, cost = 90, cooling = 8):
        super(bolter1C,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Bolter IC: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {} \nmass: {}\ncost: {}\n\
        " + ammunition_type.bolter.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)


class bolter2(weapon):
    def __init__ (self, id = 0, name = "Bolter2", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 3000, integrity = 800, maxIntegrity = 800, cooldown = 0, mass = 10, cost = 60, cooling = 3):
        super(bolter2,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Bolter II: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {} \nmass: {}\ncost: {}\n\
        " + ammunition_type.bolter.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.bolter,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 5


class missleLauncher1(weapon):
    def __init__ (self, id = 0, name = "Missle Launcher I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=6, energy=0,
                     maxCooldown = 3000, integrity = 200, maxIntegrity = 200, cooldown = 0, mass = 15, cost = 65, cooling = 2):
        super(missleLauncher1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Missle Launcher I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \nreload time: {} \nmass: {}\ncost: {}\n\
        " + ammunition_type.missle.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.missle,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 10

class atomicCannon1(weapon):
    def __init__ (self, id = 0, name = "Atomic Cannon I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=3, energy=0,
                     maxCooldown = 17000, integrity = 700, maxIntegrity = 700, cooldown = 0, mass = 30, cost = 360, cooling = 3):
        super(atomicCannon1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Atomic Cannon I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {} \nmass: {}\ncost: {}\n\
        " + ammunition_type.nuke.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.nuke,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 100


class atomicCannon2(weapon):
    def __init__ (self, id = 0, name = "Atomic Cannon II", category = 'weapon', target = 'none', minEnergy=3, maxEnergy=5, energy=0,
                     maxCooldown = 17000, integrity = 1200, maxIntegrity = 1200, cooldown = 0, mass = 60, cost = 600, cooling = 4):
        super(atomicCannon2,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Atomic Cannon II: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {} \nmass: {}\ncost: {}\n\
        " + ammunition_type.nuke.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.nuke,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 200



class incirination1Cannon1(weapon):
    def __init__ (self, id = 0, name = "Incirination I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=2, energy=0,
                     maxCooldown = 4000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 50, cost = 460, cooling = 5):
        super(incirination1Cannon1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Incirination Cannon I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {}\nmass: {}\ncost: {}\n\
        " + ammunition_type.incirination1adefault.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)


    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.incirination1adefault,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 120

class incirination1Cannon1C(incirination1Cannon1):
    def __init__ (self, id = 0, name = "Incirination I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=2, energy=0,
                     maxCooldown = 4000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 50, cost = 600, cooling = 12):
        super(incirination1Cannon1C,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Incirination Cannon IC: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}\nreload time: {}\
\nmass: {}\ncost: {}\n\
        " + ammunition_type.incirination1adefault.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)


class gattlingLaser1(weapon):
    def __init__ (self, id = 0, name = "Gattling Laser I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=4, energy=0,
                     maxCooldown = 800, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 200, cooling = 4):
        super(gattlingLaser1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Gattling Laser I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \n\
mass: {}\ncost: {}\n\
" + ammunition_type.laser1adefault.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)


    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements): 
        if(self.cooldown <= 0.0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.laser1adefault,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 8

class gattlingLaser1C(gattlingLaser1):
    def __init__ (self, id = 0, name = "Gattling Laser Ic", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=4, energy=0,
                     maxCooldown = 800, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 10, cost = 300, cooling = 12):
        super(gattlingLaser1C,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling) 
        self.description = ("Gattling Laser IC: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \n\
mass: {}\ncost: {}\n\
" + ammunition_type.laser1adefault.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)


class gattlingLaser2(weapon):
    def __init__ (self, id = 0, name = "Gattling Laser II", category = 'weapon', target = 'none', minEnergy=2, maxEnergy=4, energy=0,
                     maxCooldown = 500, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 25, cost = 350, cooling = 4):
        super(gattlingLaser2,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = ("Gattling Laser II: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {}  \n\
mass: {}\ncost: {}\n\
" + ammunition_type.laser1adefault.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.laser1adefault,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 8
        
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
                     maxCooldown = 8000, integrity = 300, maxIntegrity = 300, cooldown = 0, mass = 100, cost = 2000, cooling = 6):
        super(highEnergyLaser1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity,  cooldown, mass, cost, cooling)
        self.description = (
"High Energy Laser I: \nWeapon System \n\
integrity: {} \n\
min energy: {} \n\
max energy: {}\n\
cooling: {} \nreload time: {} \n\
mass: {}\ncost: {}\n\
" + ammunition_type.highEnergyLaser1.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown,
          self.mass,self.cost
)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if (shoot(var,self,ship1,ammunition_type.highEnergyLaser1,ships,uiMetrics,shipLookup,uiElements)):
                self.cooldown = self.maxCooldown
                self.heat += 120

class kinetic1(weapon):
    def __init__ (self, id = 0, name = "Kinetic cannon I", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=4, energy=0,
                     maxCooldown=1500, integrity = 300, maxIntegrity = 300, cooldown=0, mass=30, cost = 200, cooling = 2):
        super(kinetic1,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Kinetic Cannon I: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \n\
mass: {}\ncost: {}\n\
" + ammunition_type.kinetic1.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown, self.mass,self.cost)

    def trigger(self,var,ship1,ships,shipLookup,uiMetrics,uiElements):
        if(self.cooldown <= 0 and not ship1.stealth):
            if(shoot(var,self,ship1,ammunition_type.kinetic1,ships,uiMetrics,shipLookup,uiElements)):
                if(self.audioVar > 0):
                    play_sound_kinetic(var)
                  #  self.audioVar-=2
                self.audioVar += 1
                self.cooldown = self.maxCooldown
                self.heat += 1
        if((self.cooldown == (self.maxCooldown - 5) or self.cooldown == (self.maxCooldown - 10)) and not ship1.stealth ):
            if(self.audioVar > 0):
                play_sound_kinetic(var)
               # self.audioVar-=2
            shoot(var,self,ship1,ammunition_type.kinetic1,ships,uiMetrics,shipLookup,uiElements)
            self.heat += 1


class kinetic2(kinetic1):
    def __init__ (self, id = 0, name = "Kinetic cannon II", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=4, energy=0,
                     maxCooldown=1000, integrity = 800, maxIntegrity = 800, cooldown=0, mass=30, cost = 250, cooling = 4):
        super(kinetic2,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Kinetic Cannon II: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \n\
mass: {}\ncost: {}\n\
" + ammunition_type.kinetic1.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown, self.mass,self.cost)


class kinetic3(kinetic1):
    def __init__ (self, id = 0, name = "Kinetic cannon III", category = 'weapon', target = 'none', minEnergy=0, maxEnergy=4, energy=0,
                     maxCooldown=500, integrity = 800, maxIntegrity = 800, cooldown=0, mass=30, cost = 400, cooling = 6):
        super(kinetic3,self).__init__(id,name,category,target,minEnergy,maxEnergy,energy, maxCooldown, integrity, maxIntegrity, cooldown, mass, cost, cooling)
        self.description = ("Kinetic Cannon III: \nWeapon System \n\
integrity: {} \nmin energy: {} \nmax energy: {}\ncooling: {} \nreload time: {} \n\
mass: {}\ncost: {}\n\
" + ammunition_type.kinetic1.description).format(self.integrity,self.minEnergy,self.maxEnergy,self.cooling, maxCooldown, self.mass,self.cost)


def checkAlphaStrikeReadiness(ship):
    for system in ship.systemSlots:
        if(system.category == 'weapon'):
            if(not system.alphaStrike or system.cooldown <= 0 or system.shotThisTurn):
                continue
            else:
                return False
    return True

def shoot(var,system,ship,ammunitionType,ships,uiMetrics,shipLookup,uiElements,offsetX=0,offsetY=0):
    shipToShoot = decoyShip()
    minDist2 = 999999999
    break1 = False
    ready = True
    if(system.alphaStrike):
        ready = checkAlphaStrikeReadiness(ship)
    if(system.hold):
        ready = False
    if(system.delay and uiElements.timeElapsedProgressBar['value'] < var.turnLength/2):
        ready = False
    if(ship.desynchronisedFired and system.desynchronise):
        ready = False
    if(ready):
        for ship2 in ships:
            if(not ship.owner == ship2.owner): # add teams if needed
                list = []
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos
                ghostShip.y = ship.yPos
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship.yPos
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos - uiMetrics.canvasWidth
                ghostShip.y = ship.yPos
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos 
                ghostShip.y = ship.yPos + uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos - var.left
                ghostShip.y = ship.yPos - uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos - uiMetrics.canvasWidth
                ghostShip.y = ship.yPos - uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship.yPos - uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship.xPos - uiMetrics.canvasWidth
                ghostShip.y = ship.yPos + uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
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
    #    if(not shipToShoot.name == ""):
    #        print(str(shipToShoot) + " " + str(ship.target) + " " + str(ship.targetOnly))
        if(not(shipToShoot.name == ship.target) and ship.targetOnly):
            shipToShoot = decoyShip()
            shipToShoot.name = ""
        if(not shipToShoot.name == "" and not shipToShoot.stealth):
            system.shotThisTurn = True
            if(shipToShoot.name == ship.target):
                createRocket(var,ship,shipToShoot,system.target,ammunitionType,offsetX,offsetY)    #check if target only works correctly on targets other than standard
                ship.desynchronisedFired = system.maxCooldown/5
                if(ship.desynchronisedFired > 120):
                    ship.desynchronisedFired = 120
            else:
                createRocket(var,ship,shipToShoot,-1,ammunitionType,offsetX,offsetY)
                ship.desynchronisedFired = system.maxCooldown/5
                if(ship.desynchronisedFired > 120):
                    ship.desynchronisedFired = 120
            return True
        return False
    else:
        return False




def declareGlobalSystems():
    settings.systemLookup = {           #for system creation for ships
    "throttleBrake1": throttleBrake1,
    "stealth1": stealth1,
    "stealth2": stealth2,
    "flare1": flare1,
    "bolter1": bolter1,
    "bolter2": bolter2,
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
    settings.allSystemsList = [           #for dropdown menus in editor ( don't have to include all)
        'none',
        "flare1",
        "throttleBrake1",
        "bolter1",
        "bolter2",
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
        "stealth1",
        "stealth2",
        ]
    (settings.systemStatsBlueprints).throttleBrake1 = throttleBrake1()  
    (settings.systemStatsBlueprints).stealth1 = stealth1()         
    (settings.systemStatsBlueprints).stealth2 = stealth2()         
    (settings.systemStatsBlueprints).flare1 = flare1()      
    (settings.systemStatsBlueprints).bolter1 = bolter1()   
    (settings.systemStatsBlueprints).bolter2 = bolter2()
    (settings.systemStatsBlueprints).missleLauncher1 = missleLauncher1()
    (settings.systemStatsBlueprints).atomicCannon1 = atomicCannon1()
    (settings.systemStatsBlueprints).atomicCannon2 = atomicCannon2()
    (settings.systemStatsBlueprints).incirination1Cannon1 = incirination1Cannon1()
    (settings.systemStatsBlueprints).antiMissleSystem1 = antiMissleSystem1()
    (settings.systemStatsBlueprints).antiMissleSystem2 = antiMissleSystem2()
    (settings.systemStatsBlueprints).gattlingLaser1 = gattlingLaser1()
    (settings.systemStatsBlueprints).gattlingLaser2 = gattlingLaser2()
    (settings.systemStatsBlueprints).highEnergyLaser1 = highEnergyLaser1()
    (settings.systemStatsBlueprints).hullRepairSystem1 = hullRepairSystem1()
    (settings.systemStatsBlueprints).hullRepairSystem2 = hullRepairSystem2()
    (settings.systemStatsBlueprints).kinetic1 = kinetic1()
    (settings.systemStatsBlueprints).kinetic2 = kinetic2()
    (settings.systemStatsBlueprints).kinetic3 = kinetic3()
    (settings.systemStatsBlueprints).system = system()
    (settings.systemStatsBlueprints).none = none()

    settings.systemStats = {                                                  #to lookup statistics without creating (all)
        'none': (settings.systemStatsBlueprints).none,
        "throttleBrake1": (settings.systemStatsBlueprints).throttleBrake1,
        "stealth1": (settings.systemStatsBlueprints).stealth1,
        "stealth2": (settings.systemStatsBlueprints).stealth2,
        "flare1": (settings.systemStatsBlueprints).flare1,
        "bolter1": (settings.systemStatsBlueprints).bolter1,
        "bolter2": (settings.systemStatsBlueprints).bolter2,
        "missleLauncher1": (settings.systemStatsBlueprints).missleLauncher1,
        "atomicCannon1": (settings.systemStatsBlueprints).atomicCannon1,
        "atomicCannon2": (settings.systemStatsBlueprints).atomicCannon2,
        "incirination1Cannon1":(settings.systemStatsBlueprints).incirination1Cannon1,
        "antiMissleSystem1": (settings.systemStatsBlueprints).antiMissleSystem1,
        "antiMissleSystem2": (settings.systemStatsBlueprints).antiMissleSystem2,
        "gattlingLaser1": (settings.systemStatsBlueprints).gattlingLaser1,
        "gattlingLaser2": (settings.systemStatsBlueprints).gattlingLaser2,
        "highEnergyLaser1": (settings.systemStatsBlueprints).highEnergyLaser1,
        "hullRepairSystem1": (settings.systemStatsBlueprints).hullRepairSystem1,
        "hullRepairSystem2": (settings.systemStatsBlueprints).hullRepairSystem2,
        "kinetic1": (settings.systemStatsBlueprints).kinetic1,
        "kinetic2": (settings.systemStatsBlueprints).kinetic2,
        "kinetic3": (settings.systemStatsBlueprints).kinetic3,
        "system": (settings.systemStatsBlueprints).system 
    }

