from PIL import Image
import pygame
import sys
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            pos_x = block.x * cell_size
            pos_y = block.y * cell_size
            block_rect = pygame.Rect(int(pos_x), int(pos_y), cell_size, cell_size)
            pygame.draw.rect(screen, (170, 70, 170), block_rect)
        block_rect = pygame.Rect(int(self.body[0].x * cell_size), int(self.body[0].y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (150, 30, 30), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.pos = Vector2(random.randint(0, cell_num - 1), random.randint(0, cell_num - 1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)  # place apple on the screen

    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_num - 1), random.randint(0, cell_num - 1))


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game = True
        self.score = 0

    # every screen update, update the snake status and check for collisions
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.display_score()

    # single call to draw all game elements
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.display_score()
        if not self.game:
            self.game_over()

    # draw the grid on which the game is played on
    def draw_scene(self):
        screen.fill((170, 220, 70))
        for i in range(0, cell_num):  # draw grid
            if i % 2 == 0:
                alt = 0
            else:
                alt = 1
            for j in range(alt, cell_num, 2):
                grid = pygame.Rect(i * cell_size, j * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, (150, 200, 100), grid)

    # check for collision with the fruit
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()  # increase snake length
            self.fruit.randomize()  # generate new fruit
            self.score += 1         # update score

    # used to check if the snake head hit a wall or the body
    def check_fail(self):
        # check wall
        if self.snake.body[0].y < 0 or self.snake.body[0].x < 0 or \
         self.snake.body[0].y >= cell_num or self.snake.body[0].x >= cell_num:
            self.game_over()
        # check body
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    # displays the score for the game
    def display_score(self):
        self.display_message(28, "score: " + str(main_game.score), cell_size * cell_num // 2, 20)

    # set game mode to False and print message to the screen
    def game_over(self):
        self.game = False
        self.display_message(72, 'Game Over', cell_size * cell_num // 2, (cell_size * cell_num // 2) - 23)
        self.display_message(32, 'press space to restart the game', cell_size * cell_num // 2, (cell_size * cell_num // 2) + 30)

    # used to display a single message with a given size and location
    def display_message(self, size, msg, x, y):
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(msg, True, "Black", )
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)


# start the game
pygame.init()
cell_size = 40  # default size of cells in the game
cell_num = 20   # default number of cells in the game
screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num))
clock = pygame.time.Clock()

# used to resize any image to the desired size of a cell
test = Image.open("graphic/apple.png")
test = test.resize((cell_size, cell_size), Image.ANTIALIAS)
test.save("graphic/apple2.png")
# loads new apple after resizing
apple = pygame.image.load("graphic/apple2.png").convert_alpha()
snake_icon = pygame.image.load("graphic/snake_icon.png").convert_alpha()
pygame.display.set_caption("My Snake Game")  # rename window
pygame.display.set_icon(snake_icon)  # set icon for the game

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # move snake every 150ms

main_game = MAIN()
while True:
    # handle user events
    for event in pygame.event.get():  # get event from the user
        if event.type == pygame.QUIT:  # if the user decided to close the window
            pygame.quit()
            sys.exit()  # ends any type of code that is run on
        if event.type == SCREEN_UPDATE and main_game.game:
            main_game.update()
        if event.type == pygame.KEYDOWN:  # when a key is pressed
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1):
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(1, 0):
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0)
            if (not main_game.game) and event.key == pygame.K_SPACE:
                main_game = MAIN()

    # draw board and elements
    main_game.draw_scene()
    main_game.draw_elements()
    pygame.display.update()  # update the scene
    clock.tick(60)  # set frame rate
