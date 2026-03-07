import pygame
import sys 
import random 
from monster import *
from settings import *
from player import *
from projectiles import *


grey = (51, 51, 51)
white = (250, 250, 250)


class Game:
    def __init__(self):
        pygame.init()
        self.MONSTERS = {}
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.hp = 100
        self.ts = self.font.render(str(self.hp), True, (0,0,0))
        self.tr = self.ts.get_rect()
        self.tr.center = (50, 50)
        self.wave = WAVE
        self.waveUp()
        self.tts = self.font.render(str(self.wave), True, (0,0,0))
        self.tir = self.tts.get_rect()
        self.tir.center = (1230, 50)
        self.stime = pygame.time.get_ticks()
        self.cooldown = False
        self.PROJECTILES = []
        pygame.mouse.set_cursor(pygame.cursors.diamond)
        pygame.display.set_caption(TITLE)
        self.player = Player(self.screen.get_width() / 2, self.screen.get_height() / 2, 1, 10, 1, 10, "red", 10, 1, 8) 
    

    def update(self):
        Knockback_time = 0.15
        Stun_time = 0.3
        ctime = pygame.time.get_ticks()

        if abs(self.stime - ctime)/1000 > self.player.cooldown: 
            self.stime = ctime 
            self.cooldown = False
        else:
            pass
            

        mouser = pygame.mouse.get_pressed()
        if mouser[0]:
            if self.cooldown == False:
                mx, my = pygame.mouse.get_pos()
                self.PROJECTILES.append(Projectile(self.player.position[0], self.player.position[1], mx, my, self.player.projectile_speed))
                self.cooldown = True 
            else:
                pass
        
        
        
        for projectile in self.PROJECTILES: 
            projectile.update()
            projectile.draw(self.screen)
        
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
            pygame.draw.circle(self.screen, monster.color, pygame.Vector2(monster.position[0], monster.position[1]), monster.radius)
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
            self.wave = self.wave + 1
            self.tts = self.font.render(str(self.wave), True, (0,0,0))
            for i in range(self.wave):
                rt = random.randint(1,2)
                rx = random.randint(0, self.screen.get_width())
                ry = random.randint(0,self.screen.get_height())
                ra = random.randint(1,4)
                if ra == 1:
                    if rt == 1:
                        monst = Spider(rx, 20) 
                    elif rt ==2:
                        rant = random.randint(1,2)
                        if rant == 1: 
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
            if self.hp <= 0:
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
                pygame.draw.circle(self.screen, self.player.color, pygame.Vector2(self.player.getX(), self.player.getY()), self.player.radius)
                game.waveUp()
                game.update()
                pygame.display.update()
                pygame.display.flip()
                self.clock.tick(FPS)

game = Game()
game.run()



