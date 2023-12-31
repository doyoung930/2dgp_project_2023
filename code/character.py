# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDLK_UP, SDLK_DOWN, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, \
    SDLK_LEFT, SDLK_RIGHT, SDLK_i, SDLK_e, \
    draw_rectangle, load_wav
import game_world
import game_framework
from map import DungeonMap

import skill
import server
import math
import time
import monster
import game_over
import clear
# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def upkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def upkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def downkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def downkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def item_mode(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i
def item_mode(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e
def time_out(e):
    return e[0] == 'TIME_OUT'


# time_out = lambda e : e[0] == 'TIME_OUT'


# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3
FRAMES_PER_ACTION_MOVE = 5
FRAMES_PER_ACTION_IDLE = 3



class Idle:

    @staticmethod
    def enter(playercharacter, e):

        if playercharacter.face_dir == -1:  # left
            playercharacter.action = 2
        elif playercharacter.face_dir == 1:  # right
            playercharacter.action = 3
        elif playercharacter.face_dir == 2:  # up
            playercharacter.action = 3
        elif playercharacter.face_dir == -2:  # down
            playercharacter.action = 3
        playercharacter.dir = 1
        playercharacter.dir2 = 0
        playercharacter.frame = 0
        playercharacter.wait_time = get_time()  # pico2d import 필요

        pass

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):

        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def draw(playercharacter):
        playercharacter.character_exp()
        playercharacter.images['Idle'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.sx,
                                                                                  playercharacter.sy, 50, 50)



class RunRight:
    @staticmethod
    def enter(playercharacter, e):
        playercharacter.action = 1
        playercharacter.face_dir = 1
        pass

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.x += RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.sx,
                                                                                  playercharacter.sy, 55, 55)


class RunRightUp:
    @staticmethod
    def enter(playercharacter, e):
        playercharacter.action = 1
        playercharacter.face_dir = 2
        pass

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass
    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.x += RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.y += RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.sx,
                                                                                  playercharacter.sy, 55, 55)


class RunRightDown:
    @staticmethod
    def enter(playercharacter, e):
        playercharacter.action = 1
        playercharacter.face_dir = 3
        pass

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.x += RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.y -= RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.sx,
                                                                                  playercharacter.sy, 55, 55)


class RunLeft:
    @staticmethod
    def enter(playercharacter, e):
        playercharacter.action = 0
        playercharacter.face_dir = 4
        pass

    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.x -= RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)

        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.sx - 10,
                                                                                  playercharacter.sy, 55, 55)

class RunLeftUp:
    @staticmethod
    def enter(playercharacter, e):
        playercharacter.action = 0
        playercharacter.face_dir = 5
        pass

    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.x -= RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.y += RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.sx - 10,
                                                                                  playercharacter.sy, 55, 55)
class RunLeftDown:
    @staticmethod
    def enter(playercharacter, e):
        playercharacter.action = 0
        playercharacter.face_dir = 6
        pass

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.x -= RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.y -= RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.sx - 10,
                                                                                  playercharacter.sy, 55, 55)
class RunUp:
    @staticmethod
    def enter(playercharacter, e):
        if playercharacter.action == 2:
            playercharacter.action = 0
        elif playercharacter.action == 3:
            playercharacter.action = 1
        playercharacter.face_dir = 7


    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.y += RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.sx - 10,
                                                                                  playercharacter.sy, 55, 55)
class RunDown:
    @staticmethod
    def enter(playercharacter, e):
        if playercharacter.action == 2:
            playercharacter.action = 0
        elif playercharacter.action == 3:
            playercharacter.action = 1
        playercharacter.face_dir = 8
        pass

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        playercharacter.y -= RUN_SPEED_PPS * game_framework.frame_time
        playercharacter.x = clamp(50, playercharacter.x, server.map.w - 50.0)
        playercharacter.y = clamp(50, playercharacter.y, server.map.h - 50.0)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.sx,
                                                                                  playercharacter.sy, 55, 55)


class Attack:
    def enter(playercharacter, e):
        pass

    def exit(playercharacter, e):
        pass

    @staticmethod
    def do(playercharacter):
           pass

    @staticmethod
    def draw(playercharacter):
        pass

