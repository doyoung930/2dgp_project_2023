# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDLK_UP, SDLK_DOWN, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, \
    SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle

import game_world
import game_framework
from map import DungeonMap
from character_obj import Exp
import skill
from skill import Shield
import math


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
FRAMES_PER_ACTION = 8
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
        playercharacter.Shield()
        playercharacter.character_exp()
        playercharacter.images['Idle'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.x,
                                                                                  playercharacter.y, 50, 50)



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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.x,
                                                                                  playercharacter.y, 55, 55)


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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.x,
                                                                                  playercharacter.y, 55, 55)


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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.x,
                                                                                  playercharacter.y, 55, 55)


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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)

        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.x - 10,
                                                                                  playercharacter.y, 55, 55)

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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.x - 10,
                                                                                  playercharacter.y, 55, 55)
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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.x - 10,
                                                                                  playercharacter.y, 55, 55)
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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.x - 10,
                                                                                  playercharacter.y, 55, 55)
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
        playercharacter.x = clamp(25, playercharacter.x, 1280 - 25)
        playercharacter.y = clamp(25, playercharacter.y, 720 - 25)
        pass

    @staticmethod
    def draw(playercharacter):
        playercharacter.Shield()
        playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.x,
                                                                                  playercharacter.y, 55, 55)


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
        playercharacter.frame = (
                                        playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

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

        global dungeon_map
        dungeon_map = DungeonMap()
        self.x, self.y = 1280 / 2, 720 / 2
        self.camera_x = self.x - (1280 - 50) // 2
        self.camera_y = self.y - (1280 - 50) // 2
        
        self.frame = 0  # 캐릭터 프레임
        self.action = 3  # 2 left 3 right
        self.face_dir = 1  # 얼굴 방향
        self.dir = 0  # 좌우 방향
        self.dir2 = 0  # 위아래 방향
        self.load_images()  # 캐릭터 이미지 모음
        self.HP_image = load_image('./png/gui/hp_gauge2.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.player_width = 50  # 플레이어 크기 width
        self.player_height = 50  # 플레이어 크기 height
        self.level = 0
        self.next_level = 1
        self.player_speed = 1
        self.exp = 0        # 플레이어 경험치
        self.hp = 100

        # shield1
        self.shield_image = load_image("./png/weapon/shield-05.png")
        self.Shield_level = 1
        self.shield_angle = 0
        self.shield_radius = 100
        self.shield_x = self.x
        self.shield_y = self.y + 100 * math.sin(math.radians(self.shield_angle))
        # sword1
        #self.shield_image = load_image("./png/weapon/shield-05.png")
        self.sword1_level = 1
        self.sword1_x = self.x
        self.sword1_y = self.y

        # sword2
        self.sword2_image = load_image("./png/weapon/Sword-2-05.png")
        self.sword2_level = 1
        self.sword2_speed = 5
        self.sword2_angle = 0
        self.sword2_x = self.x
        self.sword2_y = self.y
        self.sword2_pos =[
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
        ]

        # axe
        self.axe_image = load_image("./png/weapon/axe-03.png")
        self.axe_level = 1
        self.axe_speed = 10
        self.axe_x = self.x
        self.axe_y = self.y
        self.axe_pos = [
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
            (self.x, self.y),
        ]

    def character_exp(self):
        exp = Exp(self.exp)
        game_world.add_object(exp)

    def Shield(self):
        if self.Shield_level > 0:
        #    self.shield_image.composite_draw(0, ' ', self.shield_x, self.shield_y, 40, 40)
            for i in range(1, self.Shield_level+1):
                # 플레이어의 좌표를 중점으로 원운동
                self.shield_angle += 0.5/self.Shield_level
                # 각도가 360도를 넘어가면 360도로 초기화
                if self.shield_angle+(360/i) >= 360:
                    self.shield_angle -= 360
                self.shield_x = self.x + 100 * math.cos(math.radians(self.shield_angle+(360/self.Shield_level)*i))
                self.shield_y = self.y + 100 * math.sin(math.radians(self.shield_angle+(360/self.Shield_level)*i))
                self.shield_image.composite_draw(0, ' ', self.shield_x, self.shield_y, 40, 40)

    def Sword1(self):
        sword1 = skill.Sword1(self.x, self.y, self.dir * 10, self.face_dir, self.dir2 * 10)
        game_world.add_object(sword1)

    def Sword2(self):
        # 리스트를 이용해 칼 총 8개를 관리 해야함.
        # 1 x ++ 2 x -- 3 y++ 4 y -- 5 오른쪽 위 6 오른쪽 밑 7 왼쪽 위 8 왼쪽 밑
        self.sword2_angle -= 0.5
        if self.sword2_level > 0:
            for i in range(0, self.sword2_level):
                if i == 0:
                    self.sword2_pos[i] = (self.sword2_pos[i][0]+ self.sword2_speed, self.sword2_pos[i][1])
                    self.sword2_image.composite_draw(self.sword2_angle, ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
                if i == 1:
                    self.sword2_pos[i] = (self.sword2_pos[i][0] - self.sword2_speed, self.sword2_pos[i][1])
                    self.sword2_image.composite_draw(self.sword2_angle, 'h', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
                if i == 2:
                    self.sword2_pos[i] = (self.sword2_pos[i][0] , self.sword2_pos[i][1] + self.sword2_speed)
                    self.sword2_image.composite_draw(self.sword2_angle, '', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
                if i == 3:
                    self.sword2_pos[i] = (self.sword2_pos[i][0] , self.sword2_pos[i][1] - self.sword2_speed)
                    self.sword2_image.composite_draw(self.sword2_angle, 'h', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
                if i == 4:
                    self.sword2_pos[i] = (self.sword2_pos[i][0] + self.sword2_speed, self.sword2_pos[i][1] + self.sword2_speed)
                    self.sword2_image.composite_draw(self.sword2_angle, '', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
                if i == 5:
                    self.sword2_pos[i] = (self.sword2_pos[i][0] + self.sword2_speed, self.sword2_pos[i][1] - self.sword2_speed)
                    self.sword2_image.composite_draw(self.sword2_angle, '', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
                if i == 6:
                    self.sword2_pos[i] = (self.sword2_pos[i][0] - self.sword2_speed, self.sword2_pos[i][1] + self.sword2_speed)
                    self.sword2_image.composite_draw(self.sword2_angle, 'h', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
                if i == 7:
                    self.sword2_pos[i] = (self.sword2_pos[i][0] - self.sword2_speed, self.sword2_pos[i][1] - self.sword2_speed)
                    self.sword2_image.composite_draw(self.sword2_angle, 'h', self.sword2_pos[i][0], self.sword2_pos[i][1], 40, 40)
            if self.sword2_pos[0][0] > 4000:
                for i in range(0, self.sword2_level):
                    self.sword2_pos[i] = (self.x, self.y)


    def Axe(self):
        if self.axe_level > 0:
            self.axe_image.composite_draw(0, ' ', self.axe_x, self.axe_y, 40, 40)

    def Shoes(self):
        pass

    def WarriorHat(self):
        pass

    def update(self):
        self.state_machine.update()



    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.HP_image.composite_draw(0, ' ', self.x-10, self.y+30, self.hp/2, 5)
        self.Shield()
        self.Sword2()
