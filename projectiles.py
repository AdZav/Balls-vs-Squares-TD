import pygame
import math

class Projectile:
    def __init__(self, x, y, target, damage, is_player, sprite=None):
        # setup
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 5
        self.is_player = is_player
        self.hit = False
        self.sprite = sprite
        self.angle = 0
        
        if self.sprite:
            self.sprite = pygame.transform.scale(self.sprite, (20, 20))
    
    def update(self):
        # if it already hit something or lost its target just stop
        if self.target is None or self.hit:
            return
        
        # calculating the direction to move towards the target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        # rotate arrow
        self.angle = math.atan2(dy, dx)
        
        # hits if close enough
        if distance < 10:
            self.target.hp -= self.damage
            self.hit = True
        else:
            # otherwise keep moving towards the target
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def draw(self, surface):
        # only draw if it hasnt hit yet
        if not self.hit:
            if self.sprite:
                # rotating the arrow to point at the target
                rotated = pygame.transform.rotate(self.sprite, -math.degrees(self.angle))
                # flipping it if its an enemy projectile so it points the right way
                if not self.is_player:
                    rotated = pygame.transform.flip(rotated, True, False)
                rect = rotated.get_rect(center=(int(self.x), int(self.y)))
                surface.blit(rotated, rect)
            else:
                # fallback to just drawing a colored circle
                color = (100, 100, 255) if self.is_player else (255, 100, 100)
                pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 5)

class Bomb:
    def __init__(self, x, y, damage, is_player, bomb_sprite=None, explosion_sprite=None):
        # bomb setup, will expand outward when dropped and deal damage in a radius
        self.x = x
        self.y = y
        self.damage = damage
        self.radius = 5
        self.max_radius = 60
        self.expanding = True
        self.is_player = is_player
        self.bomb_sprite = bomb_sprite
        self.explosion_sprite = explosion_sprite
        self.timer = 0
        self.falling = True
        self.fall_speed = 3
        
        # scaling the sprites to the right size
        if self.bomb_sprite:
            self.bomb_sprite = pygame.transform.scale(self.bomb_sprite, (30, 30))
        if self.explosion_sprite:
            self.explosion_sprite = pygame.transform.scale(self.explosion_sprite, (self.max_radius * 2, self.max_radius * 2))
    
    def update(self):
        # make bomb fall before exploding
        if self.falling:
            self.y += self.fall_speed
            if self.y >= 200:
                self.y = 200
                self.falling = False

        # expanding the explosion radius every frame
        if not self.falling and self.expanding:
            self.timer += 1
            self.radius += 5
            if self.radius >= self.max_radius:
                self.expanding = False
    
    def draw(self, surface):
        # showing the bomb sprite first, then switch to explosion
        if self.falling and self.bomb_sprite:
            rect = self.bomb_sprite.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.bomb_sprite, rect)
        elif not self.falling and self.explosion_sprite:
            # scaling the explosion based on how big the radius is
            scale = self.radius / self.max_radius
            scaled_explosion = pygame.transform.scale(self.explosion_sprite, 
                                                     (int(self.max_radius * 2 * scale), 
                                                      int(self.max_radius * 2 * scale)))
            rect = scaled_explosion.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(scaled_explosion, rect)
        else:
            # fallback to drawing a circle that expands
            color = (100, 100, 255) if self.is_player else (255, 100, 100)
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius, 2)