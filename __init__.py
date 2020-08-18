import module_manager
module_manager.review()

import pygame
import time
import os
import random
import math

pygame.init()

display_width = 1400
display_height = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Left 4 Dead')
clock = pygame.time.Clock()               

#################################################
# Global Functions
#################################################  
def text_objects(text, font):
    textSurface = font.render(text, True, (200,0,0))
    return textSurface, textSurface.get_rect()

def distance(xi,xii,yi,yii):
    sq1 = (xi-xii)*(xi-xii)
    sq2 = (yi-yii)*(yi-yii)
    return math.sqrt(sq1 + sq2)

#################################################
# Classes
#################################################  
class Zombie(pygame.sprite.Sprite):
    def __init__(self,x,y,scrollX,velX,width = 101,height = 145, attack = 0.1, health = 75, dead = False):
        pygame.sprite.Sprite.__init__(self)
        self.lilZomb = pygame.image.load("images"+os.sep+'zombiepalette2.png')
        self.deadZomb = pygame.image.load("images"+os.sep+'deadzomb.png')
        self.x = x
        self.y = y
        self.scrollX = scrollX
        self.velX = velX
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x - width*0.9 - scrollX, y + height*0.2, width, height*0.8)
        self.head = pygame.Rect(x - width*0.5 - scrollX, y,width, height*0.15)
        self.attack = attack
        self.health = health
        self.dead = dead
    def draw(self):
        if not self.dead:  
            if self.velX > 0:
                gameDisplay.blit(self.lilZomb,(self.x-100 - self.scrollX,self.y))
            else:
                gameDisplay.blit(pygame.transform.flip(self.lilZomb,True, False),(self.x - 100 - self.scrollX, self.y))
        else:   
            if self.velX > 0:
                gameDisplay.blit(self.deadZomb,(self.x-100 - self.scrollX, self.y + display_height/7.6))
            else:
                gameDisplay.blit(pygame.transform.flip(self.deadZomb,True, False),(self.x - 100 - self.scrollX, self.y + display_height/7.6)) 
    def move(self):
        self.x -= self.velX
        if not self.dead:
            self.rect = pygame.Rect(self.x - self.width*0.9 - self.scrollX, self.y + self.height*0.25,self.width,self.height*0.75)
            self.head = pygame.Rect(self.x - self.width*0.6 - self.scrollX, self.y, self.width - self.width*0.6, self.height*0.25)
        else:
            self.rect = pygame.Rect(0,0,0,0)
            self.head = pygame.Rect(0,0,0,0)
    def death(self):
        self.dead = True
    def removedraw(self):
        pygame.draw.rect(gameDisplay, (0,0,0),(self.x-100 - self.scrollX, self.y, self.width, self.height))

class FlippedZombie(Zombie):
    def __init__(self, x, y,scrollX, velX, width = 101,height = 145,attack = 0.1, health = 75, dead = False):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x,y,scrollX,velX,width,height,attack,health,dead)
        self.lilZomb = pygame.image.load("images"+os.sep+'zombiepalette2.png')
        self.deadZomb = pygame.image.load("images"+os.sep+'deadzomb.png')
        self.rect = pygame.Rect(x-width*0.9 - scrollX, y + height*0.25, width, height*0.75)
        self.head = pygame.Rect(x-width*0.55 - scrollX, y, width - width*0.6, height*0.25)   
    
class Sprinter(Zombie):
    def __init__(self, x, y, scrollX, velX, width = 140,height = 140, attack = 0.5, health = 50,dead = False, livePic = "images"+os.sep+'sprinter.jpg'):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x,y,scrollX,velX,width,height,attack,health,dead)
        self.sprintZomb = pygame.image.load(livePic)
        self.deadZomb = pygame.image.load("images"+os.sep+'deadSprint.png')
        self.rect = pygame.Rect(x + 10 - scrollX,y + width*0.5,width,height*0.5)
        self.head = pygame.Rect(x - scrollX,y,width,height*0.5)
    def draw(self):
        if not self.dead:
            if self.velX > 0:
                gameDisplay.blit(self.sprintZomb,(self.x - self.scrollX, self.y))
            else:
                gameDisplay.blit(pygame.transform.flip(self.sprintZomb,True,False),(self.x - self.scrollX,self.y))
        else:
            if self.velX > 0:
                gameDisplay.blit(self.deadZomb,(self.x - 30 - self.scrollX, self.y + display_height/7.9))
            else:
                gameDisplay.blit(pygame.transform.flip(self.deadZomb,True,False),(self.x-30 - self.scrollX,self.y + display_height/7.9))
    def move(self):
        self.x -= self.velX
        if not self.dead:
            self.rect = pygame.Rect(self.x + 10 - self.scrollX, self.y + self.width*0.5, self.width, self.height*0.4)
            self.head = pygame.Rect(self.x - self.scrollX, self.y, self.width, self.height*0.5)
        else:
            self.rect = (0,0,0,0)
            self.head = (0,0,0,0)
    def removedraw(self):
        pygame.draw.rect(gameDisplay, (0,0,0),(self.x - self.scrollX, self.y, self.width, self.height))

