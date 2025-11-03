from pico2d import load_image
import game_framework
from state_machine import StateMachine

def at_edge(e):
    return e[0] == 'EDGE'

PIXEL_PER_METER = (10.0 / 0.3)
FLY_SPEED_KMPH = 20.0
FLY_SPEED_MPM  = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS  = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS  = (FLY_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Bird:
    image = None
    FRAME_COLS = 5
    FRAME_ROWS = 3
    LEFT, RIGHT = 50, 1550
    TOP_Y = 540

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = self.LEFT, self.TOP_Y
        self.dir = 1
        self.frame = 0.0
        self.w = Bird.image.w // self.FRAME_COLS
        self.h = Bird.image.h // self.FRAME_ROWS
        self.TOTAL_FRAMES = self.FRAME_COLS * self.FRAME_ROWS
        self.FRAMES_PER_ACTION = self.TOTAL_FRAMES
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
        self.b.x += FLY_SPEED_PPS * dt
        if self.b.x >= self.b.RIGHT:
            self.b.x = self.b.RIGHT
            self.b.handle_state_event(('EDGE', None))
        self.b.frame = (self.b.frame + self.b.FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % self.b.FRAMES_PER_ACTION

    def draw(self):
        idx = int(self.b.frame)
        col = idx % self.b.FRAME_COLS
        row = idx // self.b.FRAME_COLS
        sy_row = (self.b.FRAME_ROWS - 1 - row)
        sx, sy = col * self.b.w, sy_row * self.b.h
        Bird.image.clip_draw(sx, sy, self.b.w, self.b.h, self.b.x, self.b.y)

class FlyLeft:
    def __init__(self, bird): self.b = bird
    def enter(self, e): self.b.dir = -1
    def exit(self, e):  pass

    def do(self):
        dt = game_framework.frame_time
        self.b.x -= FLY_SPEED_PPS * dt
        if self.b.x <= self.b.LEFT:
            self.b.x = self.b.LEFT
            self.b.handle_state_event(('EDGE', None))
        self.b.frame = (self.b.frame + self.b.FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % self.b.FRAMES_PER_ACTION

    def draw(self):
        idx = int(self.b.frame)
        col = idx % self.b.FRAME_COLS
        row = idx // self.b.FRAME_COLS
        sy_row = (self.b.FRAME_ROWS - 1 - row)
        sx, sy = col * self.b.w, sy_row * self.b.h
        try:
            Bird.image.clip_composite_draw(sx, sy, self.b.w, self.b.h, 0, 'h', self.b.x, self.b.y, self.b.w, self.b.h)
        except:
            Bird.image.clip_draw(sx, sy, self.b.w, self.b.h, self.b.x, self.b.y)
