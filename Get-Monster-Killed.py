import pygame
import os

pygame.init()

screenW = 700
screenH = 399
window = pygame.display.set_mode((screenW,screenH))
pygame.display.set_caption('Get-Monster-Killed')
clock = pygame.time.Clock()
score = 0

moveLeft = [pygame.image.load('Images/'+str(x)) for x in os.listdir('Images') if x.startswith('L')]
moveRight = [pygame.image.load('Images/'+str(x)) for x in os.listdir('Images') if x.startswith('R')]
bg = pygame.image.load('Images/bg1.jpg')
standing = pygame.image.load('Images/standing.png')

bulletSound = pygame.mixer.Sound('Sounds/bullet.wav')
hitSound = pygame.mixer.Sound('Sounds/hit.wav')

music = pygame.mixer.music.load('Sounds/music.wav')
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = 5
        self.jumped = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 8
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    
    def draw(self, window):
        if self.walkCount >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                window.blit(moveLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(moveRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(moveRight[0], (self.x, self.y))
            else:
                window.blit(moveLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(window, (255,225,225,128), self.hitbox,-1)
    def hit(self):
        self.jumped = False
        self.jumpCount = 8
        self.x = 100
        self.y = 300
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', False, (255,0,0))
        window.blit(text, (screenW//2 - (text.get_width()//2), screenH//2-50))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 100
                    pygame.quit()

class projectile():
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius)

class enemy():
    moveLeft = [pygame.image.load('Enemy/'+str(x)) for x in os.listdir('Enemy') if x.startswith('L')]
    moveRight = [pygame.image.load('Enemy/'+str(x) )for x in os.listdir('Enemy') if x.startswith('R')]
    def __init__(self, x, y, w, h, end):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.speed = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkCount >= 33:
                self.walkCount = 0
            if self.speed > 0:
                window.blit(self.moveRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                window.blit(self.moveLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1]-20,50,10))
            pygame.draw.rect(window, (0,255,0), (self.hitbox[0], self.hitbox[1]-20,50 - ((50//10)*(10-self.health)),10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        #pygame.draw.rect(window, (255,0,0), self.hitbox,-1)
    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * (-1)
                self.walkCount = 0
        else:
            if self.x + self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * (-1)
                self.walkCount = 0
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        

def background():
    window.blit(bg, (0,0))
    text = font.render('SCORE: '+str(score),1,(255,0,0))
    window.blit(text, (450,50))
    man.draw(window)
    goblin.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()

man = player(300, 300, 64, 64)
goblin = enemy(100,305, 64, 64, 500)
font = pygame.font.SysFont('Arial',45,bold=True)
bullets = []
shootLoop = 0
running = True
while running:
    clock.tick(18)

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and goblin.visible:
            score -= 5
            man.hit()
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and goblin.visible:
                score += 1
                hitSound.play()
                goblin.hit()
                bullets.pop(bullets.index(bullet))
        if bullet.x < screenW and bullet.x > 0:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x+man.w//2),round(man.y+man.h//2), 6, (0,0,0), facing))
        shootLoop = 1
    
    if keys[pygame.K_LEFT] and man.x >= man.speed:
        man.x -= man.speed
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x <= screenW - man.w - man.speed:
        man.x += man.speed
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if keys[pygame.K_UP]:
            man.jumped = True
    if man.jumped:
        if man.jumpCount >= -8:
            man.y -= int(man.jumpCount*abs(man.jumpCount)/2)
            man.jumpCount -= 1
        else:
            man.jumpCount = 8
            man.jumped = False
    background()

    