class FlippedSprinter(Sprinter):
    def __init__(self, x, y, scrollX, velX, width = 140,height = 140, attack = 0.5, health = 50,dead = False, livePic = "images"+os.sep+'sprinter.jpg'):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x,y,scrollX,velX,width,height,attack,health,dead,livePic)
        self.deadZomb = pygame.image.load("images"+os.sep+'deadSprint.png')
        self.rect = pygame.Rect(x - scrollX,y + height*0.5,width,height*0.5)
        self.head = pygame.Rect(x + 50 - scrollX,y,width,height*0.5)
    def move(self):
        self.x -= self.velX
        if not self.dead:
            self.rect = pygame.Rect(self.x - self.scrollX, self.y + self.height*0.5, self.width, self.height*0.5)
            self.head = pygame.Rect(self.x + 20 - self.scrollX, self.y, self.width - 50, self.height*0.5)
        else:
            self.rect = (0,0,0,0)
            self.head = (0,0,0,0)
    
class Giant(Zombie):
    def __init__(self, x, y, scrollX,velX, width = 149,height = 171, attack = 1, health = 100,dead = False):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x,y,scrollX,velX,width,height,attack,health,dead)
        self.giantZomb = pygame.image.load("images"+os.sep+'giant.jpg')
        self.deadZomb = pygame.image.load("images"+os.sep+'deadGiant.png')
        self.head = pygame.Rect(x + 30,y + height*0.7,width,height*0.3)
        self.rect = pygame.Rect(x + 30,y,width,height*0.7)
    def draw(self):
        if not self.dead:
            if self.velX > 0:
                gameDisplay.blit(self.giantZomb,(self.x - self.scrollX, self.y - 15))
            else:
                gameDisplay.blit(pygame.transform.flip(self.giantZomb,True,False),(self.x - self.scrollX, self.y - 15))        
        else:
            if self.velX > 0:
                gameDisplay.blit(self.deadZomb,(self.x - 30 - self.scrollX, self.y + display_height/8))
            else:
                gameDisplay.blit(pygame.transform.flip(self.deadZomb,True,False),(self.x-30 - self.scrollX,self.y + display_height/8))
    def move(self):
        self.x -= self.velX
        if not self.dead:
            self.head = pygame.Rect(self.x + 30 - self.scrollX, self.y, self.width, self.height*0.4)
            self.rect = pygame.Rect(self.x + 30 - self.scrollX, self.y + self.height*0.4, self.width, self.height*0.6)
    def removedraw(self):   
        pygame.draw.rect(gameDisplay, (0,0,0),(self.x - self.scrollX, self.y - 10,self.width,self.height))

class FlippedGiant(Giant):
    def __init__(self, x, y, scrollX,velX, width = 149,height = 171, attack = 1, health = 100,dead = False):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x,y,scrollX,velX,width,height,attack,health,dead)
        self.giantZomb = pygame.image.load("images"+os.sep+'giant.jpg')
        self.deadZomb = pygame.image.load("images"+os.sep+'deadGiant.png')
        self.head = pygame.Rect(x + 10,y + height*0.7,width,height*0.3)
        self.rect = pygame.Rect(x - 20,y,width,height*0.7)
    def move(self):
        self.x -= self.velX
        if not self.dead:
            self.head = pygame.Rect(self.x + 20 - self.scrollX, self.y, self.width - 65, self.height*0.4)
            self.rect = pygame.Rect(self.x + 20 - self.scrollX, self.y + self.height*0.4, self.width - 65, self.height*0.6)

class Bat(Zombie):
    def __init__(self,x,y,scrollX,velX,width=135,height=113,attack = 2,health = 20, dead = False,yDec = 5):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x,y,scrollX,velX,width,height,attack,health,dead)
        self.batZomb = pygame.image.load("images"+os.sep+'bird.png')
        self.deadbatZomb = pygame.image.load("images"+os.sep+'deadbird.png')
        self.rect = pygame.Rect(x,y,width,height)
        self.yDec = yDec
    def move(self):
        if not self.dead:
            self.x -= self.velX
            self.rect = pygame.Rect(self.x - self.scrollX, self.y, self.width - 35, self.height- 25)
    def draw(self):
        if not self.dead:
            gameDisplay.blit(self.batZomb,(self.x - self.scrollX, self.y))
        else:
            gameDisplay.blit(self.deadbatZomb,(self.x - self.scrollX, self.y + 10 + self.yDec))
    def removedraw(self):
        pygame.draw.rect(gameDisplay, (0,0,0),(self.x-100 - self.scrollX, self.y, self.width, self.height))

class Hero(pygame.sprite.Sprite):
    def __init__(self,mainX,mainY,scrollX,width = 102, height = 149):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images"+os.sep+'heroStand.jpg')
        self.images = ["images"+os.sep+'walk1.jpg',"images"+os.sep+'walk2.png',"images"+os.sep+'walk3.png',"images"+os.sep+'walk4.png',"images"+os.sep+'walk5.png',"images"+os.sep+'walk6.png']
        self.rect = pygame.Rect(mainX,mainY,width,height)
        self.x = mainX
        self.y = mainY
        self.scrollX = scrollX
        self.width = width
        self.height = height
    def draw(self):
        gameDisplay.blit(self.image1,(self.x + 5, self.y))
    def run(self,k,counter):
        counter = (counter + 1)%(len(self.images))
        pygame.draw.rect(gameDisplay, (0,0,0),(self.x,self.y,self.width,self.height))
        gameDisplay.blit(pygame.image.load(self.images[counter]),(self.x,self.y))
    def flipdraw(self):
        gameDisplay.blit(pygame.transform.flip(self.image1, True, False),(self.x,self.y))
    def fliprun(self,k,counter):
        counter = (counter + 1)%(len(self.images))
        pygame.draw.rect(gameDisplay, (0,0,0),(self.x,self.y,self.width,self.height))
        gameDisplay.blit(pygame.transform.flip(pygame.image.load(self.images[counter]),True,False),(self.x,self.y))

