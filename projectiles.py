import pygame 
import math

class Projectile():
    def __init__(self, x, y, target_x, target_y, speed=8, damage=10, size=5, color=(250,0,0)):
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        try:
            self.vx = dx / dist * speed
            self.vy = dy / dist * speed
        except ZeroDivisionError:
            self.vy = 8
            self.vx = 8
        self.x = x
        self.y = y
        self.radius = size 
        self.damage = damage
        self.alive = True
        self.color = color 

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > 1280 or self.y < 0 or self.y > 720:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 80, 80), (int(self.x), int(self.y)), self.radius)

    def get_damage(self):
        return self.damage