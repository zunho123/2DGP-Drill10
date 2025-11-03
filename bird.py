from pico2d import load_image
import game_framework
from state_machine import StateMachine
import random

def at_edge(e):
    return e[0] == 'EDGE'

PIXEL_PER_METER = 10.0 / 0.3
FLY_SPEED_KMPH = 40.0

class Bird:
    image = None
    FRAME_COLS = 5
    FRAME_ROWS = 3
    LEFT, RIGHT = 20, 1580
    TOP_Y = 540
    REND_W = 33
    REND_H = 25

    def __init__(self, x=None, y=None, speed_kmph=None, flap_hz=None):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x = self.LEFT if x is None else x
        self.y = self.TOP_Y if y is None else y
        self.dir = 1
        self.frame = 0.0
        self.w = Bird.image.w // self.FRAME_COLS
        self.h = Bird.image.h // self.FRAME_ROWS
        self.FRAMES_PER_ACTION = 14
        if speed_kmph is None:
            speed_kmph = random.uniform(FLY_SPEED_KMPH - 5.0, FLY_SPEED_KMPH + 5.0)
        self.speed_pps = (speed_kmph / 3.6) * PIXEL_PER_METER
        if flap_hz is None:
            flap_hz = random.uniform(13.0, 15.0)
        self.flap_hz = flap_hz
        self.FLY_RIGHT = FlyRight(self)
        self.FLY_LEFT  = FlyLeft(self)
        self.state_machine = StateMachine(
            self.FLY_RIGHT,
            {
                self.FLY_RIGHT: { at_edge: self.FLY_LEFT },
                self.FLY_LEFT:  { at_edge: self.FLY_RIGHT },
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_state_event(self, event):
        self.state_machine.handle_state_event(event)

    def draw(self):
        self.state_machine.draw()

class FlyRight:
    def __init__(self, bird): self.b = bird
    def enter(self, e): self.b.dir = 1
    def exit(self, e):  pass
    def do(self):
        dt = game_framework.frame_time
        self.b.x += self.b.speed_pps * dt
        if self.b.x >= self.b.RIGHT:
            self.b.x = self.b.RIGHT
            self.b.handle_state_event(('EDGE', None))
        self.b.frame = (self.b.frame + self.b.FRAMES_PER_ACTION * self.b.flap_hz * dt) % self.b.FRAMES_PER_ACTION
    def draw(self):
        idx = int(self.b.frame) % self.b.FRAMES_PER_ACTION
        col = idx % self.b.FRAME_COLS
        row = idx // self.b.FRAME_COLS
        sy_row = (self.b.FRAME_ROWS - 1 - row)
        sx, sy = col * self.b.w, sy_row * self.b.h
        Bird.image.clip_draw(sx, sy, self.b.w, self.b.h, self.b.x, self.b.y, self.b.REND_W, self.b.REND_H)

class FlyLeft:
    def __init__(self, bird): self.b = bird
    def enter(self, e): self.b.dir = -1
    def exit(self, e):  pass
    def do(self):
        dt = game_framework.frame_time
        self.b.x -= self.b.speed_pps * dt
        if self.b.x <= self.b.LEFT:
            self.b.x = self.b.LEFT
            self.b.handle_state_event(('EDGE', None))
        self.b.frame = (self.b.frame + self.b.FRAMES_PER_ACTION * self.b.flap_hz * dt) % self.b.FRAMES_PER_ACTION
    def draw(self):
        idx = int(self.b.frame) % self.b.FRAMES_PER_ACTION
        col = idx % self.b.FRAME_COLS
        row = idx // self.b.FRAME_COLS
        sy_row = (self.b.FRAME_ROWS - 1 - row)
        sx, sy = col * self.b.w, sy_row * self.b.h
        try:
            Bird.image.clip_composite_draw(sx, sy, self.b.w, self.b.h, 0, 'h', self.b.x, self.b.y, self.b.REND_W, self.b.REND_H)
        except:
            Bird.image.clip_draw(sx, sy, self.b.w, self.b.h, self.b.x, self.b.y, self.b.REND_W, self.b.REND_H)
