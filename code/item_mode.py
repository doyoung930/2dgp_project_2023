import game_framework
import game_world
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time
import pico2d
import play_mode
from item_select import Item_Select
import server
import time
def init():
    global item_select
    item_select = Item_Select()
    game_world.add_object(item_select, 3)

def finish():
    game_world.remove_object(item_select)

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    # global item_select


def handle_events(): 
    events = get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_1:
                    server.character.s_time = 0
                    game_framework.pop_mode()
                    server.character.sword1_level += 1
                    server.character.hp = 100
                case pico2d.SDLK_2:
                    server.character.s_time = 0
                    #game_framework.pop_mode()
                    game_framework.pop_mode()
                    if server.character.sword1_level< 8:
                        server.character.sword2_level += 1
                    server.character.hp = 100
                case pico2d.SDLK_3:
                    server.character.s_time = 0
                    #game_framework.pop_mode()
                    game_framework.pop_mode()
                    if server.character.axe_level < 4:
                        server.character.axe_level += 1
                    server.character.hp = 100
def pause():
    pass


def resume():
    pass
