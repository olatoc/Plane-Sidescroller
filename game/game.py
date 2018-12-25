import pygame
import random
import math
pygame.init()

window = pygame.display.set_mode((768,512))
pygame.font.init()
myfont = pygame.font.SysFont('Consolas', 12)
clock = pygame.time.Clock()

player_img = pygame.image.load("jet-vector-small.png")
rotate = [pygame.transform.rotate(player_img, 45), pygame.transform.rotate(player_img, 40), pygame.transform.rotate(player_img, 35),
             pygame.transform.rotate(player_img, 30), pygame.transform.rotate(player_img, 25), pygame.transform.rotate(player_img, 20),
             pygame.transform.rotate(player_img, 15), pygame.transform.rotate(player_img, 10), pygame.transform.rotate(player_img, 5),
             pygame.transform.rotate(player_img, 0), pygame.transform.rotate(player_img, -5), pygame.transform.rotate(player_img, -10),
             pygame.transform.rotate(player_img, -15), pygame.transform.rotate(player_img, -20), pygame.transform.rotate(player_img, -25),
             pygame.transform.rotate(player_img, -30), pygame.transform.rotate(player_img, -35), pygame.transform.rotate(player_img, -40),
             pygame.transform.rotate(player_img, -45)]
enemy_img = pygame.image.load("enemy.png")
explosion = [pygame.image.load("e1.png"), pygame.image.load("e2.png"), pygame.image.load("e3.png"), pygame.image.load("e4.png"), pygame.image.load("e5.png")]

enemyCount = myfont.render('Enemy count: ', False, (0, 0, 0))
projCount = myfont.render('Projectile count: ', False, (0, 20, 0))


bg = pygame.image.load('background.png').convert()
bgX = 0
bgRelX = 0

enemyTimer = 100
collision = (False, None)


