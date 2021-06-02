import time
import pygame
import sys
import random

from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        self.health = 3

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class PROJECTILE:
    def __init__(self):
        projectile_state = False
        self.snake = SNAKE()
        self.direction = self.snake.direction
        self.projectile_up = pygame.image.load('Graphics/projectile_up.png').convert_alpha()
        self.projectile_down = pygame.image.load('Graphics/projectile_down.png').convert_alpha()
        self.projectile_right = pygame.image.load('Graphics/projectile_right.png').convert_alpha()
        self.projectile_left = pygame.image.load('Graphics/projectile_left.png').convert_alpha()


    def draw_projectile(self):
        self.update()
        x_pos = self.snake.body[0].x
        y_pos = self.snake.body[0].y
        projectile_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        screen.blit(self.head, projectile_rect)


    def update(self):
        head_relation = self.snake.body[1] - self.snake.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.projectile_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.projectile_right
        elif head_relation == Vector2(0, 1):
            self.head = self.projectile_up
        elif head_relation == Vector2(0, -1):
            self.head = self.projectile_up

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class ENEMY:

    def __init__(self):
        self.randomize()


    def draw_enemy(self):
        enemy_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple_2, enemy_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.changeX = 0
        self.changeY = cell_size
        self.movement = Vector2(self.changeX, self.changeY)



    def move_enemy(self):
        self.pos += self.movement
        if self.pos.x >= (cell_number * cell_size):
            self.changeX = -40
            self.pos.y += self.changeY

        elif self.pos.x <= 0:
            self.changeX = 40
            self.pos.y += self.changeY



class MAIN:

    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.enemy = ENEMY()
        self.projectile = PROJECTILE()

    def update(self):
        self.snake.move_snake()
       # self.enemy.move_enemy()
        self.check_collision()
        self.check_fail()
        self.projectile.draw_projectile()


    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.enemy.draw_enemy()
        self.draw_lives()
        self.draw_highscore()
        #self.projectile.draw_projectile()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            if len(self.snake.body) % 4 == 0:
                self.enemy.randomize()

        if self.enemy.pos == self.snake.body[0]:
            if self.snake.health != 1:
                self.enemy.randomize()
                self.snake.health -= 1
            else:
                self.snake.reset()
                self.enemy.randomize()
                self.snake.health += 2

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

            if block == self.enemy.pos:
                self.enemy.randomize()

            if self.enemy.pos == self.fruit.pos:
                self.fruit.randomize()
                self.enemy.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()







    def game_over(self):

        self.snake.reset()
        self.snake.health = 3


    def draw_grass(self):
        grass_color = (65, 65, 67)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (200, 200, 200))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)


    def draw_lives(self):
        score_text = str(f"Lives - {self.snake.health}")
        score_surface = game_font.render(score_text, True, (200, 40, 40))
        score_x = int(cell_size * cell_number - 750)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

    def draw_highscore(self):
        with open("highscore.txt.", "r") as f:
            hiscore = f.read()

        score1 = len(self.snake.body) - 3
        if score1 >= int(hiscore):
            hiscore = score1
        score_text = str(f"Highscore - {hiscore}")
        score_surface = game_font.render(score_text, True, (100, 100, 100))
        score_x = int(cell_size * cell_number - 550)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)
        with open("highscore.txt.", "w") as f:
            f.write(str(hiscore))


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("Snake Adventures")
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
apple_2 = pygame.image.load('Graphics/apple_2.png').convert_alpha()
projectile = pygame.image.load('Graphics/Projectile_left.png')
Game_menu = pygame.image.load('Graphics/Game_menu.jpg').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)



main_game = MAIN()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            while True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == SCREEN_UPDATE:
                        main_game.update()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if main_game.snake.direction.y != 1:
                                main_game.snake.direction = Vector2(0, -1)
                        if event.key == pygame.K_RIGHT:
                            if main_game.snake.direction.x != -1:
                                main_game.snake.direction = Vector2(1, 0)
                        if event.key == pygame.K_DOWN:
                            if main_game.snake.direction.y != -1:
                                main_game.snake.direction = Vector2(0, 1)
                        if event.key == pygame.K_LEFT:
                            if main_game.snake.direction.x != 1:
                                main_game.snake.direction = Vector2(-1, 0)
                        if event.key == pygame.K_SPACE:
                            main_game.projectile_state = True


                screen.fill((70, 70, 70))
                main_game.draw_elements()
                pygame.display.update()
                clock.tick(60)

        else:
            screen.blit(Game_menu, (0, 0))
            pygame.display.update()
            clock.tick(60)