class Gun(pygame.sprite.Sprite):
    def __init__(self,ammo = 20, x = 0,y = 0,scrollX = 0,taken = True, mag = 10, image = None):
        self.ammo = ammo
        self.x = x
        self.y = y
        self.scrollX = scrollX
        self.taken = taken
        self.image = image
        self.mag = mag
        self.cap = mag
    def __repr__(self):
        return "Pistol"
    def draw(self):
        if self.image == None:
            pass
        else:
            gameDisplay.blit(pygame.image.load(self.image), (self.x - self.scrollX, self.y))

class Shotgun(Gun):
    def __init__(self, ammo, x, y, scrollX, taken, image, mag = 5, cap = 5, width = 29,height = 73):
        super().__init__(ammo,x,y,scrollX,taken,mag,cap)
        self.image = image
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x - width//2, y - height//2, width,height)
    def __repr__(self):
        return "Shotgun"

class Bullet(object):
    # Model
    def __init__(self, cx, cy,angle, speed,flip,isPellet):
        # A bullet has a position, a size, a direction, and a speed
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.angle = angle
        self.speed = speed
        self.rect = pygame.Rect(cx-self.r,cy-self.r,2*self.r,2*self.r)
        self.flip = flip
        self.isPellet = isPellet
    def draw(self):
        pygame.draw.circle(gameDisplay, (169,169,169), (int(self.cx), int(self.cy) + 10), self.r)
    def darkdraw(self): 
        pygame.draw.circle(gameDisplay, (0,0,0), (int(self.cx), int(self.cy) + 10), self.r)
    def moveBullet(self):
        self.cx += math.cos(math.radians(self.angle))*self.speed
        self.cy -= math.sin(math.radians(self.angle))*self.speed
        self.rect = pygame.Rect(self.cx - self.r, self.cy + self.r, 2*self.r, 2*self.r)
    def flipBullet(self):
        self.cx -= math.cos(math.radians(self.angle))*self.speed
        self.cy -= math.sin(math.radians(self.angle))*self.speed
        self.rect = pygame.Rect(self.cx-self.r - 101, self.cy + self.r, 2*self.r, 2*self.r)
    def flipdraw(self):
        pygame.draw.circle(gameDisplay, (169,169,169), (int(self.cx) - 101, int(self.cy) + 10), self.r)
    def darkflipdraw(self): 
        pygame.draw.circle(gameDisplay, (0,0,0), (int(self.cx) - 101, int(self.cy) + 10), self.r)
    def isOffscreen(self):
        return (self.cx + self.r <= 0 or self.cx - self.r >= display_width)

class Ammo(pygame.sprite.Sprite):
    def __init__(self,x,y,bullets = 10,pellets = 5, width = 91,height = 36, used = False):
        pygame.sprite.Sprite.__init__(self)
        self.ammoPic = pygame.image.load("images"+os.sep+'ammo.png').convert_alpha()
        self.usedammo = pygame.image.load("images"+os.sep+'usedammo.png').convert_alpha()
        self.x = x
        self.y = y
        self.bullets = bullets
        self.pellets = pellets
        self.width = width
        self.height = height
        self.used = used

class Health(pygame.sprite.Sprite):
    def __init__(self,x,y, healthgive = 25, width = 39, height = 39, used = False):
        self.x = x
        self.y = y
        self.healthgive = healthgive
        self.width = width
        self.height = height
        self.used = used
        self.healthPic = pygame.image.load("images"+os.sep+'doctor.png')

