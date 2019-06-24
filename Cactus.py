import pygame
from random import randint
import os


class cactus:

    models = [os.path.join('assets', 'cactusBig0000.png'), os.path.join(
        'assets', 'cactusSmall0000.png'), os.path.join('assets', 'cactusSmallMany0000.png')]
    size = [(30, 60), (20, 40), (60, 40)]

    def __init__(self, posX, posY):  # Constructor
        self.state = randint(0, 2)
        self.posX = posX
        self.posY = posY - self.size[self.state][1]
        self.model = pygame.image.load(self.models[self.state])
        self.model = pygame.transform.scale(self.model, self.size[self.state])

    def move(self, velocity):  # Update position, as obstacles are the things that move, not the dino
        self.posX = self.posX - velocity
