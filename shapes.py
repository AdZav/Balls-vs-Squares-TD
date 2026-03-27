import pygame

red = (245, 0, 0)
green = (9, 255, 0)

class Ball:
    #setup for Balls
    def __init__(self, x, y, type, sprite):
        self.x = x
        self.y = y
        self.damage = type['damage']
        self.hp = type['hp']
        self.maxhp = type['hp']
        self.speed = type['speed']
        self.size = type['size']
        self.cooldown = 0
        self.color = type['color']
        self.target = None
        self.range = type['range']
        self.type = type['type']
        self.sprite = sprite

        # scaling to optimal size
        if self.sprite:
            self.sprite = pygame.transform.scale(self.sprite, (self.size * 2, self.size * 2))
    
    def update(self, enemies, enemy_base, projectiles):
        # counting down cooldown per frame
        self.cooldown -= 1

    # making sure air units only attack bases
        if self.type == 'air':
            if abs(self.x - enemy_base.x) < 50:
                self.target = enemy_base
            else:
                self.target = None
        else:
            # if target dies or goes out of range it finds a new one
            if self.target is None or self.target not in enemies:
                self.target = None
            for enemy in enemies:
                if enemy.type == 'air' and self.type != 'ranged':
                    continue
                if abs(self.x - enemy.x) < self.range:
                    self.target = enemy
                    break
        
        # if there's nothing to attack it keeps moving forward
        if self.target is None:
            self.x += self.speed
        else:
            # ranged units shoot projectiles instead of just dealing instant damage
            if self.cooldown <= 0:
                if self.type == 'ranged':
                    from projectiles import Projectile
                    from sprites import sprites
                    proj = Projectile(self.x, self.y, self.target, self.damage, True, sprites.get('arrow_projectile'))
                    projectiles.append(proj)
                else:
                    # non-ranged units just deal damage
                    self.target.hp -= self.damage
                self.cooldown = 60
    
    def draw(self, surface):
        if self.sprite:
            rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.sprite, rect)
        else:
            # circle fallback if sprite doesnt load
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

        health_bar = self.hp / self.maxhp
        # red = total hp, green = current hp
        pygame.draw.rect(surface, red, (self.x - 15, self.y - 25, 30, 4))
        pygame.draw.rect(surface, green, (self.x - 15, self.y - 25, int(30 * health_bar), 4))

class Square: # squares are the enemy in this game
    def __init__(self, x, y, type, sprite):
        # square setup is mostly identical
        self.x = x
        self.y = y
        self.hp = type['hp']
        self.maxhp = type['hp']
        self.damage = type['damage']
        self.speed = type['speed']
        self.bounty = type['bounty'] # bounty = how much money you get for defeating a given square, some units have higher bounty
        self.color = type['color']
        self.size = type['size']
        self.cooldown = 0
        self.target = None
        self.range = type['range']
        self.type = type['type']
        self.sprite = sprite

        if self.sprite:
            self.sprite = pygame.transform.scale(self.sprite, (self.size * 2, self.size * 2))

    def update(self, enemies, player_base, projectiles):
        self.cooldown -= 1

        if self.type == 'air':
            if abs(self.x - player_base.x) < 50:
                self.target = player_base
            else:
                self.target = None

        else:
            if self.target is None or self.target not in enemies:
                self.target = None
                for enemy in enemies:
                    if enemy.type == 'air' and self.type != 'ranged':
                        continue
                    if abs(self.x - enemy.x) < self.range:
                        self.target = enemy
                        break
        
        if self.target is None:
            self.x -= self.speed # self.x -= self.speed bc enemies move left, player units move right
        else:
            if self.cooldown <= 0:
                if self.type == 'ranged':
                    from projectiles import Projectile
                    from sprites import sprites
                    proj = Projectile(self.x, self.y, self.target, self.damage, False, sprites.get('arrow_projectile'))
                    projectiles.append(proj)
                else:
                    self.target.hp -= self.damage
                self.cooldown = 60
    
    def draw(self, surface):
        if self.sprite:
            rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.sprite, rect)
        else:
            pygame.draw.rect(surface, self.color, (self.x - self.size//2, self.y - self.size//2, self.size, self.size))       

        health_bar = self.hp / self.maxhp
        pygame.draw.rect(surface, red, (self.x - 15, self.y - 35, 30, 4))     
        pygame.draw.rect(surface, green, (self.x - 15, self.y - 35, int(30 * health_bar), 4))
