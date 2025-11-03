from pico2d import *
import game_world
import game_framework
import math

PIXEL_PER_METER = (1.0 / 0.03)
GRAVITY = 9.8

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, throwin_speed = 15, throwin_angle = 45):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.xv = throwin_speed * math.cos(math.radians(throwin_angle))
        self.yv = abs(throwin_speed * math.sin(math.radians(throwin_angle)))


    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.yv -= GRAVITY * game_framework.frame_time

        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        if self.y < 60:
            game_world.remove_object(self)
