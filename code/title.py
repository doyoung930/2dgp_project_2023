import game_framework
import game_world
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time
import pico2d


def init():
    pass

def finish():
    pass

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_SPACE:
                    game_framework.quit()
                case pico2d.SDLK_ESCAPE:
                    game_framework.quit()


def pause():
    pass


def resume():
    pass
