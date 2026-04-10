import pygame
import random
from base import Base
from shapes import Ball, Square
from projectiles import Bomb
from sprites import sprites

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 89, 255)
red = (245, 0, 0)
green = (9, 255, 0)
purple = (106, 0, 255)
gray = (128, 128, 128)
yellow = (255, 208, 0)
orange = (255, 102, 0)

pygame.font.init()
font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 20)

class Game:
    def __init__(self):
        self.money = 750
        self.money_timer = 0
        self.balls = []
        self.squares = []
        self.bombs = []
        self.projectiles = []

        self.player_base = Base(10, 50, gray, True)
        self.enemy_base = Base(760, 50, gray, False)
        
        self.selected_ball = 0
        self.enemy_spawn_timer = 0
        self.game_over = False
        self.victory = False
        
        # five zeroes for each ball type
        self.spawn_cooldown = [0, 0, 0, 0, 0]

        self.current_wave = 1
        self.wave_timer = 0
        self.enemies_spawned_this_wave = 0
        self.max_enemies_per_wave = 10

        self.ball_types = [
            {'cost': 50, 'damage': 10, 'hp': 30, 'speed': 0.5, 'color': blue, 'size': 15, 'range': 80, 'type': 'regular', 'sprite': 'ball'}, # regular ball
            {'cost': 80, 'damage': 17, 'hp': 80, 'speed': 0.4, 'color': green, 'size': 19, 'range': 80, 'type': 'tank', "sprite": 'tank_ball'}, # tank ball
            {'cost': 60, 'damage': 15, 'hp': 20, 'speed': 0.35, 'color': purple, 'size': 14, 'range': 150, 'type': 'ranged', 'sprite': 'ranged_ball'}, # ranged ball
            {'cost': 120, 'damage': 20, 'hp': 25, 'speed': 0.35, 'color': yellow, 'size': 14, 'range': 50, 'type': 'air', 'sprite': 'flying_ball'}, # flying ball
            {'cost': 275, 'damage': 45, 'hp': 140, 'speed': 0.45, 'color': orange, 'size': 25, 'range': 100, 'type': 'super', 'sprite': 'superball'}
        ] 
        
        self.square_types = [
            {'hp': 40, 'damage': 8, 'speed': 0.5, 'bounty': 30, 'color': blue, 'size': 15, 'range': 80, 'type': 'regular', 'sprite': 'square'},
            {'hp': 90, 'damage': 16, 'speed': 0.4, 'bounty': 40,  'color': green, 'size': 19, 'range': 80, 'type': 'tank', 'sprite': 'tank_square'},
            {'hp': 20, 'damage': 15, 'speed': 0.35, 'bounty': 35, 'color': purple, 'size': 14, 'range': 150, 'type': 'ranged', 'sprite': 'ranged_square'},
            {'hp': 30, 'damage': 21, 'speed': 0.32, 'bounty': 50, 'color': yellow, 'size': 15, 'range': 50, 'type': 'air', 'sprite': 'flying_square'},
            {'hp': 155, 'damage': 40, 'speed': 0.45, 'bounty': 150, 'color': orange, 'size': 25, 'range': 100, 'type': 'super', 'sprite': 'super_square'}
        ]

    def spawn_ball(self, ball_index): # spawns ball when player presses a key
        if self.spawn_cooldown[ball_index] > 0: # checks if cooldown is still active
            return
        ball_type = self.ball_types[ball_index]
        if self.money >= ball_type['cost']:
            self.money -= ball_type['cost']
        else:
            return
    

        # making it so air units actually fly (higher y pos)
        if ball_type['type'] == 'air':
            y_pos = 150
        else:
            y_pos = 200 # 200 is ground height

        sprite = sprites.get(ball_type['sprite'])
        new_ball = Ball(50, y_pos, ball_type, sprite)
        self.balls.append(new_ball)
        self.spawn_cooldown[ball_index] = 60
        

    
    def spawn_enemy(self):
        # spawns enemies randomly throughout each wave
        # stops spawning max limit for each wave is reached
        if self.current_wave <= 5 and self.enemies_spawned_this_wave < self.max_enemies_per_wave:
            square_type = random.choice(self.square_types)
    

        # making it so air units actually fly (higher y pos)
            if square_type['type'] == 'air':
                y_pos = 150
            else:
                y_pos = 200 # 200 is ground height

            sprite = sprites.get(square_type['sprite'])
            new_square = Square(750, y_pos, square_type, sprite)
            self.squares.append(new_square)
            self.enemies_spawned_this_wave += 1

    def update(self):
        if self.game_over:
            return
        
        # counting down all the spawn cooldowns
        for i in range(len(self.spawn_cooldown)):
            if self.spawn_cooldown[i] > 0:
                self.spawn_cooldown[i] -= 1

        # makes it so you can passively earn money
        self.money_timer += 1
        if self.money_timer >= 10:
            self.money +=1
            self.money_timer = 0

        # wave management, each wave lasts 30 seconds (1800 frames at 60fps)
        self.wave_timer += 1
        if self.wave_timer > 1800:
            if self.current_wave < 5:
                # starting next wave
                self.current_wave += 1
                self.enemies_spawned_this_wave = 0
                self.max_enemies_per_wave += 5
                self.wave_timer = 0

                for square_type in self.square_types:
                    # increasing stats of enemy units each wave (progression difficulty)
                    square_type['hp'] = int(square_type['hp'] * 1.2)
                    square_type['damage'] = int(square_type['damage'] * 1.2)
                    square_type['bounty'] = int(square_type['bounty'] * 1.2)
                
                # making enemies spawn faster each wave
                spawn_delay = max(60, 180 - (self.current_wave * 20))  # gets faster each wave
                if self.enemy_spawn_timer > random.randint(spawn_delay // 2, spawn_delay):
                    self.spawn_enemy()
                    self.enemy_spawn_timer = 0
            
            else:
                # if all 5 waves are done and no enemies left, player wins
                if len(self.squares) == 0:
                    self.game_over = True
                    self.victory = True
        
        # spawning enemies at random intervals
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer > random.randint(100, 180):
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        
        # updating all the balls
        for ball in self.balls:
            ball.update(self.squares, self.enemy_base, self.projectiles)
        
        # updating all the squares
        for square in self.squares:
            square.update(self.balls, self.player_base, self.projectiles)
        
        # updating projectiles and removing ones that hit
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.hit:
                self.projectiles.remove(projectile)

        # updating bombs and applying dmg when they explode
        for bomb in self.bombs[:]:
            bomb.update()
            if not bomb.expanding:
                # checking what bomb hits based on if enemy/player dropped it
                if bomb.is_player:
                    # player bombs damage squares
                    for square in self.squares[:]:
                        distance = ((bomb.x - square.x)**2 + (bomb.y - square.y)**2)**0.5
                        if distance < bomb.max_radius:
                            square.hp -= bomb.damage
                    # and enemy base
                    if ((bomb.x - self.enemy_base.x)**2 + (bomb.y - self.enemy_base.y)**2)**0.5 < bomb.max_radius:
                        self.enemy_base.take_damage(bomb.damage)

                else:
                    # enemy bombs damage balls
                    for ball in self.balls[:]:
                        distance = ((bomb.x - ball.x)**2 + (bomb.y - self.player_base.y)**2)**0.5
                        if distance < bomb.max_radius:
                            ball.hp -= bomb.damage
                    # and player base
                    if ((bomb.x - self.player_base.x)**2 + (bomb.y - self.player_base.y)**2)**0.5 < bomb.max_radius:
                        self.player_base.take_damage(bomb.damage)
                self.bombs.remove(bomb)

        # checks for dead balls and removes them
        for ball in self.balls[:]:
            if ball.hp <= 0:
                # air units drop bombs when they die
                if ball.type == 'air':
                    bomb = Bomb(ball.x, ball.y, True, sprites.get('bomb'), sprites.get('explosion'))
                    self.bombs.append(bomb)
                self.balls.remove(ball)
            elif ball.x > 780:
                # balls that reach the end damage the enemy base
                self.enemy_base.take_damage(ball.damage)
                self.balls.remove(ball)

        # checks for dead squares
        for square in self.squares[:]:
            if square.hp <= 0:
                # air units drop bombs
                if square.type == 'air':
                    bomb = Bomb(square.x, square.y, 15, False, sprites.get('bomb'), sprites.get('explosion'))
                    self.bombs.append(bomb)
                # gives player money for killing squares
                self.money += square.bounty
                self.squares.remove(square)
            elif square.x < 0:
                # squares that reach player base damage it
                self.player_base.take_damage(square.damage)
                self.squares.remove(square)

        # win/lose conditions
        if self.player_base.hp <= 0:
            self.game_over = True
        if self.enemy_base.hp <= 0:
            self.game_over = True
            self.victory = True
        
    def draw(self, surface):
        surface.fill(white)
        self.player_base.draw(surface)
        self.enemy_base.draw(surface)
        # ground line
        pygame.draw.line(surface, black, (0, 200), (800, 200), 2)

        for ball in self.balls:
            ball.draw(surface)

        for square in self.squares:
            square.draw(surface)

        for projectile in self.projectiles:
            projectile.draw(surface)

        for bomb in self.bombs:
            bomb.draw(surface)

        # all the ui stuff
        money_text = font.render("Money: $" + str(self.money), True, black)
        surface.blit(money_text, (280, 10))

        wave_text = font.render("Wave: " + str(self.current_wave) + "/5", True, black)
        surface.blit(wave_text, (450, 10))

        # shows the keys needed to summon units
        y_start = 360
        keys = ['1', '2', '3', '4', '5']
        for i, ball_type in enumerate(self.ball_types):
            # positioning keys in rows
            y_pos = y_start + (i // 3) * 30
            x_pos = 60 + (i % 3) * 140

            # shows unit icon
            icon_sprite = sprites.get(ball_type['sprite'])
            if icon_sprite:
                icon = pygame.transform.scale(icon_sprite, (20, 20))
                # makes icon transparent when on cooldown
                if self.spawn_cooldown[i] > 0:
                    icon.set_alpha(100)
                else:
                    icon.set_alpha(255)
                icon_rect = icon.get_rect(center=(x_pos, y_pos))
                surface.blit(icon, icon_rect)
            else:
                # fallback to colored circle if spriteload fails
                if self.spawn_cooldown[i] > 0:
                    color = gray
                else:
                    color = ball_type['color']
                pygame.draw.circle(surface, color, (x_pos, y_pos), 10)
            
            # shows cost and keybind to spawn each unit
            cost_text = small_font.render(keys[i] + ": $" + str(ball_type['cost']), True, black)
            surface.blit(cost_text, (x_pos + 15, y_pos - 8))

            # shows cd timer if active
            if self.spawn_cooldown[i] > 0:
                cd_text = small_font.render(str(self.spawn_cooldown[i] // 60 + 1) + "s", True, red)
                surface.blit(cd_text, (x_pos + 100, y_pos - 8))
            
            # draws game over screen 
        if self.game_over:
            # darkens screen for game over 
            overlay = pygame.Surface((800, 400))
            overlay.set_alpha(200)
            overlay.fill(black)
            surface.blit(overlay, (0, 0))

            if self.victory:
                end_text = font.render("GAME OVER! - WIN", True, green)
            else:
                end_text = font.render("GAME OVER! - LOSE", True, red)

            text_rect = end_text.get_rect(center=(400, 200))
            surface.blit(end_text, text_rect)



                            
                        





        
            

