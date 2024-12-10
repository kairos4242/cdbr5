import pygame
from fighter import Fighter

pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Brawler")

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
scaled_bg = pygame.transform.scale(bg_image, SCREEN_SIZE)

# function for drawing background
def draw_bg():
    
    screen.blit(scaled_bg, (0,0))

# create two instances of fighters
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# game loop
run_game = True
while run_game:

    clock.tick(FPS)

    #draw bg
    draw_bg()

    #move fighters
    fighter_1.move()
    #fighter_2.move()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

    #update display
    pygame.display.update()

# exit pygame
pygame.quit()