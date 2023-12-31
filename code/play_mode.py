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
import time
# from ball import Ball
# from zombie import Zombie

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            server.character.hp = 99999
        else:
            server.character.handle_event(event)


def init():
    global m1, sword1
    running = True

    server.map = DungeonMap()
    game_world.add_object(server.map, 0)

    server.character = PlayerCharacter()
    game_world.add_object(server.character, 2)
    game_world.add_collision_pair('character:M1', server.character, None)
    game_world.add_collision_pair('character:M2', server.character, None)
    game_world.add_collision_pair('character:M3', server.character, None)
    game_world.add_collision_pair('character:M4', server.character, None)
    game_world.add_collision_pair('character:M5', server.character, None)

    # game_world.add_collision_pair('zombie:ball', zombie, None)




    sword1 = skill.Sword1()
    sword2 = server.character.Sword2()
    shield = server.character.Shield()
    axe = server.character.Axe()

    for _ in range(60):
        m1 = M1()
        game_world.add_object(m1)

        game_world.add_collision_pair('M1:sword1', m1, None)
        game_world.add_collision_pair('M1:sword2', m1, None)
        game_world.add_collision_pair('M1:axe', m1, None)
        game_world.add_collision_pair('M1:shield', m1, None)
        game_world.add_collision_pair('character:M1', None, m1)


    for _ in range(40):
        m2 = M2()
        game_world.add_object(m2)

        game_world.add_collision_pair('M2:sword1', m2, None)
        game_world.add_collision_pair('M2:sword2', m2, None)
        game_world.add_collision_pair('M2:axe', m2, None)
        game_world.add_collision_pair('M2:shield', m2, None)
        game_world.add_collision_pair('character:M2', None, m2)


    for _ in range(10):
        m3 = M3()
        game_world.add_object(m3)

        game_world.add_collision_pair('M3:sword1', m3, None)
        game_world.add_collision_pair('M3:sword2', m3, None)
        game_world.add_collision_pair('M3:axe', m3, None)
        game_world.add_collision_pair('M3:shield', m3, None)
        game_world.add_collision_pair('character:M3', None, m3)
    m4 = M4()
    game_world.add_collision_pair('M4:sword1', m4, None)
    game_world.add_collision_pair('M4:sword2', m4, None)
    game_world.add_collision_pair('M4:axe', m4, None)
    game_world.add_collision_pair('M4:shield', m4, None)
    game_world.add_collision_pair('character:M4', None, m4)
    m5 = M5()

    game_world.add_collision_pair('M5:sword1', m5, None)
    game_world.add_collision_pair('M5:sword2', m5, None)
    game_world.add_collision_pair('M5:axe', m5, None)
    game_world.add_collision_pair('M5:shield', m5, None)
    game_world.add_collision_pair('character:M5', None, m5)
    sword1 = Sword1()
    game_world.add_collision_pair('M1:sword1', None, sword1)
    game_world.add_collision_pair('M2:sword1', None, sword1)
    game_world.add_collision_pair('M3:sword1', None, sword1)
    game_world.add_collision_pair('M4:sword1', None, sword1)
    game_world.add_collision_pair('M5:sword1', None, sword1)

    sword2 = server.character.Sword2()
    game_world.add_collision_pair('M1:sword2', None, sword2)
    game_world.add_collision_pair('M2:sword2', None, sword2)
    game_world.add_collision_pair('M3:sword2', None, sword2)
    game_world.add_collision_pair('M4:sword2', None, sword2)
    game_world.add_collision_pair('M5:sword2', None, sword2)

    shield = server.character.Shield()
    game_world.add_collision_pair('M1:shield', None, shield)
    game_world.add_collision_pair('M2:shield', None, shield)
    game_world.add_collision_pair('M3:shield', None, shield)
    game_world.add_collision_pair('M4:shield', None, shield)
    game_world.add_collision_pair('M5:shield', None, shield)

    axe = server.character.Axe()
    game_world.add_collision_pair('M1:axe', None, axe)
    game_world.add_collision_pair('M2:axe', None, axe)
    game_world.add_collision_pair('M3:axe', None, axe)
    game_world.add_collision_pair('M4:axe', None, axe)
    game_world.add_collision_pair('M5:axe', None, axe)

    # game_world.add_collision_pair('M1:sword1', None, server.character.Sword1())


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

    if server.character.level == server.character.c_level + 1:
        game_framework.push_mode(item_mode)
        server.character.c_level = server.character.level


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