class Sleep:

    @staticmethod
    def enter(playercharacter, e):
        playercharacter.frame = 0
        pass

    @staticmethod
    def exit(playercharacter, e):
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = ( playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

    @staticmethod
    def draw(playercharacter):
        if playercharacter.face_dir == -1:
            playercharacter.images['Idle'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.x,
                                                                                          playercharacter.y, 50, 50)
        else:
            playercharacter.images['Idle'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.x,
                                                                                          playercharacter.y, 50, 50)

class StateMachine:
    def __init__(self, playercharacter):
        self.playercharacter = playercharacter
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, upkey_down: RunUp,downkey_down: RunDown, upkey_up: RunDown, downkey_up: RunUp, space_down: Idle},
            RunRight: {right_up: Idle, left_down: Idle, upkey_down: RunRightUp, upkey_up: RunRightDown,downkey_down: RunRightDown, downkey_up: RunRightUp, space_down: RunRight},
            RunRightUp: {upkey_up: RunRight, right_up: RunUp, left_down: RunUp, downkey_down: RunRight, space_down: RunRightUp},
            RunUp: {upkey_up: Idle, left_down: RunLeftUp, downkey_down: Idle, right_down: RunRightUp,left_up: RunRightUp, right_up: RunLeftUp, space_down: RunUp},
            RunLeftUp: {right_down: RunUp, downkey_down: RunLeft, left_up: RunUp, upkey_up: RunLeft, space_down: RunLeftUp},
            RunLeft: {left_up: Idle, upkey_down: RunLeftUp, right_down: Idle, downkey_down: RunLeftDown,upkey_up: RunLeftDown, downkey_up: RunLeftUp, space_down: RunLeft},
            RunLeftDown: {left_up: RunDown, downkey_up: RunLeft, upkey_down: RunLeft, right_down: RunDown, space_down: RunLeftDown},
            RunDown: {downkey_up: Idle, left_down: RunLeftDown, upkey_down: Idle, right_down: RunRightDown,left_up: RunRightDown, right_up: RunLeftDown, space_down: RunDown},
            RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight, space_down: RunRightDown}
        }


    def start(self):
        self.cur_state.enter(self.playercharacter, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.playercharacter)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.playercharacter, e)
                self.cur_state = next_state
                self.cur_state.enter(self.playercharacter, e)
                return True
        return False

    def draw(self):
        # DungeonMap 그리기
        # game_world.add_object(dungeon_map)
        self.cur_state.draw(self.playercharacter)

animation_names = ['Walk', 'Idle']

