import pygame

class dino:
    
    models = ["assets\dino0000.png","assets\dinorun0000.png","assets\dino0000.png", "assets\dinorun0001.png"]
    normalModels = ["assets\dino0000.png","assets\dinorun0000.png","assets\dino0000.png", "assets\dinorun0001.png", "assets\dinoJump0000.png"]
    duckModels = ["assets\dinoduck0000.png","assets\dinoduck0001.png","assets\dinoduck0000.png","assets\dinoduck0001.png"]
    specialModels = ["assets\dinoJump0000.png", "assets\dinoDead0000.png"]
    state = 0
    jumping = False
    size = (48, 48)
    ducking = False
    counter = 0
    frameInterval = 5
    
    def __init__ (self, posX, posY):
        self.defaultPosY = posY
        self.posX = posX
        self.posY = posY - self.size[1]
        self.velocity = 0
        self.model = pygame.image.load(self.models[self.state])
        self.model = pygame.transform.scale(self.model, self.size)
    
    def jump(self, velocity, gravity):
        if not self.jumping and not self.ducking:
            self.velocity = velocity
            self.posY = self.posY - self.velocity
            self.jumping = True
    
    def land(self, gravity):
        if (self.posY < self.defaultPosY - self.size[1]):
            self.velocity = self.velocity - gravity
            self.posY = self.posY - self.velocity
        else:
            self.models = self.normalModels
            self.jumping = False
            
    def duck(self): 
        if not self.jumping and not self.ducking:
            self.ducking = True
            self.size = (68, 34)
            self.models = self.duckModels
            
    def unDuck(self):
        if self.ducking:
            self.ducking = False
            self.size = (48, 48)
            self.models = self.normalModels
    
    def switchState(self):
        if self.state < 3:
            self.state = self.state+1
            self.posY = self.defaultPosY - self.size[1]
        else:
            self.state = 0
            self.posY = self.defaultPosY - self.size[1]
        self.counter = 0
    
    def move(self):
        if self.jumping:
            self.state = 0
            self.models = self.specialModels
        elif self.counter >= self.frameInterval:
            self.switchState()
        self.counter = self.counter + 1
        self.model = pygame.image.load(self.models[self.state])
        self.model = pygame.transform.scale(self.model, self.size)