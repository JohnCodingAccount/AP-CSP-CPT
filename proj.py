import pygame
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed=8, damage=10):
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        self.vx = dx / dist * speed
        self.vy = dy / dist * speed
        self.x = x
        self.y = y
        self.radius = 5
        self.damage = damage
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 80, 80), (int(self.x), int(self.y)), self.radius)

    def get_damage(self):
        return self.damage

player_pos = (width // 2, height // 2)
player_radius = 20

projectiles = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            projectiles.append(Projectile(player_pos[0], player_pos[1], mx, my))

    for p in projectiles:
        p.update()

    projectiles = [p for p in projectiles if p.alive]

    screen.fill((30, 30, 30))

    pygame.draw.circle(screen, (80, 200, 255), player_pos, player_radius)

    for p in projectiles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()