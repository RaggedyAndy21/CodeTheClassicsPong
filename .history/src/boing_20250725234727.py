import pgzero, pgzrun, pygame
import math, sys, random
from enum import Enum
if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Pleadse download"
          "it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s
                  for s in pgzero.__version__.split('.')]

if pgzero_version < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero. You are"
          "using version {pgzero.__version__}. Please upgrade using the command"
          "'pip install --upgrade pgzero'")
    sys.exit
    
WIDTH = 800
HEIGHT = 480
TITLE = "Boing!"

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PLAYER_SPEED = 6
MAX_AI_SPEED = 6

def normalised(x, y):
    length = math.hypot(x, y)
    return (x / length, y / length)

def sign(x):
    return -1 if x < 0 else 1

class Bat(Actor):
    def __init__(self, player, move_func=None):
        x = 40 if player == 0 else 760
        y = HALF_HEIGHT
        super().__init__("blank", (x, y))

        self.player = player
        self.score = 0

        if move_func != None:
            self.move_func = move_func
        else:
            self.move_func = self.ai

        self.timer = 0
        
    def update(self):
        self.timer -= 1
        y_movement = self.move_func()
        self.y = min(400, max(80, self.y + y_movement))

        frame = 0
        if self.timer > 0:
            if game.ball.out():
                frame = 2
            else: frame = 1
        self.image = "bat" + str(self.player) + str(frame)

    def ai(self):
        x_distance = abs(game.ball.x - self.x)
        target_y_1 = HALF_HEIGHT
        target_y_2 = game.ball.y + game.ai_offset
        weigth1 = min(1, x_distance / HALF_WIDTH)
        weight2 = 1 - weigth1
        target_y = (weigth1 * target_y_1) + (weight2 * target_y_2)
        return min(MAX_AI_SPEED, max(-MAX_AI_SPEED, target_y - self.y))

class Impact(actor):
    def __init__(self, pos):
        super().__ini__("blank", pos)
        self.time = 0

    def update(self):
        self.image = "impact" + str(self.time // 2)
        self.time += 1
    
class Ball(Actor):
    def __init__(self, dx):
        super().__init__("ball", (0,0))
        self.x, self.y = HALF_WIDTH, HALF_HEIGHT
        self.dx, self.dy = dx, 0
        self.speed = 5
        
    def update(self):
        for i in range(self.speed):
            original_x = self.x
            self.x += self.dx
            self.y += self.dy
            if abs(self.x - HALF_WIDTH) >= 344 and abs(original_x - HALF_WIDTH) < 344:
                if self.x < HALF_WIDTH:
                    new_dir_x = 1
                    bat = game.bats[0]
                else:
                    new_dir_x = -1
                    bat = game.bats[1]

                    difference_y = self.y - bat.y

                    if difference_y > -64 and difference_y < 64:
                        self.dx = -self.dx
                        self.dy += difference_y / 128
                        self.dy = min(max(self.dy, -1), 1)
                        self.dx, self.dy = normalised(self.dx, self.dy)
                        game.impacts.append(Impact((self.x - new_dir_x * 10, self.y)))
                        