#################################################
# Game Introduction
#################################################       
def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if (display_width/(3.5) < mouse[0]  and mouse[0] < display_width/3.5 + 200) and (display_height*(0.5) < mouse[1]) \
                and (mouse[1] < display_height*(0.5) + 50):
                    intro = False
                    difficulty()
                if (display_width*(0.443) < mouse[0]  and mouse[0] < display_width*(0.443) + 200) and (display_height*(0.5) + 50 < mouse[1]) \
                and (mouse[1] < display_height*(0.5) + 100):
                    intro = False
                    keys()
                if (display_width*(0.443) < mouse[0]  and mouse[0] < display_width*(0.443) + 200) and (display_height*(0.35) + 50 < mouse[1]) \
                and (mouse[1] < display_height*(0.35) + 100):
                    intro = False
                    directions()
                if (display_width*(0.6) < mouse[0]  and mouse[0] < display_width*(0.6) + 200) and (display_height*(0.5) < mouse[1]) \
                and (mouse[1] < display_height*(0.5) + 50):
                    pygame.quit()
                    quit()
        background = pygame.image.load("images" + os.sep + 'l4d background.jpg')
        gameDisplay.blit(background,(0,0))
        largeText = pygame.font.Font("Fonts"+os.sep+'futurot.ttf',115)
        TextSurf, TextRect = text_objects("LEFT 4 DEAD", largeText)
        TextRect.center = ((display_width/2+30),(display_height/2 - 150))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.draw.rect(gameDisplay, (128,128,128),(display_width*(0.6),display_height*(0.5),100,50))
        mouse = pygame.mouse.get_pos()
        if (display_width/(3.5) < mouse[0]  and mouse[0] < display_width/(3.5) + 200) and (display_height*(0.5) < mouse[1]) \
        and (mouse[1] < display_height*(0.5) + 50):
                pygame.draw.rect(gameDisplay, (128,0,0),(display_width/3.5,display_height*(0.5),200,50))
        else:
            pygame.draw.rect(gameDisplay,(0,0,0),(display_width/3.5,display_height*(0.5),200,50))
        if (display_width*(0.6) < mouse[0]  and mouse[0] < display_width*(0.6) + 200) and (display_height*(0.5) < mouse[1]) \
        and (mouse[1] < display_height*(0.5) + 50):
                pygame.draw.rect(gameDisplay, (128,0,0),(display_width*(0.6),display_height*(0.5),200,50))
        else:
            pygame.draw.rect(gameDisplay, (0,0,0),(display_width*(0.6),display_height*(0.5),200,50))
        if (display_width*(0.443) < mouse[0]  and mouse[0] < display_width*(0.443) + 200) and (display_height*(0.5) + 50 < mouse[1]) \
        and (mouse[1] < display_height*(0.5) + 100):
            pygame.draw.rect(gameDisplay, (128,0,0),(display_width*(0.443),display_height*(0.5) + 50,200,50))
        else:
            pygame.draw.rect(gameDisplay, (0,0,0),(display_width*(0.443),display_height*(0.5) + 50,200,50))
        if (display_width*(0.443) < mouse[0]  and mouse[0] < display_width*(0.443) + 200) and (display_height*(0.35) + 50 < mouse[1]) \
        and (mouse[1] < display_height*(0.35) + 100):
            pygame.draw.rect(gameDisplay, (128,0,0),(display_width*(0.443),display_height*(0.35) + 50,200,50))
        else:
            pygame.draw.rect(gameDisplay, (0,0,0),(display_width*(0.443),display_height*(0.35) + 50,200,50))
        playText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 30)
        textSurf, textRect = text_objects("Play", playText)
        textRect.center = ( (display_width/3.5+(100)), (display_height*(0.5)+(50/2)) )
        gameDisplay.blit(textSurf,textRect)
        textSurf, textRect = text_objects("Exit", playText)
        textRect.center = ( (display_width*0.6+(100)), (display_height*(0.5)+(50/2)) )
        gameDisplay.blit(textSurf, textRect)
        textSurf, textRect = text_objects("Keys", playText)
        textRect.center = ( (display_width*0.443+(100)), (display_height*(0.5) + 75) )
        gameDisplay.blit(textSurf, textRect)
        keyText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 25)
        textSurf, textRect = text_objects("Directions", keyText)
        textRect.center = ( (display_width*0.443+(100)), (display_height*(0.35) + 75) )
        gameDisplay.blit(textSurf, textRect)
        pygame.display.update()
        clock.tick(30)

#################################################
# Difficulty
#################################################   
def difficulty():
    start = True
    titleText = pygame.font.Font("Fonts" + os.sep + "futurot.ttf",100)
    gameText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 30)
    background = pygame.image.load("images" + os.sep + 'difficultBackground.jpg')
    while start:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if (display_width*0.43 < mouse[0]  and mouse[0] < display_width*0.43 + 200) and (display_height*(0.36) < mouse[1]) \
                and (mouse[1] < display_height*(0.36) + 65):
                    start = False
                    gameLoop(0)
                if (display_width*(0.385) < mouse[0]  and mouse[0] < display_width*(0.385) + 320) and (display_height*(0.55) < mouse[1]) \
                and (mouse[1] < display_height*(0.55) + 70):
                    start = False
                    gameLoop(1)
                if (display_width*(0.42) < mouse[0]  and mouse[0] < display_width*(0.42) + 225) and (display_height*(0.75)< mouse[1]) \
                and (mouse[1] < display_height*(0.75) + 75):
                    start = False
                    gameLoop(2)
        gameDisplay.blit(background,(0,0))
        
        textSurf, textRect = text_objects("Difficulty Level", titleText)
        textRect.center = ( (display_width*0.5, (display_height*(0.2) ) ) )
        gameDisplay.blit(textSurf, textRect)
        
        keyText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 75)
        textSurf, textRect = text_objects("Easy", keyText)
        textRect.center = ( (display_width*0.5), (display_height*(0.4)) )
        gameDisplay.blit(textSurf, textRect)
        
        textSurf, textRect = text_objects("Medium", keyText)
        textRect.center = ( (display_width*0.5), (display_height*(0.6)) )
        gameDisplay.blit(textSurf, textRect)
        
        textSurf, textRect = text_objects("Hard", keyText)
        textRect.center = ( (display_width*0.5), (display_height*(0.8)) )
        gameDisplay.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(30)


