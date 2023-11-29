import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time
import pico2d

from item_

def init(): pass


def finish(): pass


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
