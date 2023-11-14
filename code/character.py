# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDLK_UP, SDLK_DOWN, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT,  \
    draw_rectangle

import game_world
import game_framework


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
    print('up')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def up_down(e):
    print('up')
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
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:

    @staticmethod
    def enter(playercharacter, e):
        if playercharacter.face_dir == -1:#left
            playercharacter.action = 2
        elif playercharacter.face_dir == 1:#right
            playercharacter.action = 3
        elif playercharacter.face_dir == 2: #up
            playercharacter.action = 3
        elif playercharacter.face_dir == -2:    #down
            playercharacter.action = 3
        playercharacter.dir = 0
        playercharacter.frame = 0
        playercharacter.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.fire_ball()
        pass

    @staticmethod
    def do(playercharacter):
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - playercharacter.wait_time > 2:
            playercharacter.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(playercharacter):
        playercharacter.image.composite_draw(0, ' ', playercharacter.x, playercharacter.y, 50, 50)

class Run:

    @staticmethod
    def enter(playercharacter, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            playercharacter.dir, playercharacter.action, playercharacter.face_dir = 1, 0, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            playercharacter.dir, playercharacter.action, playercharacter.face_dir = -1, 0, -1
        elif up_up(e) or down_down(e):
            playercharacter.dir, playercharacter.action, playercharacter.face_dir = 1, 0, -2
        elif up_down or down_up(e):
            playercharacter.dir, playercharacter.action, playercharacter.face_dir = -1, 0, 2
    @staticmethod
    def exit(playercharacter, e):
        if space_down(e):
            playercharacter.fire_ball()

        pass

    @staticmethod
    def do(playercharacter):
        # playercharacter.frame = (playercharacter.frame + 1) % 8
        if playercharacter.face_dir == -1 or playercharacter.face_dir == 1:
            playercharacter.x += playercharacter.dir * RUN_SPEED_PPS * game_framework.frame_time
            playercharacter.x = clamp(25, playercharacter.x, 1600 - 25)
        elif  playercharacter.face_dir == -2 or playercharacter.face_dir == 2:
            print("2 or -2 ")
            playercharacter.y -= playercharacter.dir * RUN_SPEED_PPS * game_framework.frame_time
            playercharacter.y = clamp(25, playercharacter.y, 1600 - 25)

        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(playercharacter):
        if playercharacter.face_dir == -1:
            playercharacter.image.composite_draw(0, 'h', playercharacter.x, playercharacter.y, 50, 50)
        else:
            playercharacter.image.composite_draw(0, ' ', playercharacter.x, playercharacter.y, 50, 50)
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
        playercharacter.frame = (playercharacter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(playercharacter):
        if playercharacter.face_dir == -1:
            playercharacter.image.composite_draw(0, 'h', playercharacter.x, playercharacter.y, 50, 50)
        else:
            playercharacter.image.composite_draw(0, ' ', playercharacter.x, playercharacter.y, 50, 50)


class StateMachine:
    def __init__(self, playercharacter):
        self.playercharacter = playercharacter
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Run, down_down: Run, up_up: Run, down_up: Run, time_out: Sleep, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle, space_down: Run},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, down_down: Run, up_up: Run, down_up: Run}
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
        self.cur_state.draw(self.playercharacter)

animation_names = ['Walk']
class PlayerCharacter:
    images = None
    def load_images(self):
        if PlayerCharacter.images == None:
            PlayerCharacter.images = {}
            for name in animation_names:
                PlayerCharacter.images[name] = [load_image("./png/character/ch1/walk/" + "Walk" + " _%d" % i + ".png") for i in range(0, 5)]

    def __init__(self):
        self.x, self.y = 50, 90
        self.frame = 0
        self.action = 3     # 2 left 3 right
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('./png/character/ch1/walk/Walk_1.png')
        self.sleep_image = load_image('./png/character/ch1/walk/Walk_1.png')
        self.walk_image = load_image('./png/character/ch1/walk/Walk_1.png')
        self.attack_image = load_image('./png/character/ch1/walk/Walk_1.png')
        self.load_images()
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.ball_count = 10

    # def fire_ball(self):
    #     if self.ball_count > 0:
    #         self.ball_count -= 1
    #         ball = Ball(self.x, self.y, self.face_dir*10)
    #         game_world.add_object(ball)
    #         game_world.add_collision_pair('zombie:ball', None, ball)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        #self.font.draw(self.x - 10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))


    # fill here
