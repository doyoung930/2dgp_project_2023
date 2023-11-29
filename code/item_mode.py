import game_framework
import game_world
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time
import pico2d

from item_select import Item_Select

def init():
    global item_select
    item_select = Item_Select()
    game_world.add_object(item_select, 3)

def finish():
    game_world.remove_object(item_select)

def update(): pass


def draw(): pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_1:
                    game_framework.pop_mode()
                case pico2d.SDLK_2:
                    game_framework.pop_mode()

def pause(): pass


def resume(): pass
