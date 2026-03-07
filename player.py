
class Player():
    def __init__(self, posx, posy, atk, hp, defs, move, col, rad, cool, sped):
        self.position = (posx, posy)
        self.attack_power = atk 
        self.health = hp 
        self.defense = defs
        self.speed = move 
        self.color = col 
        self.radius = rad
        self.cooldown = cool
        self.projectile_speed = sped

    def getPos(self):
        return self.position
    
    def getX(self):
        return self.position[0]

    def getY(self):
        return self.position[1]
    
    def getAtk(self):
        return self.attack_power
    
    def getHP(self):
        return self.health

    def getDef(self):
        return self.defense
    
    def getSpeed(self):
        return self.speed
    
    def setPos(self, posx, posy):
        self.position = (posx, posy)
    
    def setX(self, posx):
        self.position = (posx, self.getY())

    def setY(self, posy):
        self.position = (self.getX(), posy)

    def setAtk(self, atk):
        self.attack_power = atk 
    
    def setHP(self, hp):
        self.health = hp
    
    def setDef(self, defs):
        self.defense = defs 

    def setSpeed(self, speed):
        self.speed = speed 

    def move(self, px, py):
        while True:
            sx = self.position[0]
            sy = self.position[1]
            sped = self.speed
            if py > sy:
                sy = sped
            elif py < sy: 
                sy = -sped
            else:
                sy = 0
            if px > sx:
                sx = sped
            elif px < sx:
                sx = -sped
            else:
                sx = 0
            self.position = (self.position[0] + sx , self.position[1] + sy)
            break 

    def attack(self):
        pass 

    def draw(self):
        pass

    def takeDamage(self):
        pass 

    def detectDamage(self):
        pass 