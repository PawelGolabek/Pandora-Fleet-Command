import tkinter as tk
import random

import src.naglowek as naglowek

class ship():
    def __init__(self,var, name="MSS Artemis", owner="ai2", target=0,
                 hp=0, maxHp=None, ap=0, maxAp=None, shields=0, maxShields = 0, xPos=300, yPos=300,energy = 0,
                 ammunitionChoice=0, ammunitionNumberChoice=0, systemSlots = [], systemStatus = [],
                 detectionRange=1, xDir=0, yDir=1, turnRate=0, ghostPoints = [], signatures = [], speed=0, maxSpeed = 0,
                 outlineColor="red",id = 9999,signatureCounter=0, stance='rush',color = "red"):
        # Init info                                             
        self.name = name
        self.owner = owner
        self.target = target
        self.xPos = xPos
        self.yPos = yPos

        self.energyLimit = energy
        self.tmpEnergyLimit = energy
        self.energy = energy
        self.ammunitionChoice = ammunitionChoice
        self.ammunitionNumberChoice = ammunitionNumberChoice
        self.signatureCounter = signatureCounter
        self.systemSlots = []
        self.declareSystemSlots(systemSlots,systemStatus)

        self.detectionRange = detectionRange
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.ghostPoints = ghostPoints
        self.signatures = signatures
        self.speed = round(float(speed))
        self.maxSpeed = round(float(maxSpeed))
        self.outlineColor = outlineColor
        self.hp = hp
        if(maxHp == None):
            self.maxHp = hp
        else:
            self.maxHp = maxHp
        self.ap = ap
        if(maxAp == None):
            self.maxAp = ap
        else:
            self.maxAp = maxAp
        self.declareShieldState(shields,maxShields,var)
        # Mid-round info
        self.visible = False
        self.moveOrderX = xPos+0.01
        self.moveOrderY = yPos+0.01
        self.id = id
        self.signatureCounter = 0
        self.killed = False
        self.stealth = 0
        self.color = color
        self.targetOnly = False
        self.CBVar = tk.IntVar()
        self.CBVar.set(0)
        #for events
        self.disabled = False
        #ui
        self.uiHeatBuildup = 0
        #ai info
        if(owner=="ai1"):
            self.prefMinRange = 100
            self.prefAverageRange = 200
            self.prefMaxRange = 300
            self.stance = stance

    def setTarget(self,variable):
        self.target = variable.get()
    def setTargetStr(self,variable):
        self.target = variable
    def setTargetOnly(self):
        if(self.targetOnly):
            self.targetOnly = False
        else:
            self.targetOnly = True

    def declareSystemSlots(self,systemSlots,systemStatus):
        for tmp in systemSlots:
            if(not tmp == 'none'):
                targetClass =  naglowek.systemLookup[tmp]
                tmpSystem = targetClass()
                self.systemSlots.append(tmpSystem)
        i = 0
        for tmp in systemStatus:
            if(i < len(self.systemSlots)):
                self.systemSlots[i].cooldown = int(tmp)
                i+=1

    def declareShieldState(self,shields,maxShields,var):
        self.shields = shields
        self.maxShields = maxShields
        self.shieldsState = []
        tmp = 0
        while(tmp < maxShields):
            self.shieldsState.append(var.shieldMaxState)
            tmp += 1

    def respawn(self,var,respawns,uiMetrics):
        for system in self.systemSlots:
            system.integrity = system.maxIntegrity
            system.heat = 0
        self.hp = self.maxHp
        self.ap = self.maxAp
        i = 0
        for shieldState in self.shieldsState:
            shieldState = var.shieldMaxState
            i+=1
            self.shields += 1
        for tmp in self.systemSlots:
            tmp.cooldown = 0
            # find pos
        tmpPosX = 100
        tmpPosY = 100
        bestPosX = 100
        bestPosY = 100
        checksLeft = 100
        while(checksLeft):
            tmpPosX = random.randrange(uiMetrics.canvasWidth)
            tmpPosY = random.randrange(uiMetrics.canvasHeight)
            maxDist2 = 0
            for ship2 in var.ships:
                dist2 = abs(tmpPosX - ship2.xPos) * abs(tmpPosX - ship2.xPos) + abs(tmpPosY - ship2.yPos) * abs(tmpPosY - ship2.yPos)
                if(maxDist2 < dist2):
                    bestPosX = tmpPosX
                    bestPosY = tmpPosY
            checksLeft -= 1
        self.xPos = bestPosX
        self.yPos = bestPosY
        respawns -= 1