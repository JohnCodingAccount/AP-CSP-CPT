import pygame
import sys 
import random 
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
        if dist == 0: 
            return
        vx = dx / dist * self.speed
        vy = dy / dist * self.speed 
        self.position = (self.position[0] + vx, self.position[1] + vy)
    
    def knockback(self, px, py):
        self.isKnocked = True
        dx = px - self.position[0]
        dy = py - self.position[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        vx = dx / dist * self.kbSpeed
        vy = dy / dist * self.kbSpeed 
        self.position = (self.position[0] - vx, self.position[1] - vy)
        
    def isAtPlayer(self, mp, pp, mr, pr):
        mv = pygame.math.Vector2(mp)
        pv = pygame.math.Vector2(pp)
        d = mv.distance_to(pv)
        return d < (mr + pr)

class Spider(Monster):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, 2, 1, (25, 25, 25), 7, 4) 

class Zombie(Monster):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, 0.5, 2, (100, 100, 100), 12, 6) 

class Boss(Monster):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, 0.5, 5, (0, 0, 0), 50, 31) 

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
            if hd == 0 or dist < hd:
                hd = dist
                hmonx = mons[mon].position[0]
                hmony = mons[mon].position[1]
        return hmonx, hmony

class Tower(Building):
    def __init__(self, pos, health, type):
        super().__init__(pos, health, type)

class Tent(Building):
    def __init__(self, pos, health, type):
        super().__init__(pos, health, type)
    
    def Heal(self):
        pass

grey = (51, 51, 51)
white = (250, 250, 250)

MAX_PROJECTILES = 1000
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720 
FPS = 60
TITLE = "Create Performance Task"
WAVE = 0