#################################################
# Key Press Directions
#################################################   
def keys():   
    direct = True
    directScreen = pygame.image.load("images"+os.sep+'directionPage.jpg')
    gameDisplay.blit(directScreen,(0,0))
    while direct:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_b:
                    gameIntro()
                    direct = False
        text = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 30)
        
        textSurf, textRect = text_objects("Press A to walk left", text)
        textRect.center = ( (display_width/3), (display_height*(0.65)) )
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Press D to walk right", text)
        textRect.center = ( (display_width/3), (display_height*(0.75) ))
        gameDisplay.blit(textSurf, textRect)
        
        textSurf, textRect = text_objects("Press W to jump", text)
        textRect.center = ( (display_width/3), (display_height*(0.85)))
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Press Space to shoot", text)
        textRect.center = ( (display_width*(2/3)), (display_height*(0.65)))
        gameDisplay.blit(textSurf,textRect) 
            
        textSurf, textRect = text_objects("Press up or down to aim", text)
        textRect.center = ( (display_width*(2/3)), (display_height*(0.75)) )
        gameDisplay.blit(textSurf, textRect)
        
        textSurf, textRect = text_objects("Press B to exit Directions", text)
        textRect.center = ( (display_width*(0.8)), (display_height*(0.95) ) )
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Press E to interact with items", text)
        textRect.center = ( (display_width*(2/3)), (display_height*(0.85) ) )
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        clock.tick(30)

#################################################
# Game Directions
#################################################   
def directions():
    direct = True
    gameDisplay.fill((0,0,0))
    while direct:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_b:
                    gameIntro()
                    direct = False
        backText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 30)
        
        textSurf, textRect = text_objects("Shoot zombies either in the body or in the head for more damage!", backText)
        textRect.center = ( (display_width*(0.5)), (display_height*(0.15) ) )
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Be careful with your ammo and health!", backText)
        textRect.center = ( (display_width*(0.5)), (display_height*(0.3) ) )
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Zombies will be coming in from all sides", backText)
        textRect.center = ( (display_width*(0.5)), (display_height*(0.45) ) )
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Get to the car to survive for another night", backText)
        textRect.center = ( (display_width*(0.5)), (display_height*(0.6) ) )
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("You can only shoot when standing still, be careful...", backText)
        textRect.center = ( (display_width*(0.5)), (display_height*(0.75) ) )
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Press B to exit Directions", backText)
        textRect.center = ( (display_width*(0.8)), (display_height*(0.95) ) )
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        clock.tick(30)

#################################################
# Game Loop
#################################################   

def bulletDraw(bullet,bulletList):
        if not bullet.flip:
            bullet.darkdraw()
            bullet.moveBullet()
            bullet.draw()
            pygame.draw.rect(gameDisplay,(192,192,192),(bullet.cx - bullet.r, bullet.cy + bullet.r, 2*bullet.r, 2*bullet.r))
        else:
            bullet.darkflipdraw()
            bullet.flipBullet()
            bullet.flipdraw()
            pygame.draw.rect(gameDisplay,(192,192,192),(bullet.cx-bullet.r - 101, bullet.cy + bullet.r, 2*bullet.r, 2*bullet.r))
        if bullet.isOffscreen() or bullet.cy + bullet.r > display_height*0.955:
            bullet.darkdraw()
            bulletList.remove(bullet)

def createZombie(randomNum,zombieList,randomFlip,scrollX):
    if randomNum <= 5:
        if randomFlip == 0:
            zombieList.append(Zombie(display_width + scrollX,display_height*0.78+10,scrollX,2))
        else:
            zombieList.append(FlippedZombie(0 + scrollX,display_height*0.78+10,scrollX,-2))
    elif randomNum == 6 or randomNum == 7:
        zombieList.append(Bat(display_width + scrollX, random.randint(250,350), scrollX, 3))
    elif randomNum == 8 or randomNum == 9:
        if randomFlip == 0:
            zombieList.append(Sprinter(display_width + scrollX,display_height*0.78+10,scrollX,4))
        else:
            zombieList.append(FlippedSprinter(0 + scrollX, display_height*0.78+10,scrollX,-4))
    elif randomNum == 10:
        if randomFlip == 0:
            zombieList.append(Giant(display_width + scrollX, display_height*0.78+10,scrollX,1))
        else:
            zombieList.append(FlippedGiant(0 + scrollX, display_height*0.78+10,scrollX,-1))

def bulletDetection(zomb,bullet,bulletList):
    if isinstance(zomb,Bat) == False:
        if bullet.rect.colliderect(zomb.head):
            print('head')
            zomb.health -= 25
            bulletList.remove(bullet)
            bullet.darkdraw()
    if bullet.rect.colliderect(zomb.rect):
        print('body')
        zomb.health -= 10
        bulletList.remove(bullet)
        bullet.darkdraw()  
    
