import pygame
import sys
from game import Game
from sprites import load_sprites

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Balls vs. Squares")
clock = pygame.time.Clock()

load_sprites()

game = Game()

running = True
while running:
    # handles events like closing window/key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game.game_over:
            # 5 keybinds cuz theres five playable units
            if event.key == pygame.K_1:
                game.spawn_ball(0)
            if event.key == pygame.K_2:
                game.spawn_ball(1)
            if event.key == pygame.K_3:
                game.spawn_ball(2)
            if event.key == pygame.K_4:
                game.spawn_ball(3)
            if event.key == pygame.K_5:
                game.spawn_ball(4)
    
    #updating and drawing everything
    game.update()
    game.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()