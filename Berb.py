import pygame
from random import randint

class berb:
    
    state = 0
    models = ["assets\\berd.png","assets\\berd2.png"]
    size = [(46, 40),(46, 40)]
    
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY - randint(0, 2)*40 - self.size[0][1]
        self.model = pygame.image.load(self.models[self.state])
        self.model = pygame.transform.scale(self.model, self.size[0])
    
    def move(self, velocity):
        self.posX = self.posX - velocity
        if self.state < 1:
            self.state = self.state + 1
        else:
            self.state = 0
        self.model = pygame.image.load(self.models[self.state])
        self.model = pygame.transform.scale(self.model, self.size[0])