def drawAmmoBox(scrollX,ammoBox):
    if scrollX > 0:
        if ammoBox.used:
            gameDisplay.blit(ammoBox.usedammo,(ammoBox.x - scrollX, ammoBox.y + 5))
        else:
            gameDisplay.blit(ammoBox.ammoPic,(ammoBox.x - scrollX, ammoBox.y + 5))
    else:
        if ammoBox.used:
            gameDisplay.blit(ammoBox.usedammo,(ammoBox.x, ammoBox.y + 5))
        else:
            gameDisplay.blit(ammoBox.ammoPic,(ammoBox.x, ammoBox.y + 5))

def drawHealthBox(scrollX,healthBox):
    if scrollX > 0:
        if not healthBox.used:
            gameDisplay.blit(healthBox.healthPic,(healthBox.x - scrollX, healthBox.y)) 
    else: 
        if not healthBox.used:
            gameDisplay.blit(healthBox.healthPic,(healthBox.x, healthBox.y)) 

def deadZombDraw(deadZomb):
    if isinstance(deadZomb,Bat):
        if deadZomb.yDec + 5 < 420:
            deadZomb.yDec += 5
    deadZomb.draw()
    
def createHud(healthPool):
    if healthPool > 0:
        pygame.draw.rect(gameDisplay,(50,205,50),(20,20,(500*(healthPool*0.01)),30))
    pygame.draw.rect(gameDisplay,(192,192,192),(20,75,200,50))
    pygame.draw.rect(gameDisplay,(192,192,192),(245,75,265,50))
    
def checkDeath(healthPool,crashed):
    if healthPool <= 0:
        crashed = True
        deathScreen()

def drawText(gun,ammoText,gameText,scrollX):
    textSurf, textRect = text_objects("Ammo: %d of %d" % (gun.mag,gun.ammo), ammoText)
    textRect.center = ( 117, 100 )
    gameDisplay.blit(textSurf,textRect)
    
    textSurf, textRect = text_objects("Press T to get out", gameText)
    textRect.center = ( 5100 - scrollX, display_height*0.75 )
    gameDisplay.blit(textSurf,textRect)
    
    textSurf, textRect = text_objects("Cannot go back", gameText)
    textRect.center = ( display_width/2 - scrollX, display_height*0.675 )
    gameDisplay.blit(textSurf,textRect)
    
    textSurf, textRect = text_objects("Gun: %s" % (gun), gameText)
    textRect.center = ( 375, 100 )
    gameDisplay.blit(textSurf,textRect)

