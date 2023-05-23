import pygame
from pygame.locals import *  # noqa
import sys
import random


class FlappyBird:
    pygame.init()
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(65, 50, 50, 50) #границы птички
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.background = pygame.image.load("assets/background.png").convert()
        self.gap = 150 #расстояние между колоннами внутри (прорезь)
        self.wallx = 400 #расстояние от одной колонны до другой 
        self.birdY = 350 #первоначальная позиция птицы по высоте
        self.jump = 0 #высота прыжка
        self.jumpSpeed = 10 #скорость падения 
        self.gravity = 5 # скорость падение 
        self.dead = False
        self.sprite = 0 #выбор картинки для птички 
        self.counter = 0 #счетчик сколько колонн прошла
        self.offset = random.randint(-110, 110) #место в котором появится отверстие 
        pygame.mixer.music.load('sounds/music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.fall = pygame.mixer.Sound('sounds/fall.wav')
        self.fall.set_volume(0.1)
        
        pygame.display.set_caption('Flappy bird')
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -100: #момент удаления колонн при выходе за границу
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1 #как быстро птичка опускается по Y
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if not (0 < self.bird[1] < 720): #если птица упала вниз 
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5
    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 80)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                #если нажата клавиша или мышка и при этом птичка жива
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.dead: #обработка смены картинок для птички
                self.sprite = 2 
                    
                self.fall.play()
                
                                
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()
game = FlappyBird()
game.run()