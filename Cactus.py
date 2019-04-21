import pygame
from random import randint

class cactus:
    
    models = ["assets\cactusBig0000.png", "assets\cactusSmall0000.png", "assets\cactusSmallMany0000.png"]
    size = [(30, 60), (20, 40), (60, 40)]
    
    def __init__(self, posX, posY):
        self.state = randint(0,2)
        self.posX = posX
        self.posY = posY - self.size[self.state][1]
        self.model = pygame.image.load(self.models[self.state])
        self.model = pygame.transform.scale(self.model, self.size[self.state])
        
    def move(self, velocity):
        self.posX = self.posX - velocity