import pygame

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def move(self):
        self.movespeed = 10
        self.dx = 0
        self.dy = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # movement
        if key[pygame.K_a]:
            self.dx = -self.movespeed
        if key[pygame.K_d]:
            self.dx = self.movespeed

        # ensure stays on screen
        

        # update player position
        self.rect.x += self.dx
        self.rect.y += self.dy