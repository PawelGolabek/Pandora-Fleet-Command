from colorCommands import rgbtohex

class ammunition():
    def __init__(self, name='', typeName='', sort = '', owner='', target='', xDir=0, yDir=0, turnRate=2, speed=100, \
         shotsPerTurn=5, damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, ttl = 10000, color = (rgbtohex(20,255,255)), special=None):
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
        
class ammunition_type:
    type1adefault = ammunition()
    type1adefault.name = 'type1a'
    type1adefault.typeName = 'type1a'
    type1adefault.shotsPerTurn = 8
    type1adefault.damage = 10
    type1adefault.turnRate = 6
    type1adefault.speed = 90
    type1adefault.color = rgbtohex(250,250,20)

    type2adefault = ammunition()
    type2adefault.name = 'type2a'
    type2adefault.typeName = 'type2a'
    type2adefault.damage = 20
    type2adefault.turnRate = 6
    type2adefault.speed = 120

    type3adefault = ammunition()
    type3adefault.name = 'type3a'
    type3adefault.typeName = 'type3a'
    type3adefault.damage = 300
    type3adefault.turnRate = 10
    type3adefault.speed = 70

    laser1adefault = ammunition()
    laser1adefault.name = 'laser1a'
    laser1adefault.typeName = 'laser1a'
    laser1adefault.sort = 'laser'
    laser1adefault.damage = 1
    laser1adefault.turnRate = 25
    laser1adefault.speed = 1000
    laser1adefault.ttl = 600
    laser1adefault.color = rgbtohex(250,250,20)

    highEnergyLaser1 = ammunition()
    highEnergyLaser1.name = 'highEnergyLaser1'
    highEnergyLaser1.typeName = 'highEnergyLaser1'
    highEnergyLaser1.sort = 'laser'
    highEnergyLaser1.damage = 40
    highEnergyLaser1.speed = 1000
    highEnergyLaser1.ttl = 800
    highEnergyLaser1.color = rgbtohex(200,20,125)

    kinetic1 = ammunition()
    kinetic1.name = 'kinetic1'
    kinetic1.typeName = 'kinetic1'
    kinetic1.sort = 'kinetic'
    kinetic1.damage = 1
    kinetic1.speed = 250
    kinetic1.turnRate = 90
    kinetic1.ttl = 800
    kinetic1.color = rgbtohex(50,40,35)


# ammunition_lookup = dict
# ammunition_lookup = {'type1a': type1a,
#                    'type2a': type2a,
#                   'type3a': type3a,
#                  }
