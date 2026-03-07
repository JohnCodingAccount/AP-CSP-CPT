import pygame
import time
import math
import random
class Monster:
    def __init__(self, posx, posy, speed, atk, col, rad, health=10):
        self.position = (posx,posy)
        self.speed = speed 
        self.kbSpeed = speed * 2
        self.atk = atk 
        self.color = col
        self.health = health
        self.radius = rad
        self.alive = True
        self.isKnocked = False
        self.isKnocked2 = False 
        self.kt = None 
    def move(self, px, py):
        dx = px - self.position[0]
        dy = py - self.position[1]
        dist = math.hypot(dx, dy)
        vx = dx / dist * self.speed
        vy = dy / dist * self.speed 
        self.position = (self.position[0] + vx, self.position[1] + vy)
    
    def knockback(self, px, py):
        self.isKnocked = True
        dx = px - self.position[0]
        dy = py - self.position[1]
        dist = math.hypot(dx, dy)
        vx = dx / dist * self.kbSpeed
        vy = dy / dist * self.kbSpeed 
        self.position = (self.position[0] - vx, self.position[1] - vy)
        
    def isAtPlayer(self, mp, pp, mr, pr):
        mv = pygame.math.Vector2(mp)
        pv = pygame.math.Vector2(pp)
        d = mv.distance_to(pv)
        if d < (mr + pr):
            return True
        else:
            return False
        
class Spider(Monster):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, 2, 1, (25, 25, 25), 7, 4) 
    def move(self, px, py):
        super().move(px, py)
    
    def knockback(self, px, py):
        return super().knockback(px, py)
    
    def isAtPlayer(self, mp, pp, mr, pr):
        return super().isAtPlayer(mp, pp, mr, pr)


class Zombie(Monster):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, 0.5, 2, (100, 100, 100), 12, 6) 
    def move(self, px, py):
        super().move(px, py)
    
    def isAtPlayer(self, mp, pp, mr, pr):
        return super().isAtPlayer(mp, pp, mr, pr)
    
    def knockback(self, px, py):
        return super().knockback(px, py)
    


class Boss(Monster):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, 0.5, 5, (0, 0, 0), 25, 21) 
    def move(self, px, py):
        super().move(px, py)
    
    def knockback(self, px, py):
        return super().knockback(px, py)
    
    def isAtPlayer(self, mp, pp, mr, pr):
        return super().isAtPlayer(mp, pp, mr, pr)