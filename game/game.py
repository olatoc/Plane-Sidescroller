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

numEnemies = myfont.render('Enemy count: ', False, (0, 0, 0))
projCount = myfont.render('Projectile count: ', False, (0, 20, 0))

bg = pygame.image.load('background.png').convert()
bgX = 0
bgRelX = 0

level = 0

enemyTimer = 100
collision = (False, None)

#level globals
ammoCount = 30
enemyCount = 0
enemySpeed = 0
enemyFireRate = 0
enemySpawnRate = 0
totalSpawned = 0

class Player():
    def __init__(self, y, wid, hgt):
        self.x = 256
        self.y = y
        self.wid = wid
        self.hgt = hgt
        self.velX = 5
        self.velY = 5

        self.animateCycle = 9

        self.ammo = ammoCount
        self.isShooting = 0
        self.killCount = 0

        self.explosionCycle = 0

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
        if (self.y + self.velY) > 0:
            self.y += self.velY
        if (self.y + self.hgt + self.velY) >= 500:
            self.death()

    def controls(self, keys):
        if keys[pygame.K_LEFT] and self.animateCycle >= 1:
            self.animateCycle -= 1
        elif keys[pygame.K_RIGHT] and self.animateCycle <= 17:
            self.animateCycle += 1
        if keys[pygame.K_SPACE]:
            if not self.isShooting and self.ammo > 0:
                self.playerShoot()
        else:
            self.isShooting = False

    def playerShoot(self):
        self.isShooting = True
        projectiles.append(Projectile())
        self.ammo -= 1

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
        self.x -= 20
        if self.x + 10 < 0:
            enemyProj.remove(self)

class Enemy():
    def __init__(self, x, wid, hgt, hp):
        global enemyFireRate
        self.x = x
        self.y = random.choice(range(10,502))
        self.wid = wid
        self.hgt = hgt
        self.hp = hp
        self.velY = 0
        self.velX = enemySpeed
        self.dist = 0
        self.explosionCycle = 0
        self.dying = False
        self.isShooting = False
        self.shootTimer = enemyFireRate
    def death(self):
        global enemyCount
        if not self.dying:
            p.killCount += 1
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
                window.blit(explosion[self.explosionCycle//2], (self.x - 16, self.y - 32))
                self.explosionCycle += 1
            else:
                enemies.remove(self)
        else:
            window.blit(enemy_img, (self.x, self.y))
        if self.shootTimer <= 0:
            if abs(self.dist) < 10:
                self.enemyShoot()
        else:
            self.isShooting = False
            self.shootTimer -= 1
    def enemyShoot(self):
        global enemyShootRate
        self.isShooting = True
        self.shootTimer = enemyFireRate
        enemyProj.append(EnemyProjectile(self))

projectiles = []
enemyProj = []

enemies = []
def spawnEnemy():
    global totalSpawned
    enemies.append(Enemy(768, enemy_img.get_rect().width, enemy_img.get_rect().height, 100))
    totalSpawned += 1

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
    for proj in enemyProj:
        projDot = [proj.x + 5, proj.y + 5]
        if projDot[1] >= (p.y + p.hgt*.25) and projDot[1] <= (p.y + p.hgt*.75):
            if projDot[0] >= p.x and projDot[0] <= (p.x + p.wid):
                p.death()
                enemyProj.remove(proj)
                break
    for enemy in enemies:
        enemyDot = [enemy.x + 5, enemy.y + 11]
        if enemyDot[0] >= p.x and enemyDot[0] <= (p.x + p.wid):
            if enemyDot[1] >= p.y and enemyDot[1] <= (p.y + p.hgt):
                collision = (True, enemy)
                p.death()
def redraw():
    global bgX, bgRelX, enemyTimer, enemyCount, totalSpawned, level
    bgRelX = bgX % bg.get_rect().width
    window.blit(bg,(bgRelX - bg.get_rect().width,0))
    if bgRelX < 768:
        window.blit(bg,(bgRelX,0))
    bgX -= p.velX

    p.draw(window)
    if enemyTimer <= 0:
        if p.killCount <= enemyCount and totalSpawned < enemyCount:
            spawnEnemy()
            enemyTimer = 100

    for enemy in enemies:
        enemy.draw(window)
    for proj in projectiles:
        proj.draw(window)
    for proj in enemyProj:
        proj.draw(window)

    numEnemies = myfont.render('Enemy count: ' + str(enemyCount - p.killCount), False, (0, 0, 0))
    projCount = myfont.render('Ammo: ' + str(p.ammo), False, (0, 0, 0))
    levelBanner = myfont.render('Level ' + str(level), False, (255, 255, 255))
    window.blit(numEnemies,(0,0))
    window.blit(projCount,(0,20))
    window.blit(levelBanner,(0,40))

    pygame.display.update()

def initialize():
    startup_banner = myfont.render('PRESS ENTER TO START', False, (255, 255, 255))
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            break
        window.blit(startup_banner, (300, 256))
        pygame.display.update()
    levelOne()

def levelOne():
    global level, enemyCount, enemySpeed, enemyFireRate, ammoCount, enemySpawnRate
    level = 1
    enemyCount = 5
    enemySpeed = 2
    enemyFireRate = 10
    enemySpawnRate = 1
    p.ammo = 30
    ammoCount = 30
def levelTwo():
    global level, enemyCount, enemySpeed, enemyFireRate, ammoCount, enemySpawnRate
    level = 2
    enemyCount = 10
    enemySpeed = 3
    enemyFireRate = 5
    enemySpawnRate = 2
    p.ammo = 30
    ammoCount = 30
def levelThree():
    global level, enemyCount, enemySpeed, enemyFireRate, ammoCount, enemySpawnRate
    level = 3
    enemyCount = 15
    enemySpeed = 4
    enemyFireRate = 1
    enemySpawnRate = 3
    p.ammo = 30
    ammoCount = 30

levels = {1: levelOne,
          2: levelTwo,
          3: levelThree}

def gameover():
    pygame.quit()

def main():
    global level, enemyCount, enemySpeed, enemyFireRate, ammoCount, enemySpawnRate, enemyTimer
    initialize()

    run = True
    while run:
        clock.tick(30)
        enemyTimer -= enemySpawnRate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        p.controls(keys)
        checkCollisions()
        #print(level)
        if enemyCount == p.killCount and level >= 1:
            levels[level + 1]()
        redraw()
main()
