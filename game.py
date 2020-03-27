import pygame
import sys

class Player:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.old_x = self.x
        self.old_y = self.y

        self.sprite = sprites["player"]

        self.balls = []

    def update(self):
        pass

    def render(self):
        render_x = round(self.x) * grid_space_size
        render_y = round(self.y) * grid_space_size

        screen.blit(self.sprite, (render_x, render_y))

    def shoot(self):
        self.balls.append(Ball(self.x, self.y, -1, 0))

    def handle_new_location(self):
        pass

    def handle_keypresses(self, key):
        # Movement
        if key == pygame.K_RIGHT:
            self.x += 1
        elif key == pygame.K_LEFT:
            self.x -= 1
        elif key == pygame.K_DOWN:
            self.y += 1
        elif key == pygame.K_UP:
            self.y -= 1

        # Actions
        if key == pygame.K_SPACE:
            self.shoot()

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y

        self.speed = 0.01

        self.speed_x = self.speed * speed_x
        self.speed_y = self.speed * speed_y

        self.sprite = sprites["ball"]

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        rounded_x = round(self.x)
        rounded_y = round(self.y)

        if self.old_x != rounded_x:
            self.handle_new_location()

        if self.old_y != rounded_y:
            self.handle_new_location()

        self.old_x = rounded_x
        self.old_y = rounded_y

    def render(self):
        render_x = round(self.x) * grid_space_size
        render_y = round(self.y) * grid_space_size

        screen.blit(self.sprite, (render_x, render_y))

    def handle_new_location(self):
        collision_object = check_collisions(self, (0, 0))

        if type(collision_object) == Wall:
            self.speed_x *= -1
            self.speed_y *= -1

        elif type(collision_object) == Wedge:
            if collision_object.direction == "ul":
                if self.speed_x < 0:
                    self.speed_y = -self.speed_x
                    self.speed_x = 0
                elif self.speed_x > 0:
                    self.speed_x *= -1
                elif self.speed_y < 0:
                    self.speed_x = -self.speed_y
                    self.speed_y = 0
                elif self.speed_y > 0:
                    self.speed_y *= -1

            elif collision_object.direction == "dl":
                if self.speed_x < 0:
                    self.speed_y = self.speed_x
                    self.speed_x = 0
                elif self.speed_x > 0:
                    self.speed_x *= -1
                elif self.speed_y < 0:
                    self.speed_y *= -1
                elif self.speed_y > 0:
                    self.speed_x = self.speed_y
                    self.speed_y = 0

            elif collision_object.direction == "ur":
                if self.speed_x < 0:
                    self.speed_x *= -1
                elif self.speed_x > 0:
                    self.speed_y = self.speed_x
                    self.speed_x = 0
                elif self.speed_y < 0:
                    self.speed_x = self.speed_y
                    self.speed_y = 0
                elif self.speed_y > 0:
                    self.speed_y *= -1

            elif collision_object.direction == "dr":
                if self.speed_x < 0:
                    self.speed_x *= -1
                elif self.speed_x > 0:
                    self.speed_y = - self.speed_x
                    self.speed_x = 0
                elif self.speed_y < 0:
                    self.speed_y *= -1
                elif self.speed_y > 0:
                    self.speed_x = -self.speed_y
                    self.speed_y = 0

            self.x = round(self.x)
            self.y = round(self.y)

            if self.speed_x < 0:
                self.x += 0.4
            elif self.speed_x > 0:
                self.x -= 0.5
            elif self.speed_y < 0:
                self.y += 0.4
            elif self.speed_y > 0:
                self.y -= 0.5

        elif type(collision_object) == Goal:
            load_next_level()

class Wall:
    def __init__(self):
        self.sprite = sprites["wall"]

class Wedge:
    def __init__(self, direction):
        self.direction = direction

        self.sprite = sprites["wedges"][direction]

class Goal:
    def __init__(self):
        self.sprite = sprites["goal"]

def check_collisions(object, offset):
    try:
        check_x = round(object.x) + offset[0]
        check_y = round(object.y) + offset[1]

        return map_data[check_y][check_x]

    except IndexError:
        if type(object) == Ball:
            player.balls.remove(object)

            return None

def load_next_level():
    global player
    global map_data
    global current_level

    if current_level >= len(game_data):
        print("Game Complete")
        sys.exit()

    map_data = game_data[current_level]["map_data"]
    player = Player(game_data[current_level]["start_position"])

    current_level += 1

pygame.init()

screen_size = (600, 600)
screen = pygame.display.set_mode(screen_size)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

grid_space_size = 60

sprites = {"wedges": {"dl": pygame.image.load("wedge_bottom_left.png"),\
                      "dr": pygame.image.load("wedge_bottom_right.png"),\
                      "ul": pygame.image.load("wedge_top_left.png"),\
                      "ur": pygame.image.load("wedge_top_right.png")},
           "player": pygame.image.load("player.png"),\
           "wall": pygame.image.load("wall.png"),\
           "ball": pygame.image.load("ball.png"),\
           "goal": pygame.image.load("goal.png")}

player = Player((0, 0))

game_data = []

current_level = 0
map_data = []

with open("game_data.txt") as file:
    for line in file:
        game_data.append(eval(line))

load_next_level()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            player.handle_keypresses(event.key)

    screen.fill(black)

    player.update()
    player.render()

    for ball in player.balls:
        ball.update()
        ball.render()

    render_x = 0
    render_y = 0
    for row in map_data:
        for object in row:
            if object:
                screen.blit(object.sprite, (render_x, render_y))

            render_x += grid_space_size

        render_x = 0
        render_y += grid_space_size

    pygame.display.flip()
