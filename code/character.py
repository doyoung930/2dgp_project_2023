# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDLK_UP, SDLK_DOWN, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, \
    SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle

import game_world
import game_framework
from map import DungeonMap
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


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


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
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
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
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 3
        if get_time() - playercharacter.wait_time > 2:
            playercharacter.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(playercharacter):
        #playercharacter.Shield()
        playercharacter.images['Idle'][int(playercharacter.frame)].composite_draw(0, ' ', playercharacter.x,
                                                                                  playercharacter.y, 50, 50)


class Run:

    @staticmethod
    def enter(playercharacter, e):
        if right_up(e) or left_up(e) or down_up(e) or up_up(e):
            print(playercharacter.dir2, playercharacter.action, playercharacter.face_dir)
            playercharacter.face_dir = 1
        #if right_down(e) or left_up(e):  # 오른쪽으로 RUN
        elif right_down(e):  # 오른쪽으로 RUN
            playercharacter.dir, playercharacter.action, playercharacter.face_dir = 1, 0, 1
        #elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
        elif left_down(e):  # 왼쪽으로 RUN
            playercharacter.dir, playercharacter.action, playercharacter.face_dir = -1, 0, -1
        #elif up_up(e) or down_down(e):
        elif down_down(e):
            playercharacter.dir2, playercharacter.action, playercharacter.face_dir = 1, 0, -2
        #elif up_down(e) or down_up(e):
        elif up_down(e):
            playercharacter.dir2, playercharacter.action, playercharacter.face_dir = -1, 0, 2

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.Sword1()
        pass

    @staticmethod
    def do(playercharacter):
        # playercharacter.frame = (playercharacter.frame + 1) % 8
        if playercharacter.face_dir == -1 or playercharacter.face_dir == 1:
            # playercharacter.x += playercharacter.dir * RUN_SPEED_PPS * game_framework.frame_time
            playercharacter.x = clamp(25, playercharacter.x, 1600 - 25)
        elif playercharacter.face_dir == -2 or playercharacter.face_dir == 2:
            # playercharacter.y -= playercharacter.dir2 * RUN_SPEED_PPS * game_framework.frame_time
            playercharacter.y = clamp(25, playercharacter.y, 1600 - 25)

        playercharacter.frame = (
                                            playercharacter.frame + FRAMES_PER_ACTION_MOVE * ACTION_PER_TIME * game_framework.frame_time) % 5

    @staticmethod
    def draw(playercharacter):
        # DungeonMap 그리기
        #dungeon_map.draw()
        #playercharacter.Shield()
        if playercharacter.face_dir == -1:
            playercharacter.images['Walk'][int(playercharacter.frame)].composite_draw(0, 'h', playercharacter.x - 10,
                                                                                      playercharacter.y, 55, 55)
        else:
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
        # DungeonMap 그리기
        #dungeon_map.draw()
        #playercharacter.Shield()
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
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Run, down_down: Run,
                   up_up: Run, down_up: Run, time_out: Sleep, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Idle, down_down: Idle,
                  up_up: Idle, down_up: Idle, space_down: Run},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, down_down: Run,
                    up_up: Run, down_up: Run}
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
        #game_world.add_object(dungeon_map)
        self.cur_state.draw(self.playercharacter)


animation_names = ['Walk', 'Idle']


class PlayerCharacter:
    images = None

    def load_images(self):
        if PlayerCharacter.images == None:
            PlayerCharacter.images = {}
            for name in animation_names:
                PlayerCharacter.images[name] = [load_image("./png/character/ch1/walk/" + name + "_%d" % i + ".png") for
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
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.ball_count = 10
        self.player_width = 50  # 플레이어 크기 width
        self.player_height = 50  # 플레이어 크기 height
        self.level = 0
        self.player_speed = 1

        # shield
        self.Shield_level = 0
        self.angle = 0
        self.shield_x = self.x + 100 * math.cos(math.radians(self.angle))
        self.shield_y = self.y + 100 * math.sin(math.radians(self.angle))
        self.angle_vel = 0

        # sword1
        self.sword1_level = 4
        self.angle = 0
        self.sword1_x = self.x
        self.sword1_y = self.y


        # sword2
        self.sword2_level = 4
        self.angle = 0
        self.sword2_x = self.x
        self.sword2_y = self.y

        # axe
        self.axe_level = 4
        self.angle = 0
        self.axe_x = self.x
        self.axe_y = self.y

        # 각도 업데이트
    # def fire_ball(self):
    #     if self.ball_count > 0:
    #         self.ball_count -= 1
    #         ball = Ball(self.x, self.y, self.face_dir*10)
    #         game_world.add_object(ball)
    #         game_world.add_collision_pair('zombie:ball', None, ball)

    def Shield(self):
        for i in range (0, self.Shield_level):
            self.angle = 360 // self.Shield_level * i
            self.angle_vel += 10 * game_framework.frame_time * 5 * (6 - self.Shield_level)
            self.angle +=self.angle_vel
            if self.angle >= 360:
                self.angle -= 360
            self.shield_x = self.x + 100 * math.cos(math.radians(self.angle)) - 110
            self.shield_y = self.y + 100 * math.sin(math.radians(self.angle))
            if self.Shield_level > 0:
                shield = Shield(self.shield_x, self.shield_y, 10, 100, 10)
                game_world.add_object(shield)
                # collision
                #game_world.add_collision_pair('zombie:ball', None, ball)
    def Sword1(self):
             sword1 = skill.Sword1(self.x, self.y, self.dir*10, self.face_dir, self.dir2*10)
             #print(self.face_dir)
             game_world.add_object(sword1)
             #game_world.add_collision_pair('zombie:ball', None, sword1)
    def Sword2(self):
        pass
    def Axe(self):
        pass
    def Shoes(self):
        pass

    def WarriorHat(self):
        pass

    def update(self):
        self.state_machine.update()
        self.camera_x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.camera_y -= self.dir2 * RUN_SPEED_PPS * game_framework.frame_time

        # 캐릭터가 화면 밖으로 나가지 않도록 clamp 함수를 사용하여 좌표 제한
        self.x = clamp(25, self.x, 1200 - 25)
        self.y = clamp(25, self.y, 720 - 25)

        # DungeonMap의 map_x 업데이트
        dungeon_map.map_x = self.camera_x
        dungeon_map.map_y = self.camera_y

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()


