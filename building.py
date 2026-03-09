import pygame
import math

class Building:
    def __init__(self, pos, health, type):
        self.position = (pos[0], pos[1])
        self.alive = True 
        self.health = health
        self.cooldown = False
        self.st = 0 
        self.type = type

    
    def getClosest(self, mons):
        hd = 0
        hmonx = 0
        hmony = 0
        for mon in mons: 
            dx = mons[mon].position[0] - self.position[0]
            dy = mons[mon].position[1] - self.position[1]
            dist = math.hypot(dx, dy)
            if abs(dist) > hd:
                hd = dist
                hmonx = mons[mon].position[0]
                hmony = mons[mon].position[1]
        return hmonx, hmony
        
class Tower(Building):
    def __init__(self, pos, health, type):
        super().__init__(pos, health, type)
    
    def getClosest(self, mons):
        return super().getClosest(mons)

class Tent(Building):
    def __init__(self, pos, health, type):
        super().__init__(pos, health, type)
    
    def getClosest(self, mons):
        return super().getClosest(mons)
    
    def Heal(self):
        pass