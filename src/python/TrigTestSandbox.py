import pygame

pygame.init()


# create game window
game_screen = pygame.display.set_mode((1920, 1080), flags=pygame.SCALED | pygame.FULLSCREEN, vsync=1)
# set frame rate
pygame_clock = pygame.time.Clock()
FPS = 60