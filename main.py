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

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720 
FPS = 60
TITLE = "Create Performance Task"
WAVE = 0
MONSTERS = {}

MAX_PROJECTILES = 1000

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
        super().__init__(posx, posy, 1.5, 5, (0, 0, 0), 50, 51) 
    def move(self, px, py):
        super().move(px, py)
    
    def knockback(self, px, py):
        return super().knockback(px, py)
    
    def isAtPlayer(self, mp, pp, mr, pr):
        return super().isAtPlayer(mp, pp, mr, pr)

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


grey = (51, 51, 51)
white = (250, 250, 250)



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
        self.waveUp()
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

    
    def get_point_on_circle(self, h, k, radius):
        theta = random.random() * 2 * math.pi
    
        x = h + math.cos(theta) * radius
        y = k + math.sin(theta) * radius
    
        return x, y
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
        else:
            pass

        if self.building == True:
            if self.selection == 1:
                self.screen.blit(self.towertemplate, (pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety))
            elif self.selection == 2:
                self.screen.blit(self.tenttemplate, (pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety))
        else: 
            pass 

        mouser = pygame.mouse.get_pressed()
        if mouser[0]:
            if self.building == True:
                if self.selection == 1:
                    if self.gold >= self.cost:
                        self.gold -= self.cost 
                        build = Tower((pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety), 5, "Tower")
                        self.BUILDINGS.append(build)
                        self.updateVisible()
                elif self.selection == 2:
                    if self.gold >= self.cost:
                        self.gold -= self.cost
                        build = Tent((pygame.mouse.get_pos()[0] + self.offsetx, pygame.mouse.get_pos()[1] + self.offsety), 5, "Tent")
                        self.BUILDINGS.append(build)
                        self.tg = self.font.render(str(self.gold), True, (0,0,0))
                else: 
                    pass
            else:
                if self.cooldown == False:
                    mx, my = pygame.mouse.get_pos()
                    self.PROJECTILES.append(Projectile(self.player.position[0], self.player.position[1], mx, my, self.player.projectile_speed))
                    self.cooldown = True 
                else:
                    pass
        
        
        if self.building == False:
            for build in self.BUILDINGS:
                if build.type == "Tower":
                    #self.screen.blit(self.tower, build.position)
                    if build.cooldown == False:
                        build.st = pygame.time.get_ticks()
                        tx, ty = build.getClosest(self.MONSTERS)
                        self.PROJECTILES.append(Projectile(build.position[0],build.position[1], tx, ty, self.player.projectile_speed))
                        build.cooldown = True 
                    if abs(build.st - pygame.time.get_ticks())/1000 > 3:
                        build.cooldown = False 
                    for monster in self.MONSTERS:
                        mp = self.MONSTERS[monster].position
                        mv = pygame.math.Vector2(mp)
                        bv = pygame.math.Vector2(build.position)
                        d = mv.distance_to(bv)
                        if d < (self.MONSTERS[monster].radius+20):
                            build.health -= 1
                    if build.health <= 0:
                        build.alive = False
                    if build.alive == False:
                        self.BUILDINGS.remove(build)
                elif build.type == "Tent":
                    #self.screen.blit(self.tent, build.position)
                    if build.cooldown == False:
                        build.st = pygame.time.get_ticks()
                        self.hp += 1 
                        self.updateVisible()
                        build.cooldown = True 
                    if abs(build.st - pygame.time.get_ticks())/1000 > 3:
                        build.cooldown = False 
                    for monster in self.MONSTERS:
                        mp = self.MONSTERS[monster].position
                        mv = pygame.math.Vector2(mp)
                        bv = pygame.math.Vector2(build.position)
                        d = mv.distance_to(bv)
                        if d < (self.MONSTERS[monster].radius+20):
                            build.health -= 1
                    if build.health <= 0:
                        build.alive = False
                    if build.alive == False:
                        self.BUILDINGS.remove(build)



        
        
        
            for projectile in self.PROJECTILES: 
                projectile.update()
                #projectile.draw(self.screen)
        
            self.PROJECTILES = [p for p in self.PROJECTILES if p.alive]

            if len(self.PROJECTILES) > MAX_PROJECTILES:
                self.PROJECTILES.pop(0)

            dels = [] 
            for key in self.MONSTERS:
                monster = self.MONSTERS[key]
                if monster.kt != None:
                    if abs(monster.kt - pygame.time.get_ticks())/1000 > Knockback_time:
                        monster.isKnocked = False
                    else:
                        pass
                    if abs(monster.kt - pygame.time.get_ticks())/1000 > Stun_time:
                        monster.isKnocked2 = False
                    else:
                        pass
                else:
                    pass
                if monster.isKnocked:
                    monster.knockback(self.player.getX(), self.player.getY())
                else:
                    if monster.isKnocked2:
                        pass
                    else:
                        monster.move(self.player.getX(), self.player.getY())
                #pygame.draw.circle(self.screen, monster.color, pygame.Vector2(monster.position[0], monster.position[1]), monster.radius)
                if monster.health <= 0:
                    dels.append(key)
                    break
                if monster.isAtPlayer(monster.position, self.player.position, monster.radius, self.player.radius) == True:
                    self.player.color = "green"
                    self.hp -= monster.atk
                    self.ts = self.font.render(str(self.hp), True, (0,0,0))
                
                else:
                    self.player.color = "red"
                projs = self.PROJECTILES
                for projectile in projs:
                    pr = projectile.radius
                    mr = monster.radius
                    pp = (projectile.x, projectile.y)
                    mp = monster.position
                    mv = pygame.math.Vector2(mp)
                    pv = pygame.math.Vector2(pp)
                    d = mv.distance_to(pv)
                    if d < (mr + pr):
                        self.PROJECTILES.remove(projectile)
                        monster.isKnocked = True 
                        monster.isKnocked2 = True
                        monster.kt = pygame.time.get_ticks() 
                        monster.health -= (projectile.damage / 2)
                        game.waveUp()
                    else:
                        continue
            
            for i in dels:
                try:
                    self.MONSTERS.pop(i)
                except KeyError:
                    pass
    
    def waveUp(self):
        
        mons = len(self.MONSTERS)
        if mons <= 0:
            self.gold += self.wave 
            self.wave = self.wave + 1
            self.updateVisible()
            for i in range(self.wave):
                rt = random.randint(1,2)
                rx = random.randint(0, self.screen.get_width())
                ry = random.randint(0,self.screen.get_height())
                ra = random.randint(1,4)
                if ra == 1:
                    if rt == 1:
                        monst = Spider(rx, 20) 
                    elif rt ==2:
                        rant = random.randint(1,5)
                        if rant == 1 or rant == 2 or rant == 3 or rant == 4: 
                            monst = Zombie(rx, 20)
                        else:
                            monst = Boss(rx, 20)
                if ra == 2: 
                    if rt == 1:
                        monst = Spider(rx, 700) 
                    elif rt ==2:
                        monst = Zombie(rx, 700)   
                if ra == 3: 
                    if rt == 1:
                        monst = Spider(20, ry) 
                    elif rt ==2:
                        monst = Zombie(20, ry)   
                if ra == 4:
                    if rt == 1:
                        monst = Spider(1260, ry) 
                    elif rt ==2:
                        monst = Zombie(1260, ry)   
                self.MONSTERS[i] = monst

    def run(self): 
        running = True
        while running:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if self.building == False:
                            self.building = True
                        else:
                            self.building = False
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
                    tr.center = (self.screen.get_width(), self.screen.get_height())
                    self.screen.blit(ts2, tr)
                
            else:
                self.screen.fill(white)
                self.screen.blit(self.ts, self.tr)
                self.screen.blit(self.tts, self.tir)
                self.screen.blit(self.tg, self.tgr)
                pygame.draw.circle(self.screen, self.player.color, pygame.Vector2(self.player.getX(), self.player.getY()), self.player.radius)
                game.waveUp()
                game.update()
                self.updateVisible()
                self.render()
                pygame.display.update()
                pygame.display.flip()
                self.clock.tick(FPS)

game = Game()
game.run()




