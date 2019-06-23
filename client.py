import pygame
from Dino import dino
from Cactus import cactus
from Berb import berb
from random import randint
from math import floor, ceil
import socket
import threading

# Socket
HOST = "192.168.1.94"
PORT = 1234
connection_established = False
conn, addr = None, None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Threading
def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    
def recData():
    pass   
    
def connectToServer():
    global connection_established, conn, addr, sock, running, showResult
    conn = sock.connect((HOST, PORT))
    sock.send('Connecting...'.encode())
    while True:
        recvData = sock.recv(1024).decode()
        print(recvData)
        connection_established = True
        if recvData == "won":
            showResult = True
            running = False
        if recvData == "go":
            reset()
            running = True

    
createThread(connectToServer)

# Game
pygame.font.init()
myfont = pygame.font.Font("assets\PressStart2P-Regular.ttf", 16)

title = "Dino (client)"
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
showResult = False

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
    global showResult
    if showResult:
        result = myfont.render("You won", False, (0, 0, 0))
        screen.blit(result,(0.45*displayW, 0.08*displayH))
    textsurface = myfont.render(str(ceil(score)), False, (0, 0, 0))
    screen.blit(textsurface,(0.9*displayW, 0.08*displayH))
    screen.blit(obstacles[0].model, (obstacles[0].posX, obstacles[0].posY))
    screen.blit(obstacles[1].model, (obstacles[1].posX, obstacles[1].posY))
    screen.blit(Dino.model, (Dino.posX, Dino.posY))

def reset():
    global multiplier, score, Dino, obstacles
    multiplier = 1
    score = 0
    Dino = dino(displayW*0.075, displayH*0.7)
    obstacles = [cactus(displayW, displayH*0.7), cactus(displayW + randint(displayW/2, displayW), displayH*0.7)]
    
def pause():
    global score, Dino, obstacles, multiplier, running, sock, connection_established, showResult
    print("Pause:", running)    
    while not running:
        for event in pygame.event.get():
            if event.type == 12:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset()
                    if connection_established:
                        sock.send("go".encode())
                    showResult = False
                    running = True
    play()

def play():
    global running, score, multiplier, clock, Dino, obstacles, connection_established, sock
    print("Play:", running)
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
            if connection_established:
                print('sending result')
                data = "won"
                sock.send(data.encode())
                running = False                
            break
        
        screen.fill(background)
        pygame.draw.line(screen, (0,0,0), (displayW, displayH*0.68), (0, displayH*0.68))
        moveObjects()
        renderObjects()
        newObstacle()
        score = score + 0.125
        multiplier = 1 + floor(score/100)/2
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