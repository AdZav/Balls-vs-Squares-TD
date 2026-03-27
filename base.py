import pygame

green = (100, 255, 100)
red = (255, 100, 100)

class Base:
    def __init__(self, x, y, color, is_player):
        # setup
        self.x = x
        self.y = y
        self.hp = 100
        self.max_hp = 100
        self.color = color
        self.is_player = is_player # "is_player" determines what side (player/enemy) the base belongs to, true for player, false for enemy
    
    def take_damage(self, damage):
        # reduces health when something hits the base
        self.hp -= damage
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, 30, 300))
        
        # healthbar, fills up from bottom to top based on health percentage
        health_height = int((self.hp / self.max_hp) * 300)
        bright_color = (0, 200, 0) if self.is_player else (200, 0, 0)
        pygame.draw.rect(surface, bright_color, (self.x, self.y + 300 - health_height, 30, health_height))