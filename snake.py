import json
import os
import random
import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_1, K_2, K_3, K_4, K_5, K_RETURN

#VISUALS
SCREEN_SIZE = 800
BLOCK_WIDTH = 40

class Snake():
    def __init__(self, parent_screen, length = 5):
        self.length = length # length is currently 5
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg")

        # initiate x and y coordinates
        self.x = [BLOCK_WIDTH] * self.length
        self.y = [BLOCK_WIDTH] * self.length

        # direction
        self.direction = "right"
    
    def draw(self):

        self.parent_screen.fill((0, 0, 0)) # clears screen to add all the elements

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i])) # blit draws one object over another to redraw snake in new position

    def increase(self):
        self.length += 1
        self.x.append(-1) # -1 is placeholder, gets updated when the snake moves
        self.y.append(-1)

# move the snake
    def move_left(self):
        if self.direction != 'right': # can't move the snake 180 degrees
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    # moves the snake to the position directly in front of it
    def move(self):
        
        for i in range(self.length - 1, 0, -1): # assigns position of each block to the space in front of it to show movement
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # top left corner is (0, 0), these if statements move the snake based on current direction
        if self.direction == 'right':
            self.x[0] += BLOCK_WIDTH

        if self.direction == 'left':
            self.x[0] -= BLOCK_WIDTH

        if self.direction == 'up':
            self.y[0] -= BLOCK_WIDTH

        if self.direction == 'down':
            self.y[0] += BLOCK_WIDTH

        # reset snake to opposite side if it crosses borders
        if self.x[0] >= SCREEN_SIZE:
            self.x[0] = 0

        if self.x[0] < 0:
            self.x[0] = SCREEN_SIZE

        if self.y[0] >= SCREEN_SIZE:
            self.y[0] = 0

        if self.y[0] < 0:
            self.y[0] = SCREEN_SIZE

        self.draw()

# Apple instructions
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple_img = pygame.image.load("resources/apple.jpg")
        
        # first apple coordinates are (160, 200)
        self.x = BLOCK_WIDTH * 4
        self.y = BLOCK_WIDTH * 5

    def draw(self):
        self.parent_screen.blit(self.apple_img, (self.x, self.y))
    
    def move(self, snake):
        # Creates and places food on map
        while True:
            x = random.randint(0, 19) * BLOCK_WIDTH # randomly places it on the 20 possiblle locations
            y = random.randint(0, 19) * BLOCK_WIDTH
            
            clean = True

            for i in range(0, snake.length): # checks new apple placement to see if it matches any of the snake's body segments
                if x == snake.x[i] and y == snake.y[i]:
                    clean = False
                    break
            
            if clean:
                self.x = x
                self.y = y
                return

# Base Game info
class Game:
    def __init__(self):
        pygame.init() #initializes required modules in pygame
        pygame.display.set_caption("Snake Game - Pygame")
        self.SCREEN_UPDATE = pygame.USEREVENT # pygame event is used to create a custom user event which can be used to trigger screen updates

        # change how fast the snake goes
        self.timer = 150
        pygame.time.set_timer(self.SCREEN_UPDATE, self.timer)

        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) # sets the x and y vals for screen size

        self.snake = Snake(self.surface, length = 5)
        self.snake.draw()

        self.apple = Apple(parent_screen = self.surface)

        self.score = 0
        self.record = 0

        self.retrieve_data()
    
    def play(self):

        pygame.time.set_timer(self.SCREEN_UPDATE, self.timer)

        self.snake.move()
        self.apple.draw()
        self.display_score()
    
        # check if snake eats apple
        if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
            self.score += 1
            self.snake.increase()
            self.apple.move(self.snake)
            print(str(self.score))
            if self.record < self.score:
                self.record = self.score
                self.save_data()

        # if snake collides with itself
        for i in range (1, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                print("snake died")
                raise Exception("Collision Occurred")

    def save_data(self):
        data_folder_path = "./resources"
        file_name = "data.json"
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        complete_path = os.path.join(data_folder_path, file_name)
        data = {'record': self.record}
        with open(complete_path, 'w') as file:
            json.dump(data, file, indent = 4)
    
    def retrieve_data(self):
        data_folder_path = os.path.join("./resources", "data.json")
        
        if os.path.exists(data_folder_path):
            with open(data_folder_path, 'r') as file:
                data = json.load(file)

            if data is not None:
                self.record = data['record']

    # display scores
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        msg = "Score: " + str(self.score) + " Record: " + str(self.record)
        scores = font.render(f"{msg}", True, (200, 200, 200))
        self.surface.blit(scores, (350, 10))

    # Game Over message
    def show_game_over(self):
        font = pygame.font.SysFont('arial', 30)
        line0 = font.render(f"You died! Your score was {self.score}.", True, (255, 0, 0))
        self.surface.blit(line0, (250, 300))
        line1 = font.render(f"Press enter to try again!", True, (255, 0, 0))
        self.surface.blit(line1, (250, 400))
        pygame.display.update()

    # reset game
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.score = 0

    # run the game
    def run(self):

        running = True
        pause = False

        while running:

            # Handle events in game
            for event in pygame.event.get():
                
                # tracks if a key has been pressed
                if event.type == KEYDOWN:

                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()

                    # Change snake speed
                    if event.key == K_1:
                        self.timer = 50
                    if event.key == K_2:
                        self.timer = 100
                    if event.key == K_3:
                        self.timer = 150
                    if event.key == K_4:
                        self.timer = 300
    
                    if event.key == K_RETURN:
                        pause = False

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.SCREEN_UPDATE:
                    try:
                        if not pause:
                            self.play()
                    except Exception as e:
                        self.show_game_over()
                        pause = True
                        self.reset()
    
            # update display
            pygame.display.update()

game = Game()
game.run()