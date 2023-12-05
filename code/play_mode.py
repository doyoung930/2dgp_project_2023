import random

from pico2d import *
import game_framework

import game_world
import item_mode
from map import DungeonMap
from character import PlayerCharacter
import skill
from monster import *
from skill import *

#from ball import Ball
#from zombie import Zombie

import server

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
            server.character.handle_event(event)

def init():
    global m1, sword1
    running = True

    server.map = DungeonMap()
    game_world.add_object(server.map, 0)



    server.character = PlayerCharacter()
    game_world.add_object(server.character, 2)
    game_world.add_collision_pair('character:hit', server.character, None)


    #game_world.add_collision_pair('zombie:ball', zombie, None)
    for _ in range(20):
        m1 = M1()
        sword1 = skill.Sword1()
        game_world.add_object(m1)
        game_world.add_collision_pair('character:hit',  server.character, m1)


        # game_world.add_collision_pair('M1:sword1', None, server.character.Sword1())

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