class Player():
    def __init__(self, y, wid, hgt):
        self.x = 256
        self.y = y
        self.wid = wid
        self.hgt = hgt
        self.velX = 5
        self.velY = 5

        self.animateCycle = 9

        self.isJumping = False
        self.jumpTime = 10
        self.neg = 1

        self.isShooting = 0

        self.explosionCycle = 0
        self.dead = 0

    def death(self):
        global collision
        if collision[0]:
            while self.explosionCycle < 10:
                clock.tick(30)
                window.blit(explosion[self.explosionCycle//2], (238, self.y - 32))
                window.blit(explosion[self.explosionCycle//2], (collision[1].x, collision[1].y - 32))
                self.explosionCycle += 1
                pygame.display.update()
        else:
            while self.explosionCycle < 10:
                clock.tick(30)
                window.blit(explosion[self.explosionCycle//2], (238, self.y - 32))
                self.explosionCycle += 1
                pygame.display.update()
        gameover()

    def draw(self, window):
        window.blit(rotate[self.animateCycle], (256, self.y))
        self.velY = self.animateCycle - 9
        if (self.y + self.velY) > 0 and not self.dead:
            self.y += self.velY
        if (self.y + self.hgt + self.velY) >= 500:
            self.death()

    def controls(self, keys):
        if keys[pygame.K_LEFT] and self.animateCycle >= 1:
            self.animateCycle -= 1
        elif keys[pygame.K_RIGHT] and self.animateCycle <= 17:
            self.animateCycle += 1
        if keys[pygame.K_SPACE]:
            if not self.isShooting:
                self.playerShoot()
        else:
            self.isShooting = False
        if p.isJumping:
            if p.jumpTime >= -10:
                p.neg = 1
                if p.jumpTime < 0:
                    p.neg = -1
                p.y -= p.jumpTime**2 * p.neg * 0.5
                p.jumpTime -= 1
            else:
                p.isJumping = False
                p.jumpTime = 10
                p.neg = 1
    def playerShoot(self):
        self.isShooting = True
        projectiles.append(Projectile())
        
p = Player(250, player_img.get_rect().width, player_img.get_rect().height)

class Projectile():
    def __init__(self):
        self.x = 256
        self.y = p.y
        self.vector = (20, (p.animateCycle - 9)*2)
    def draw(self, window):
        pygame.draw.circle(window, (0,0,0), (self.x + 64, self.y + 16 + p.animateCycle - 9), 5)
        self.x += self.vector[0]
        self.y += self.vector[1]
        if self.x > 780:
            projectiles.remove(self)
class EnemyProjectile():
    def __init__(self, enemy):
        self.x = round(enemy.x)
        self.y = round(enemy.y + 11)
    def draw(self, window):
        pygame.draw.circle(window, (255,0,0), (self.x, self.y), 5)
        self.x -= 10
        if self.x + 10 < 0:
            enemyProj.remove(self)

class Enemy():
    def __init__(self, x, wid, hgt, hp):
        self.x = x
        self.y = random.choice(range(10,502))
        self.wid = wid
        self.hgt = hgt
        self.hp = hp
        self.velY = 0
        self.velX = 3
        self.dist = 0
        self.explosionCycle = 0
        self.dying = False
        self.isShooting = False
        self.shootTimer = 
    def death(self):
        self.dying = True

    def draw(self, window):
        self.dist = self.y - p.y
        self.velY = self.dist/100
        self.x -= self.velX
        self.y -= self.velY
        window.blit(enemy_img, (self.x, self.y))
        if self.x + self.wid <= 0:
            enemies.remove(self)
        if self.dying:
            if self.explosionCycle < 10:
                window.blit(explosion[self.explosionCycle//2], (self.x, self.y - 32))
                self.explosionCycle += 1
            else:
                enemies.remove(self)
        if self.dist < 10:
            if not self.isShooting:
                self.enemyShoot()
        else:
            self.isShooting = False
    def enemyShoot(self):
        self.isShooting = True
        enemyProj.append(EnemyProjectile(self))
        

projectiles = []
enemyProj = []

enemies = []
def spawnEnemy():
    enemies.append(Enemy(768, enemy_img.get_rect().width, enemy_img.get_rect().height, 100))

def checkCollisions():
    global collision
    for proj in projectiles:
        projDot = [proj.x + 5, proj.y + 5]
        for enemy in enemies:
            if projDot[1] >= enemy.y and projDot[1] <= (enemy.y + enemy.hgt):
                if projDot[0] >= enemy.x and projDot[0] <= (enemy.x + enemy.wid):
                    enemy.death()
                    projectiles.remove(proj)
                    break

    for enemy in enemies:
        enemyDot = [enemy.x + 5, enemy.y + 11]
        if enemyDot[0] >= p.x and enemyDot[0] <= (p.x + p.wid):
            if enemyDot[1] >= p.y and enemyDot[1] <= (p.y + p.hgt):
                collision = (True, enemy)
                p.death()
def redraw():
    global bgX, bgRelX, enemyTimer
    bgRelX = bgX % bg.get_rect().width
    window.blit(bg,(bgRelX - bg.get_rect().width,0))
    if bgRelX < 768:
        window.blit(bg,(bgRelX,0))
    bgX -= p.velX

    p.draw(window)
    if enemyTimer <= 0:
        spawnEnemy()
        enemyTimer = 25
    for enemy in enemies:
        enemy.draw(window)
    for proj in projectiles:
        proj.draw(window)
    for proj in enemyProj:
        proj.draw(window)
    
    window.blit(enemyCount,(0,0))
    window.blit(projCount,(0,20))

    pygame.display.update()

def gameover():
    pygame.quit()

run = True
while run:
    clock.tick(30)
    enemyTimer -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    p.controls(keys)
    checkCollisions()
    redraw()
    enemyCount = myfont.render('Enemy count: ' + str(len(enemies)), False, (0, 0, 0))
    projCount = myfont.render('Projectile count: ' + str(len(projectiles)), False, (0, 0, 0))

pygame.quit()
