import random

from pico2d import *
import game_framework

import game_world
from map import DungeonMap
from character import PlayerCharacter
#from ball import Ball
#from zombie import Zombie

playercharacter = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            playercharacter.handle_event(event)

def init():
    global dungeon_map
    global playercharacter

    running = True

    dungeon_map = DungeonMap()
    game_world.add_object(dungeon_map, 0)

    playercharacter = PlayerCharacter()
    game_world.add_object(playercharacter, 2)

    # fill here



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # fill here

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

