
import pygame, sys
from pygame.locals import *
import random
 

def main():
    pygame.init()
    
    FPS = 60
    FramePerSec = pygame.time.Clock()
    
    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Screen information
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")
            
    c1 = Castle((30,30))
    c2 = Castle((500,500))
    c3 = Castle((550,750))
    c4 = Castle((30,750))
    c5 = Castle((550,30))
    c6 = Castle((300,400))

    #E1 = Enemy()
    
    while True:     
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for c in Castle.instances:
            c.update()
        for x in Person.instances:
            x.update()
        
        pygame.display.flip()
        DISPLAYSURF.fill(WHITE)
        for c in Castle.instances:
            if c.rect.collidepoint(pygame.mouse.get_pos()):
                c.drawinfo(DISPLAYSURF)
            c.draw(DISPLAYSURF)
        for x in Person.instances:
            x.draw(DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(FPS)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface() 
        self.image = pygame.image.load("Enemy.png")
        #self.screen.blit(pygame.transform.scale(self.image (40,40)))
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
 


class Person(pygame.sprite.Sprite):
    instances = []
    def __init__(self, castle, location):

        super().__init__()
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load("playersmall.png")
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.castle = castle
        self.target = self.choice_excluding(Castle.instances, self.castle)
        Person.instances.append(self)

    def choice_excluding(self, lst, exception):
        possible_choices = [v for v in lst if v != exception]
        return random.choice(possible_choices)
 
    def update(self):
        if(pygame.Rect.colliderect(self.rect, self.target.rect)):
            self.castle.people.remove(self)
            Person.instances.remove(self)
        x, y = self.target.rect.center
        x2, y2 = self.rect.center
        xration = 1 if x2 < x else -1 if x != x2 else 0
        yration = 1 if y2 < y else -1 if y != y2 else 0
        self.rect.move_ip(xration, yration)

    def distance(self, x, y):
        if x >= y:
            result = x - y
        else:
            result = y - x
        return result

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Castle(pygame.sprite.Sprite):
    instances = []
    def __init__(self, location):

        super().__init__()
        self.foodProd = {"fish":100, "goat": 0}
        self.population = 100
        self.people = []
        self.last = pygame.time.get_ticks()
        self.cooldown = 100
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load("smallercastle.png")
        #self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.center = location        
        Castle.instances.append(self)

    def drawinfo(self, surface):
        base_font = pygame.font.Font(None, 32)
        user_text = str(self.population)
        input_rect = pygame.Rect(200, 0, 140, 32)
        pygame.draw.rect(surface, pygame.Color("gray"), input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        surface.blit(text_surface, (input_rect.x+5, input_rect.y+5))

    def __str__(self):
        stringout = ""
        stringout += self.population
        return "foo"

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.populationgrowth()
            self.last = now
            if len(self.people) < 11:
                self.create_person()

    def populationgrowth(self):
        values = self.foodProd.values()
        total = sum(values)
        if self.population < total: self.population += 1 

    def create_person(self):
        self.population -= 1
        self.people.append(Person(self, self.rect.center))
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)    
main()