class PlayerCharacter:
    images = None
    def load_images(self):
        if PlayerCharacter.images == None:
            PlayerCharacter.images = {}
            for name in animation_names:
                PlayerCharacter.images[name] = [load_image("./png/character/ch1/walk/" + name + "_%d" % i + ".png")
                                                for
                                                i in range(0, 5)]

    def __init__(self):

        self.at_sound = load_wav('attack.wav')
        self.s2_sound = load_wav('sword2.wav')
        self.axe_sound = load_wav('axe.wav')
        self.at_sound.set_volume(30)
        self.s2_sound.set_volume(30)
        self.axe_sound.set_volume(30)
        self.bgm = load_wav('bg.wav')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        self.time_since_last_monster = 0.0
        self.x, self.y = 1580, 2000
        self.sx = 1580
        self.sy = 2000
        
        self.frame = 0  # 캐릭터 프레임
        self.action = 3  # 2 left 3 right
        self.face_dir = 1  # 얼굴 방향
        self.dir = 0  # 좌우 방향
        self.dir2 = 0  # 위아래 방향
        self.load_images()  # 캐릭터 이미지 모음
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.player_width = 50  # 플레이어 크기 width
        self.player_height = 50  # 플레이어 크기 height

        self.c_level = 0
        self.level = 0
        self.next_level = 1

        self.player_speed = 1


        # shield1
        self.shield_image = load_image("./png/weapon/shield-05.png")
        self.shield_level = 1
        self.shield_angle = 0
        self.shield_radius = 100
        self.shield_x = self.sx
        self.shield_y = self.sy + 100 * math.sin(math.radians(self.shield_angle))

        # sword1
        #self.shield_image = load_image("./png/weapon/shield-05.png")
        self.sword1_level = 1
        self.sword1_x = self.sx
        self.sword1_y = self.sy

        # sword2
        self.sword2_image = load_image("./png/weapon/Sword-2-05.png")
        self.sword2_level = 0 #<8

        # sword2 timer
        self.sword_cooldown = 3.0  # Sword2 함수의 실행 주기를 나타내는 변수
        self.shield_cooldown = 3.0  # Sword2 함수의 실행 주기를 나타내는 변수
        self.time_since_last_sword = 0.0  # 마지막 Sword2 함수 실행 이후의 경과 시간을 저장하는 변수
        self.time_since_last_shield = 0.0  # 마지막 Sword2 함수 실행 이후의 경과 시간을 저장하는 변수

        # axe
        self.axe_level = 0 #<4


        #base
        self.exp_w_image = load_image('./png/gui/exp_w.png')
        self.base_image = load_image('./png/gui/base_gauge2.png')

        #hp
        self.HP_image = load_image('./png/gui/hp_gauge2.png')
        self.hp = 100
        self.max_hp = 100

        # exp
        self.EXP_image = load_image('./png/gui/exp_gauge2.png')
        self.exp = 0  # 플레이어 경험치
        self.max_exp = 1000

        self.s_time = 0
    def character_exp(self):
        pass

    def Shield(self):
        if self.shield_level > 0:
            shield = skill.Shield(self.sx, self.sy, self.shield_level)
            game_world.add_object(shield)


    def Sword1(self):
        if self.sword1_level > 0:
            self.at_sound.play()
            sword1 = skill.Sword1(self.sx, self.sy, self.dir * 10, self.face_dir, self.dir2 * 10)
            game_world.add_object(sword1)
            game_world.add_collision_pair('M1:sword1', None, sword1)
            game_world.add_collision_pair('M2:sword1', None, sword1)
            game_world.add_collision_pair('M3:sword1', None, sword1)
            game_world.add_collision_pair('M4:sword1', None, sword1)
            game_world.add_collision_pair('M5:sword1', None, sword1)

    def Sword2(self):
        if self.sword2_level > 0:
            self.s2_sound.play()

            sword2 = skill.Sword2(self.sx, self.sy, 3, self.sword2_level)
            game_world.add_object(sword2)
            game_world.add_collision_pair('M1:sword2', None, sword2)
            game_world.add_collision_pair('M2:sword2', None, sword2)
            game_world.add_collision_pair('M3:sword2', None, sword2)
            game_world.add_collision_pair('M4:sword2', None, sword2)
            game_world.add_collision_pair('M5:sword2', None, sword2)

    def Axe(self):
        if self.axe_level > 0:
            self.axe_sound.play()
            axe = skill.Axe(self.sx, self.sy, self.axe_level)

            game_world.add_object(axe)
            game_world.add_collision_pair('M1:axe', None, axe)
            game_world.add_collision_pair('M2:axe', None, axe)
            game_world.add_collision_pair('M3:axe', None, axe)
            game_world.add_collision_pair('M4:axe', None, axe)
            game_world.add_collision_pair('M5:axe', None, axe)


    def base_g(self):
        self.exp_w_image.composite_draw(0, ' ', server.map.cw - 1250, server.map.ch - 710, 60, 17)
        self.base_image.composite_draw(0 , ' ', server.map.cw - 610, server.map.ch-710, 1220, 15)

    def EXP(self):
        self.e_exp = self.exp / 1000 * 1220
        #self.EXP_image.composite_draw(0, ' ', server.map.cw - 610, server.map.ch-710, 1220, 15)
        self.EXP_image.composite_draw(0, ' ', server.map.cw - 1220 + 610 * self.exp/1000 , server.map.ch-710, self.e_exp , 15)

    def Shoes(self):
        pass

    def WarriorHat(self):
        pass

    def update(self):
        time.sleep(self.s_time)
        #print(self.sx, self.sy)
        self.state_machine.update()
        self.x = clamp(50.0, self.x, server.map.w - 50.0)
        self.y = clamp(50.0, self.y, server.map.h - 50.0)
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom



    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

        self.HP_image.composite_draw(0, ' ', self.sx-10, self.sy+30, self.hp/2, 5)



        # dt는 경과된 시간(delta time)을 나타냅니다.
        self.time_since_last_sword += 0.005
        self.time_since_last_monster += 0.0001
        if self.time_since_last_monster >= 100.0:
            game_framework.change_mode(clear)

        # Sword2 함수를 주기적으로 실행하기 위한 조건문
        if self.time_since_last_sword >= self.sword_cooldown:
            self.Sword2()
            self.Axe()
            self.time_since_last_sword = 0.0  # 경과 시간 초기화
            for _ in range(20):
                m1 = monster.M1()
                game_world.add_object(m1)
                game_world.add_collision_pair('M1:sword1', m1, None)
                game_world.add_collision_pair('M1:sword2', m1, None)
                game_world.add_collision_pair('M1:axe', m1, None)
                game_world.add_collision_pair('M1:shield', m1, None)
                game_world.add_collision_pair('character:M1', None, m1)
            for _ in range(5):
                m3 = monster.M3()
                game_world.add_object(m3)
                game_world.add_collision_pair('M3:sword1', m3, None)
                game_world.add_collision_pair('M3:sword2', m3, None)
                game_world.add_collision_pair('M3:axe', m3, None)
                game_world.add_collision_pair('M3:shield', m3, None)
                game_world.add_collision_pair('character:M3', None, m3)
            for _ in range(3):
                m4 = monster.M4()
                game_world.add_object(m4)
                game_world.add_collision_pair('M4:sword1', m4, None)
                game_world.add_collision_pair('M4:sword2', m4, None)
                game_world.add_collision_pair('M4:axe', m4, None)
                game_world.add_collision_pair('M4:shield', m4, None)
                game_world.add_collision_pair('character:M4', None, m4)
            for _ in range(1):
                m5 = monster.M5()
                game_world.add_object(m5)
                game_world.add_collision_pair('M5:sword1', m5, None)
                game_world.add_collision_pair('M5:sword2', m5, None)
                game_world.add_collision_pair('M5:axe', m5, None)
                game_world.add_collision_pair('M5:shield', m5, None)
                game_world.add_collision_pair('character:M5', None, m5)
            if self.level == 8:
                for _ in range(20):
                    m4 = monster.M4()
                    game_world.add_object(m4)
                    game_world.add_object(m4)
                    game_world.add_collision_pair('M4:sword1', m4, None)
                    game_world.add_collision_pair('M4:sword2', m4, None)
                    game_world.add_collision_pair('M4:axe', m4, None)
                    game_world.add_collision_pair('M4:shield', m4, None)
                    game_world.add_collision_pair('character:M4', None, m4)
            if self.level == 12:
                for _ in range(10):
                    m5 = monster.M5()
                    game_world.add_object(m5)
                    game_world.add_collision_pair('M5:sword1', m5, None)
                    game_world.add_collision_pair('M5:sword2', m5, None)
                    game_world.add_collision_pair('M5:axe', m5, None)
                    game_world.add_collision_pair('M5:shield', m5, None)
                    game_world.add_collision_pair('character:M5', None, m5)

        #if self.time_since_last_monster >=self.sword_cooldown:

        #self.Shield()

        self.base_g()
        self.EXP()
        
    def get_bb(self):
        return self.sx-25, self.sy-25, self.sx+15 , self.sy+25

    # fill here
    def handle_collision(self, group, other):
        match group:
            case 'character:M1':
                self.hp -= 1

            case 'character:M2':
                self.hp -= 1
            case 'character:M3':
                self.hp -= 1
            case 'character:M4':
                self.hp -= 1
            case 'character:M5':
                self.hp -= 1
        if self.hp < -9999:
            game_framework.change_mode(game_over)