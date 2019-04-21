import sys, pygame
from Dino import dino
from Cactus import cactus
from Berb import berb
from random import randint
from math import ceil

pygame.font.init()
myfont = pygame.font.Font("assets\PressStart2P-Regular.ttf", 16)

title = "Dino"
displayW = 1024
displayH = 576
screen = pygame.display.set_mode((displayW, displayH))
pygame.display.set_caption(title)

background = 255,255,255
gravity = 1
clock = pygame.time.Clock()
framerate = 60

multiplier = 1
score = 0
Dino = dino(displayW*0.075, displayH*0.7)
obstacles = [cactus(displayW, displayH*0.7), cactus(displayW + randint(displayW/2, displayW), displayH*0.7)]

yVelocity = 18
xVelocity = 4*multiplier
isBerb = 1
running = True

def newObstacle():
    if (obstacles[0].posX <= 0-obstacles[0].size[obstacles[0].state][0]):
        obstacles[0] = obstacles[1]
        if not randint(0, isBerb):
            obstacles[1] = cactus(displayW+randint(displayW/2, displayW), displayH*0.7)
        else:
            obstacles[1] = berb(displayW+randint(displayW/2, displayW), displayH*0.7)
            
def collide():
    if (Dino.posY + Dino.size[1] >= obstacles[0].posY and Dino.posY + Dino.size[1] <= obstacles[0].posY + obstacles[0].size[obstacles[0].state][1]) or (Dino.posY >= obstacles[0].posY and Dino.posY <= obstacles[0].posY + obstacles[0].size[obstacles[0].state][1]):
        if Dino.posX + Dino.size[0] >= obstacles[0].posX and Dino.posX + Dino.size[0] <= obstacles[0].posX + obstacles[0].size[obstacles[0].state][0]:
            return True
        elif Dino.posX >= obstacles[0].posX and Dino.posX <= obstacles[0].posX + obstacles[0].size[obstacles[0].state][0]:
            return True
            
def moveObjects():
    if Dino.jumping:
        Dino.land(gravity)
    Dino.move()
    obstacles[0].move(xVelocity*multiplier)
    obstacles[1].move(xVelocity*multiplier)

def renderObjects():
    textsurface = myfont.render(str(ceil(score)), False, (0, 0, 0))
    screen.blit(textsurface,(0.9*displayW, 0.08*displayH))
    screen.blit(obstacles[0].model, (obstacles[0].posX, obstacles[0].posY))
    screen.blit(obstacles[1].model, (obstacles[1].posX, obstacles[1].posY))
    screen.blit(Dino.model, (Dino.posX, Dino.posY))

def pause():
    global score, dino, obstacles, multiplier
    while 1:
        for event in pygame.event.get():
            if event.type == 12:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    multiplier = 1
                    score = 0
                    Dino = dino(displayW*0.075, displayH*0.7)
                    obstacles = [cactus(displayW, displayH*0.7), cactus(displayW + randint(displayW/2, displayW), displayH*0.7)]
                    play()

def play():
    global running, score, multiplier, clock, Dino, obstacles
    while running:
        for event in pygame.event.get():
            if event.type == 12:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Dino.jump(yVelocity, gravity)
                if event.key == pygame.K_DOWN:
                    Dino.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    Dino.unDuck()

        if collide():
            break
        
        screen.fill(background)
        pygame.draw.line(screen, (0,0,0), (displayW, displayH*0.68), (0, displayH*0.68))
        moveObjects()
        renderObjects()
        newObstacle()
        score = score + 0.1
        multiplier = ceil(score/100)
        pygame.display.update()
        clock.tick(framerate)

    Dino.model = pygame.image.load(Dino.specialModels[1])
    Dino.model = pygame.transform.scale(Dino.model, (48, 48))
    screen.fill(background)
    pygame.draw.line(screen, (0,0,0), (displayW, displayH*0.68), (0, displayH*0.68))
    renderObjects()
    pygame.display.update()
    pause()

play()