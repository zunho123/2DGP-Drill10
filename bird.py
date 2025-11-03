from pico2d import load_image
import game_framework
from state_machine import StateMachine

def at_edge(e):
    return e[0] == 'EDGE'

class Bird:

    image = None

    FRAME_COLS = 5
    FRAME_ROWS = 3
    FPS = 12

    LEFT = 50
    RIGHT = 1550
    TOP_Y = 540
    SPEED = 250

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x, self.y = self.LEFT, self.TOP_Y
        self.dir = 1
        self.time = 0.0
        self.frame = 0

        self.w = Bird.image.w // self.FRAME_COLS
        self.h = Bird.image.h // self.FRAME_ROWS
        self.total_frames = self.FRAME_COLS * self.FRAME_ROWS

        self.fly_right = FlyRight(self)
        self.fly_left  = FlyLeft(self)

        self.state_machine = StateMachine(
            self.fly_right,
            {
                self.fly_right: { at_edge: self.fly_left  },
                self.fly_left:  { at_edge: self.fly_right },
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_state_event(self, event):
        self.state_machine.handle_state_event(event)

    def draw(self):
        self.state_machine.draw()

class FlyRight:
    def __init__(self, bird): self.bird = bird
    def enter(self, e): self.bird.dir = 1
    def exit(self, e):  pass

    def do(self):
        dt = game_framework.frame_time
        b = self.bird

        b.x += b.SPEED * dt
        if b.x >= b.RIGHT:
            b.x = b.RIGHT
            b.handle_state_event(('EDGE', None))

        b.time += dt
        b.frame = int(b.time * b.FPS) % b.total_frames

    def draw(self):
        b = self.bird
        col = b.frame % b.FRAME_COLS
        row = b.frame // b.FRAME_COLS
        sx, sy = col * b.w, row * b.h
        try:
            Bird.image.clip_draw(sx, sy, b.w, b.h, b.x, b.y)
        except:
            Bird.image.clip_draw(sx, sy, b.w, b.h, b.x, b.y)

class FlyLeft:
    def __init__(self, bird): self.bird = bird
    def enter(self, e): self.bird.dir = -1
    def exit(self, e):  pass

    def do(self):
        dt = game_framework.frame_time
        b = self.bird

        b.x -= b.SPEED * dt
        if b.x <= b.LEFT:
            b.x = b.LEFT
            b.handle_state_event(('EDGE', None))

        b.time += dt
        b.frame = int(b.time * b.FPS) % b.total_frames

    def draw(self):
        b = self.bird
        col = b.frame % b.FRAME_COLS
        row = b.frame // b.FRAME_COLS
        sx, sy = col * b.w, row * b.h
        try:
            Bird.image.clip_composite_draw(sx, sy, b.w, b.h, 0, 'h', b.x, b.y, b.w, b.h)
        except:
            Bird.image.clip_draw(sx, sy, b.w, b.h, b.x, b.y)