class Game:
    def __init__(self):
        self.offsetx = -20 
        self.offsety = -20
        pygame.init()
        self.building = False
        self.MONSTERS = {}
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.hp = 100
        self.cost = 10
        self.ts = self.font.render("Health: " + str(self.hp), True, (0,0,0))
        self.tr = self.ts.get_rect()
        self.tr.center = (100, 50)
        self.gold = 1
        self.tg = self.font.render("Points: " + str(self.gold), True, (0,0,0))
        self.tgr = self.tg.get_rect()
        self.tgr.center = (100, 100)
        self.wave = WAVE
        self.selection = 1 
        self.tts = self.font.render("Wave: " + str(self.wave), True, (0,0,0))
        self.tir = self.tts.get_rect()
        self.tir.center = (1180, 50)
        self.stime = pygame.time.get_ticks()
        self.cooldown = False
        self.PROJECTILES = []
        self.BUILDINGS = []
        self.tent = pygame.image.load("Tent.png")
        self.tower = pygame.image.load("Tower.png")
        self.towertemplate = pygame.image.load("Tower.png")
        self.tenttemplate = pygame.image.load("Tent.png")
        self.tenttemplate.set_alpha(100)
        self.towertemplate.set_alpha(100)
        pygame.mouse.set_cursor(pygame.cursors.diamond)
        pygame.display.set_caption(TITLE)
        self.player = Player(self.screen.get_width() / 2, self.screen.get_height() / 2, 1, 10, 1, 10, "red", 10, 1, 8) 

        self.enemy_table = [
            (Spider, 30),   
            (Zombie, 70),   
            (Boss, 0)      
        ]

    def choose_enemy(self):
        total = sum(weight for enemy, weight in self.enemy_table)
        r = random.uniform(0, total)
        upto = 0
        for enemy, weight in self.enemy_table:
            if upto + weight >= r:
                return enemy
            upto += weight

    def random_spawn_edge(self):
        side = random.randint(1, 4)
        if side == 1:  
            return random.randint(0, SCREEN_WIDTH), 0
        if side == 2:  
            return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
        if side == 3:  
            return 0, random.randint(0, SCREEN_HEIGHT)
        if side == 4:  
            return SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)

    def waveUp(self):
        if len(self.MONSTERS) <= 0:
            
            if self.wave > 5:
                self.enemy_table = [(Spider, 35), (Zombie, 60), (Boss, 5)]
            if self.wave > 10:
                self.enemy_table = [(Spider, 40), (Zombie, 55), (Boss, 5)]
            if self.wave > 15:
                self.enemy_table = [(Spider, 0), (Zombie, 95), (Boss, 5)]
            if self.wave > 20:
                self.enemy_table = [(Spider, 70), (Zombie, 20), (Boss, 10)]
            if self.wave > 25:
                self.enemy_table = [(Spider, 15), (Zombie, 65), (Boss, 20)]
            if self.wave > 30:
                self.enemy_table = [(Spider, 35), (Zombie, 50), (Boss, 15)]
            if self.wave > 35:
                self.enemy_table = [(Spider, 50), (Zombie, 50), (Boss, 0)]
            if self.wave > 40:
                self.enemy_table = [(Spider, 45), (Zombie, 50), (Boss, 5)]
            if self.wave > 45:
                self.enemy_table = [(Spider, 0), (Zombie, 60), (Boss, 40)]
            if self.wave > 50:
                self.enemy_table = [(Spider, 30), (Zombie, 60), (Boss, 10)]

            self.gold += self.wave
            self.wave += 1
            self.updateVisible()

            for i in range(self.wave):
                EnemyClass = self.choose_enemy()
                x, y = self.random_spawn_edge()
                self.MONSTERS[i] = EnemyClass(x, y)

    def updateVisible(self):
        self.ts = self.font.render("Health: " + str(self.hp), True, (0,0,0))
        self.tg = self.font.render("Points: " + str(self.gold), True, (0,0,0))
        self.tts = self.font.render("Wave: " + str(self.wave), True, (0,0,0))

    def render(self):
        for build in self.BUILDINGS:
            if build.type == "Tower":
                self.screen.blit(self.tower, build.position)
            elif build.type == "Tent":
                self.screen.blit(self.tent, build.position)
        for projectile in self.PROJECTILES:
            projectile.draw(self.screen)
        for key in self.MONSTERS:
            monster = self.MONSTERS[key]
            pygame.draw.circle(self.screen, monster.color, pygame.Vector2(monster.position[0], monster.position[1]), monster.radius)

    def update(self):
        Knockback_time = 0.15
        Stun_time = 0.3
        ctime = pygame.time.get_ticks()

        if abs(self.stime - ctime)/1000 > self.player.cooldown: 
            self.stime = ctime 
            self.cooldown = False

        if self.building == True:
            if self.selection == 1:
                self.screen.blit(self.towertemplate, (pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety))
            elif self.selection == 2:
                self.screen.blit(self.tenttemplate, (pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety))

        mouser = pygame.mouse.get_pressed()
        if mouser[0]:
            if self.building:
                if self.selection == 1 and self.gold >= self.cost:
                    self.gold -= self.cost 
                    build = Tower((pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety), 5, "Tower")
                    self.BUILDINGS.append(build)
                    self.updateVisible()
                elif self.selection == 2 and self.gold >= self.cost:
                    self.gold -= self.cost
                    build = Tent((pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety), 5, "Tent")
                    self.BUILDINGS.append(build)
                    self.updateVisible()
            else:
                if not self.cooldown:
                    mx, my = pygame.mouse.get_pos()
                    self.PROJECTILES.append(Projectile(self.player.position[0], self.player.position[1], mx, my, self.player.projectile_speed))
                    self.cooldown = True

        for build in self.BUILDINGS[:]:
            if build.type == "Tower":
                if not build.cooldown:
                    build.st = pygame.time.get_ticks()
                    tx, ty = build.getClosest(self.MONSTERS)
                    self.PROJECTILES.append(Projectile(build.position[0], build.position[1], tx, ty, self.player.projectile_speed))
                    build.cooldown = True 
                if abs(build.st - pygame.time.get_ticks())/1000 > 3:
                    build.cooldown = False 
                for monster in self.MONSTERS.values():
                    d = pygame.math.Vector2(monster.position).distance_to(build.position)
                    if d < monster.radius + 20:
                        build.health -= 1
                if build.health <= 0:
                    self.BUILDINGS.remove(build)
            elif build.type == "Tent":
                if not build.cooldown:
                    build.st = pygame.time.get_ticks()
                    self.hp += 1 
                    self.updateVisible()
                    build.cooldown = True 
                if abs(build.st - pygame.time.get_ticks())/1000 > 3:
                    build.cooldown = False 
                for monster in self.MONSTERS.values():
                    d = pygame.math.Vector2(monster.position).distance_to(build.position)
                    if d < monster.radius + 20:
                        build.health -= 1
                if build.health <= 0:
                    self.BUILDINGS.remove(build)

        for projectile in self.PROJECTILES: 
            projectile.update()
        self.PROJECTILES = [p for p in self.PROJECTILES if p.alive]
        if len(self.PROJECTILES) > MAX_PROJECTILES:
            self.PROJECTILES.pop(0)

        Knockback_time = 0.15
        Stun_time = 0.3
        dels = []
        for key, monster in list(self.MONSTERS.items()):
            if monster.kt is not None:
                if abs(monster.kt - pygame.time.get_ticks())/1000 > Knockback_time:
                    monster.isKnocked = False
                if abs(monster.kt - pygame.time.get_ticks())/1000 > Stun_time:
                    monster.isKnocked2 = False

            if monster.isKnocked:
                monster.knockback(self.player.getX(), self.player.getY())
            elif not monster.isKnocked2:
                monster.move(self.player.getX(), self.player.getY())

            if monster.health <= 0:
                dels.append(key)

            if monster.isAtPlayer(monster.position, self.player.position, monster.radius, self.player.radius):
                self.player.color = "green"
                self.hp -= monster.atk
                self.updateVisible()
            else:
                self.player.color = "red"

            for projectile in self.PROJECTILES[:]:
                d = pygame.math.Vector2(monster.position).distance_to((projectile.x, projectile.y))
                if d < monster.radius + projectile.radius:
                    self.PROJECTILES.remove(projectile)
                    monster.isKnocked = True
                    monster.isKnocked2 = True
                    monster.kt = pygame.time.get_ticks()
                    monster.health -= (projectile.damage / 2)
                    self.waveUp()

        for i in dels:
            self.MONSTERS.pop(i, None)

    def run(self): 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.building = not self.building
                    elif event.key == pygame.K_1:
                        self.selection = 1
                    elif event.key == pygame.K_2:
                        self.selection = 2

            if self.hp <= 0:
                while True:
                    self.screen.fill((0,0,0))
                    font2 = pygame.font.Font("freesansbold.ttf", 89)
                    ts2 = font2.render("Game Over", True, (250, 250, 250))
                    tr = ts2.get_rect()
                    tr.center = (self.screen.get_width()//2, self.screen.get_height()//2)
                    self.screen.blit(ts2, tr)
                    pygame.display.update()
            else:
                self.screen.fill(white)
                self.screen.blit(self.ts, self.tr)
                self.screen.blit(self.tts, self.tir)
                self.screen.blit(self.tg, self.tgr)
                pygame.draw.circle(self.screen, self.player.color, pygame.Vector2(self.player.getX(), self.player.getY()), self.player.radius)
                self.waveUp()
                self.update()
                self.updateVisible()
                self.render()
                pygame.display.update()
                self.clock.tick(FPS)

game = Game()
game.run()
