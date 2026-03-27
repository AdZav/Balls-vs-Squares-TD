import pygame
import os

sprites = {}

def load_sprites():

    image_folder = "A:/TDSprites"
    sprite_files = {
        'ball': 'ball.png',
        'tank_ball': 'tank_ball.png',
        'ranged_ball': 'ranged_ball.png',
        'flying_ball': 'flying_ball.png',
        'superball': 'superball.png',
        'square': 'square.png',
        'tank_square': 'tank_square.png',
        'ranged_square': 'ranged_square.png',
        'flying_square': 'flying_square.png',
        'super_square': 'super_square.png',
        'arrow_projectile': 'arrow_projectile.png',
        'bomb': 'bomb.png',
        'explosion': 'explosion_afterbomb.png'
    }
    
    for name, filename in sprite_files.items():
        try:
            path = os.path.join(image_folder, filename)
            img = pygame.image.load(path)
            sprites[name] = img
        except:
            print(f"Could not load {filename} from {image_folder}")

    return sprites
