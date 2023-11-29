import random

from pico2d import *
import game_framework

import game_world
import item_mode
from map import DungeonMap
from character import PlayerCharacter
from character_obj import BaseGauge
import skill

#from ball import Ball
#from zombie import Zombie


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_mode(item_mode)
        else:
            playercharacter.handle_event(event)

def init():
    global dungeon_map
    global playercharacter

    running = True

    dungeon_map = DungeonMap()
    game_world.add_object(dungeon_map, 0)

    basegauge = BaseGauge()
    game_world.add_object(basegauge, 0)

    playercharacter = PlayerCharacter()
    game_world.add_object(playercharacter, 2)


    #
    # shield = skill.Shield()
    # game_world.add_object(playercharacter, 2)
    # sword1 = skill.Sword1()
    # game_world.add_object(playercharacter, 2)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

