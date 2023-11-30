import pico2d
import game_framework
import game_world
import play_mode

from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time


def init():
    running = True

    info = Info()
    game_world.add_object(info, 0)




def finish():
    game_world.clear()
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
            game_framework.change_mode(play_mode)
            # match event.key:
            #     case pico2d.SDLK_SPACE:
            #         game_framework.change_mode(play_mode)
            #     case pico2d.SDLK_ESCAPE:
            #         game_framework.quit()


def pause():
    pass


def resume():
    pass


class Info:
    def __init__(self):
        self.image = load_image('./png/gui/info.png')


    def update(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1056, 597, 0, ' ', 640, 360, 1280, 720)
