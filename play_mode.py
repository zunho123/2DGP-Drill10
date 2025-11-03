from pico2d import *
from bird import Bird
from boy import Boy
from grass import Grass
import game_world
import game_framework
import random

birds = []
boy = None


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global bird
    global running

    running = True
    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    base_x = Bird.LEFT
    top_y = Bird.TOP_Y

    birds = [Bird(x = base_x + random.randint(-5, 5), y = top_y - random.randint(0, 150)) for _ in range(10)]

    for b in birds:
        game_world.add_object(b, 2)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass
def resume():
    pass