def gameLoop(difficulty): 
    zombieList = []
    deadZombList = []
    bulletList = []
    diffList = [15,25,35]
    secList = [3,2,1]
    pistol = Gun()
    shotgun = Shotgun(10,display_width//2.79,display_height*0.8,0,False,"images"+os.sep+'shotgun.png')
    gunList = [pistol]
    noGunList = [shotgun]
    jumpBoost = 0
    gunAngle = 0
    healthPool = 100
    frame_count = 0
    frame_rate = 60
    zombieCount = 0
    crashed = False
    x_change = 0
    y_change = 0
    mainX = 0
    mainY = display_height*0.78
    isJumping = False
    canShoot = True
    swipe = False
    running = False
    flipImage = False
    carMove = False
    counter = 0
    yDec = 0
    gunIndex = 0
    scrollX = 0
    k = 0
    shootProj = 0
    reloadTime = 0
    reloading = False
    carValX = 0
    ammoBoxList = [Ammo(display_width//2 - 100, display_height*0.915,10,random.randint(5,8)),Ammo(2500,display_height*0.915,15,4)]
    healthBoxList = [Health(display_width - 50, display_height*0.915 - 5),Health(3000,display_height*0.915 - 5,random.randint(25,40))]
    moonBackground = pygame.image.load("images"+os.sep+'moon.jpg')
    carPic = pygame.image.load("images"+os.sep+'endingCar.png')
    text = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 15)  
    gameText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 30)
    clock = pygame.time.Clock()
    while not crashed:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                        x_change = -5
                        flipImage = True
                        running = True
                if event.key == pygame.K_d:
                        flipImage = False
                        x_change = 5
                        running = True
                if event.key == pygame.K_w:
                    if not isJumping and jumpBoost == 0:
                        isJumping = True
                        jumpBoost = 15
                if event.key == pygame.K_e:
                    for ammoBox in ammoBoxList:
                        if ammoBox.rect.colliderect(hero.rect):
                            if not ammoBox.used:
                                if isinstance(gun,Shotgun):
                                    gun.ammo += ammoBox.pellets
                                else:
                                    gun.ammo += ammoBox.bullets
                                ammoBox.used = True
                    for healthBox in healthBoxList:
                        if healthBox.rect.colliderect(hero.rect):
                            if healthPool + healthBox.healthgive >= 100:
                                healthPool = 100
                            else:
                                healthPool += healthBox.healthgive
                            healthBox.used = True
                    if hero.rect.colliderect(shotgun.rect):
                        if not shotgun.taken:
                            gunList.append(shotgun)
                            noGunList.remove(shotgun)
                            shotgun.taken = True
                if event.key == pygame.K_t:
                    if hero.x >= 5000 - scrollX:
                        carMove = True
                if event.key == pygame.K_r:
                    reloading = True
                if event.key == pygame.K_q:
                    gunIndex = (gunIndex + 1)%(len(gunList))
                if event.key == pygame.K_SPACE:
                    if canShoot:
                        if gunIndex == 0:
                            if flipImage:
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle,7,True,False))
                                gun.mag -= 1
                            else:
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle,7,False,False))
                                gun.mag -= 1
                        elif gunIndex == 1:
                            if flipImage:
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle,10,True,False))
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle + 5,10,True,False))
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle - 5,10,True,False))
                                gun.mag -= 1
                            else:
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle,10,False,False))
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle + 5,10,False,False))
                                bulletList.append(Bullet(mainX + 100, mainY + (mainY*0.07),gunAngle - 5,10,False,False))
                                gun.mag -= 1
                if event.key == pygame.K_UP:
                    gunAngle += 7
                if event.key == pygame.K_DOWN:
                    gunAngle -= 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w:
                    x_change = 0
                    y_change = 0
                running = False
                
        frame_count += 1
        total_seconds = frame_count / frame_rate
            
        if scrollX > 0:
            gameDisplay.fill((0,0,0),(0 - scrollX,0,display_width + scrollX,display_height))  
        else:
            gameDisplay.fill((0,0,0),(0,0,display_width,display_height))            

        pygame.draw.rect(gameDisplay,(221,194,131),(0-scrollX,display_height*0.705,display_width//2,display_height*0.247))

        gameDisplay.blit(moonBackground,(display_width - 200, 30))

        pygame.draw.line(gameDisplay,(128,0,0),(0 - scrollX, display_height*0.702),(display_width//2 - scrollX, display_height*0.702),3)
                    
        if jumpBoost > 0:
            y_change = -4
            jumpBoost = jumpBoost - 1
        else: 
            y_change = 4
        if mainY + y_change <= display_height*0.78:
            mainY += y_change
        else:
            isJumping = False
                
        if mainX >= display_width//2:
            if scrollX >= display_width/2.05:
                if total_seconds % secList[difficulty] == 0:
                    maxZombies = diffList[difficulty]
                    if zombieCount < maxZombies:
                        zombieCount += 1
                        randomNum = random.choice([0,1,2,3,4,5,6,7,8,9,10])
                        randomFlip = random.choice([0,1])
                        createZombie(randomNum,zombieList,randomFlip,scrollX)

        for ammoBox in ammoBoxList:
            ammoBox.rect = pygame.Rect(ammoBox.x - scrollX, ammoBox.y, ammoBox.width - 30, ammoBox.height)
    
        for healthBox in healthBoxList:
            healthBox.rect = pygame.Rect(healthBox.x - scrollX, healthBox.y, healthBox.width, healthBox.height)

        hero = Hero(mainX,mainY,scrollX)

        if mainX <= display_width//2:
            mainX += x_change
        elif scrollX + x_change >= 0:
            scrollX += x_change
        
        zombDonk = (pygame.sprite.spritecollide(hero,zombieList,False,collided = None))
        
        flipList = list(filter(lambda zombie: zombie.x < display_width//2 + zombie.scrollX, zombDonk))
        regList =  list(filter(lambda zombie: zombie.x > display_width//2 + zombie.scrollX, zombDonk))
        
        if len(flipList) >= 1 and len(regList) >= 1:
            scrollX -= x_change
    
        textSurf, textRect = text_objects("Pistol", gameText)
        textRect.center = ( display_width//4.5 - scrollX, display_height*0.75)
        gameDisplay.blit(textSurf,textRect)
        
        pygame.draw.rect(gameDisplay,(192,192,192),(display_width//5.1 - scrollX,display_height*0.79,75,100))

        textSurf, textRect = text_objects("Shotgun", gameText)
        textRect.center = ( display_width//3 + 50 - scrollX, display_height*0.75)
        gameDisplay.blit(textSurf,textRect)

        pygame.draw.rect(gameDisplay,(192,192,192),(display_width//2.9 - scrollX,display_height*0.79,75,100))
        
        for gun in noGunList:
            gun.scrollX = scrollX
            gun.draw()

        if carMove == True:
            carValX += 2
            scrollX -= x_change
            pygame.draw.rect(gameDisplay,(0,0,0),(mainX,mainY,hero.width + 5, hero.height))
            gameDisplay.blit(carPic,(5000 - scrollX + carValX,display_height*0.825))
            hero = Hero(0,-500,scrollX)
            if carValX == 500:
                endScreen()
                crashed = True
        else:
            gameDisplay.blit(carPic,(5000 - scrollX,display_height*0.825))  

        timeRun = clock.tick()
        if flipImage == False:
            if running == False:
                hero.draw()
            else:
                k += timeRun
                if k > 10:
                    counter += 1
                    k = 0
                hero.run(k,counter)
        else:
            if running == False:
                hero.flipdraw()
            else:
                k += timeRun
                if k > 10:
                    counter += 1
                    k = 0
                hero.fliprun(k,counter)      

        for zomb in zombieList:
            zomb.scrollX = scrollX
            if isinstance(zomb,Bat) == False:
                zomb.move()
                if pygame.sprite.collide_rect(zomb,hero):
                    attackDamage = zomb.attack
                    healthPool -= attackDamage
                    zomb.x += zomb.velX
                zomb.draw()
            else:
                zomb.move()
                zomb.draw()
            if zomb.health <= 0:   
                zombieList.remove(zomb)
                zomb.removedraw()
                zomb.death()
                deadZombList.append(zomb)
            
            if isinstance(zomb,Bat):
                if zomb.x + zomb.width - scrollX > 0:
                    shootProj += timeRun
                    if shootProj >= 100:
                        shootProj = 0
                        angling = (math.degrees(abs(math.acos((zomb.x-scrollX - hero.x)/distance(zomb.x-scrollX,hero.x,zomb.y,hero.y)))))
                        bulletList.append(Bullet(zomb.x - scrollX + 100,zomb.y + 50,-1*angling + 5,5,True,True))

            for bullet in bulletList:
                if not bullet.isPellet:
                    bulletDetection(zomb,bullet,bulletList)
                else:
                    if bullet.rect.colliderect(hero.rect):
                        bulletList.remove(bullet)
                        bullet.darkdraw()
                        healthPool -= 5
        
        for bullet in bulletList:
            bulletDraw(bullet,bulletList)

        gun = gunList[gunIndex]
                
        if gun.ammo <= 0 and gun.mag == 0:
            canShoot = False
            reloading = False
        elif gun.mag == 0 or reloading == True:
            canShoot = False
            reloadTime += timeRun
            textSurf, textRect = text_objects("Reloading", gameText)
            textRect.center = ( 275, 175 )
            gameDisplay.blit(textSurf,textRect)
            if reloadTime >= 100:
                canShoot = True
                reloadTime = 0
                if gun.ammo >= gun.cap:
                    gun.ammo -= (gun.cap - gun.mag)
                    gun.mag = gun.cap
                else:
                    gun.mag = gun.ammo
                    gun.ammo = 0
                reloading = False
        else: 
            canShoot = True

        for deadZomb in deadZombList:
            deadZomb.scrollX = scrollX
            deadZombDraw(deadZomb)

        for ammoBox in ammoBoxList:
            drawAmmoBox(scrollX,ammoBox)
        
        for healthBox in healthBoxList:
            drawHealthBox(scrollX,healthBox)

        if scrollX > 0:
            pygame.draw.line(gameDisplay,(128,0,0),(0,display_height*0.955),(display_width + scrollX,display_height*0.955),3)
        else:
            pygame.draw.line(gameDisplay,(128,0,0),(0,display_height*0.955),(display_width,display_height*0.955),3)
                
        pygame.draw.rect(gameDisplay,(128,0,0),(20,20,500,30))
        
        createHud(healthPool)
        
        textSurf, textRect = text_objects("Health", gameText)
        textRect.center = ( 270, 35 )
        gameDisplay.blit(textSurf,textRect)
                        
        ammoText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 21)
        drawText(gun,ammoText,gameText,scrollX)
        checkDeath(healthPool,crashed)

        pygame.draw.line(gameDisplay,(96,62,17),(display_width//2 - scrollX, display_height*0.955),(display_width//2-scrollX,display_height*0.7),7)
        pygame.draw.circle(gameDisplay,(128,0,0),(display_width//2 - scrollX,int(display_height*0.8275)),10,3)
        pygame.draw.circle(gameDisplay,(255,255,255),(display_width//2 - scrollX,int(display_height*0.8275)),6,3)

        pygame.display.update()
        clock.tick(60)

#################################################
# Ending Screen
#################################################   
def endScreen():
    crashed = False
    background = pygame.image.load("images"+os.sep+'sunshining.jpg')
    gameDisplay.blit(background,(0,0))
    clock = pygame.time.Clock()
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_t:
                    crashed = True
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    crashed = True
                    gameLoop()
            
        gameText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 150)
        textSurf, textRect = text_objects("You survived...", gameText)
        textRect.center = (display_width/2, display_height/4)
        gameDisplay.blit(textSurf,textRect)
        
        text = pygame.font.Font("Fonts" + os.sep + "futurot.ttf", 75)
        textSurf, textRect = text_objects("Press T to quit game", text)
        textRect.center = (display_width/2, display_height/1.85)
        gameDisplay.blit(textSurf,textRect)
        
        textSurf, textRect = text_objects("Press R to play again", text)
        textRect.center = (display_width/2, display_height/2.5)
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        clock.tick(30)


#################################################
# Death Screen
#################################################   
def deathScreen():
    end = True
    deathImage = random.choice(["images"+os.sep+'firstDeath.jpg',"images"+os.sep+'secondDeath.jpg',"images"+os.sep+'thirdDeath.jpg',"images"+os.sep+'fourthDeath.jpg'])
    while end:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()  
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    gameLoop()
                    end = False
        deathback = pygame.image.load(deathImage)
        gameDisplay.blit(deathback,(0,0))
        gameText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 150)
        textSurf, textRect = text_objects("YOU'RE DEAD", gameText)
        textRect.center = (display_width/2, display_height/2)
        gameDisplay.blit(textSurf,textRect)
        restartText = pygame.font.Font("Fonts"+os.sep+"futurot.ttf", 40)
        textSurf, textRect = text_objects("Press R to fight again...", restartText)
        textRect.center = (display_width/2, display_height/2 + 100)
        gameDisplay.blit(textSurf,textRect)
        pygame.display.update()
        clock.tick(30)

gameIntro()
pygame.quit()
quit()