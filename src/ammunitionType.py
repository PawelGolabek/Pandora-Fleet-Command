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
    type1adefault = ammunition()
    type1adefault.name = 'type1a'
    type1adefault.typeName = 'type1a'
    type1adefault.damage = 90
    type1adefault.turnRate = 6
    type1adefault.speed = 110
    type1adefault.heat = 7.5
    type1adefault.color = rgbtohex(250,250,20)

    type2adefault = ammunition()
    type2adefault.name = 'type2a'
    type2adefault.typeName = 'type2a'
    type2adefault.damage = 160
    type2adefault.turnRate = 6
    type2adefault.speed = 100
    type2adefault.heat = 10

    type3adefault = ammunition()
    type3adefault.name = 'type3a'
    type3adefault.typeName = 'type3a'
    type3adefault.damage = 1000
    type3adefault.turnRate = 6
    type3adefault.speed = 70
    type3adefault.heat = 50

    laser1adefault = ammunition()
    laser1adefault.name = 'laser1a'
    laser1adefault.typeName = 'laser1a'
    laser1adefault.sort = 'laser'
    laser1adefault.damage = 4
    laser1adefault.turnRate = 25
    laser1adefault.speed = 1000
    laser1adefault.ttl = 600
    laser1adefault.color = rgbtohex(120,120,250)
    laser1adefault.heat = 3.5

    highEnergyLaser1 = ammunition()
    highEnergyLaser1.name = 'highEnergyLaser1'
    highEnergyLaser1.typeName = 'highEnergyLaser1'
    highEnergyLaser1.sort = 'laser'
    highEnergyLaser1.damage = 80
    highEnergyLaser1.speed = 1000
    highEnergyLaser1.ttl = 800
    highEnergyLaser1.color = rgbtohex(200,20,125)
    highEnergyLaser1.heat = 40

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
    type1adefault.color = rgbtohex(250,250,20)
