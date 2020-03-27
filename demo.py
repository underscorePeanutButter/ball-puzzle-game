import pygame
import sys

class Map:
    def __init__(self, size, ball_delay, layout):
        self.size = size
        self.ball_delay = ball_delay
        self.layout = layout

class Wall:
    def __init__(self):
        self.sprite = sprites["wall"]

class Wedge:
    def __init__(self, direction):
        self.direction = direction

        self.sprite = sprites["wedges"][self.direction]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.sprite = sprites["player"]

        self.balls = []

    def shoot(self):
        self.balls.append(Ball(self.x, self.y, "left"))

class Ball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

        self.sprite = sprites["ball"]

    def update(self):
        if self.direction == "left":
            self.x -= 0.01
        elif self.direction == "right":
            self.x += 0.01
        elif self.direction == "up":
            self.y -= 0.01
        elif self.direction == "down":
            self.y += 0.01

        if self.x < 0 or self.x >= screen_size[0] / 60 or self.y < 0 or self.y >= screen_size[1] / 60:
            player.balls.remove(self)

    def check_collisions(self):
        if round(self.y) < len(test_map.layout) and round(self.y >= 0) and round(self.x) < len(test_map.layout[0]) and round(self.x >= 0):
            focused_map_content = test_map.layout[round(self.y)][round(self.x)]

            if type(focused_map_content) == Wall:
                if self.direction == "right":
                    self.x -= 1
                    self.direction = "left"
                elif self.direction == "left":
                    self.x += 1
                    self.direction = "right"
                elif self.direction == "up":
                    self.y += 1
                    self.direction = "down"
                elif self.direction == "down":
                    self.y -= 1
                    self.direction = "up"

            elif type(focused_map_content) == Wedge:
                if focused_map_content.direction == "bottomleft":
                    if self.direction == "left":
                        self.direction = "up"
                        self.y -= 1
                    elif self.direction == "down":
                        self.direction = "right"
                        self.x += 1
                elif focused_map_content.direction == "topleft":
                    if self.direction == "left":
                        self.direction = "down"
                        self.y += 1
                    elif self.direction == "up":
                        self.direction = "right"
                        self.x += 1

            for ball in player.balls:
                if ball == self:
                    continue

                if round(self.x) == round(ball.x) and round(self.y) == round(ball.y):
                    if self.direction == "left":
                        self.direction = "right"
                        self.x += 1
                        ball.direction = "left"
                        ball.x -= 1
                    elif self.direction == "right":
                        self.direction = "left"
                        self.x -= 1
                        ball.direction = "right"
                        ball.x += 1
                    elif self.direction == "up":
                        self.direction = "down"
                        self.y += 1
                        ball.direction = "up"
                        ball.y -= 1
                    elif self.direction == "down":
                        self.direction = "up"
                        self.y -= 1
                        ball.direction = "down"
                        ball.y += 1

print("Starting pygame... ", end="")

pygame.init()

print("done.")
print("Loading variables... ", end="")

screen_size = (800, 600)

print("done.")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

print("Starting window... ", end="")

screen = pygame.display.set_mode(screen_size)

print("done.")
print("Loading sprites... ", end="")

sprites = {"wedges": {"bottomleft": pygame.image.load("wedge_bottom_left.png"),\
                      "bottomright": pygame.image.load("wedge_bottom_right.png"),\
                      "topleft": pygame.image.load("wedge_top_left.png"),\
                      "topright": pygame.image.load("wedge_top_right.png")},
           "player": pygame.image.load("player.png"),\
           "wall": pygame.image.load("wall.png"),\
           "ball": pygame.image.load("ball.png")}

print("done.")

test_map_layout = [[None, None, None, None, None],
                   [Wall(), Wall(), Wall(), None, Wall()],
                   [Wall(), Wedge("topleft"), None, None, None],
                   [Wall(), None, Wall(), None, Wall()],
                   [Wall(), Wedge("bottomleft"), None, None, None],
                   [Wall(), Wall(), Wall(), None, Wall()],
                   [None, None, Wall(), None, Wall()],
                   [None, None, Wall(), Wall(), Wall()]]
test_map = Map(7, 10, test_map_layout)

player = Player(6, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x += 1
            if event.key == pygame.K_LEFT:
                player.x -= 1
            if event.key == pygame.K_UP:
                player.y -= 1
            if event.key == pygame.K_DOWN:
                player.y += 1
            if event.key == pygame.K_SPACE:
                player.shoot()
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    map_x = 0
    map_y = 0

    for row in test_map.layout:
        for column in row:
            if column:
                screen.blit(column.sprite, (map_x, map_y))

            map_x += 60
        map_y += 60
        map_x = 0

    for ball in player.balls:
        ball.update()
        ball.check_collisions()

        screen.blit(ball.sprite, (round(ball.x) * 60, round(ball.y) * 60))

    screen.blit(player.sprite, (player.x * 60, player.y * 60))

    pygame.display.flip()
