from src.colorCommands import rgbtohex

class ammunition():
    def __init__(self, name='', typeName='', sort = '', owner='', target='', xDir=0, yDir=0, turnRate=2, speed=100, \
         shotsPerTurn=5, damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, ttl = 10000, color = (rgbtohex(20,255,255)), special=None, heat = 0):
        self.owner = owner
        self.target = target
        self.name = name
        self.typeName = typeName
        self.sort = sort
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.shotsPerTurn = shotsPerTurn
        self.damage = damage
        self.damageFalloffStart = damageFalloffStart
        self.damageFalloffStop = damageFalloffStop
        self.defaultAccuracy = defaultAccuracy
        self.ttl = ttl
        self.color = color
        self.special = special
        self.heat = heat
        
class ammunition_type:
    bolter = ammunition()
    bolter.name = 'bolter'
    bolter.typeName = 'bolter'
    bolter.damage = 90
    bolter.turnRate = 6
    bolter.speed = 110
    bolter.heat = 7.5
    bolter.color = rgbtohex(250,250,20)

    missle = ammunition()
    missle.name = 'missle'
    missle.typeName = 'missle'
    missle.damage = 160
    missle.turnRate = 6
    missle.speed = 100
    missle.heat = 10

    nuke = ammunition()
    nuke.name = 'nuke'
    nuke.typeName = 'nuke'
    nuke.damage = 1000
    nuke.turnRate = 6
    nuke.speed = 70
    nuke.heat = 50

    laser1adefault = ammunition()
    laser1adefault.name = 'laser1a'
    laser1adefault.typeName = 'laser1a'
    laser1adefault.sort = 'laser'
    laser1adefault.damage = 1
    laser1adefault.turnRate = 25
    laser1adefault.speed = 1000
    laser1adefault.ttl = 600
    laser1adefault.color = rgbtohex(120,120,250)
    laser1adefault.heat = 6

    highEnergyLaser1 = ammunition()
    highEnergyLaser1.name = 'highEnergyLaser1'
    highEnergyLaser1.typeName = 'highEnergyLaser1'
    highEnergyLaser1.sort = 'laser'
    highEnergyLaser1.damage = 10
    highEnergyLaser1.speed = 1000
    highEnergyLaser1.ttl = 800
    highEnergyLaser1.color = rgbtohex(200,20,125)
    highEnergyLaser1.heat = 240

    kinetic1 = ammunition()
    kinetic1.name = 'kinetic1'
    kinetic1.typeName = 'kinetic1'
    kinetic1.sort = 'kinetic'
    kinetic1.damage = 2
    kinetic1.speed = 250
    kinetic1.turnRate = 6
    kinetic1.ttl = 800
    kinetic1.heat = 1.2
    kinetic1.color = rgbtohex(50,40,35)

    incirination1adefault = ammunition()
    incirination1adefault.name = 'incirination1a'
    incirination1adefault.typeName = 'incirination1a'
    incirination1adefault.sort = 'rocket'
    incirination1adefault.damage = 10
    incirination1adefault.speed = 150
    incirination1adefault.turnRate = 6
    incirination1adefault.ttl = 800
    incirination1adefault.heat = 400
    incirination1adefault.color = rgbtohex(250,250,20)
