from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

import server
import skill

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.5 / TIME_PER_ACTION

FRAMES_PER_M1_ACTION = 19.0
FRAMES_PER_M2_ACTION = 19.0
FRAMES_PER_M3_ACTION = 19.0
FRAMES_PER_M4_ACTION = 19.0
FRAMES_PER_M5_ACTION = 19.0

animation_names = ['Walk']


class M1:
    images = None

    def load_images(self):
        if M1.images == None:
            M1.images = {}
            for name in animation_names:
                M1.images[name] = [load_image("./png/monster/M1/png/walk/" + name + "_%d" % i + ".png")
                                   for i in range(0, 19)]

    def __init__(self):
        self.x, self.y = random.randint(1600 - 800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 19)
        self.dir = random.choice([-1, 1])

        self.x = random.randint(100, server.map.w - 100)
        self.y = random.randint(100, server.map.h - 100)
        self.size = clamp(0.7, random.random() * 2, 1.3)
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 19)
        self.state = 'Walk'

        self.i_state = 'Idle'
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

        # hp
        self.hp = 1

    def get_bb(self):
        return (
            self.x - 50 * self.size - server.map.window_left,
            self.y - 50 * self.size - server.map.window_bottom,
            self.x + 50 * self.size - server.map.window_left,
            self.y + 50 * self.size - server.map.window_bottom
        )

    def update(self):
        self.frame = (self.frame + FRAMES_PER_M1_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_M1_ACTION
        self.tx, self.ty = server.character.x, server.character.y
        self.bt.run()

    def draw(self):
        sx, sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        if math.cos(self.dir) < 0:
            M1.images[self.state][int(self.frame)].draw(sx, sy, 100 * self.size, 100 * self.size)
        else:
            M1.images[self.state][int(self.frame)].composite_draw(0, 'h', sx, sy, 100 * self.size, 100 * self.size)


    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        match group:
            case 'M1:sword1':
                self.hp -= server.character.sword1_level
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M1:sword2':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M1:shield':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M1:axe':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

    def set_target_location(self):
        self.tx, self.ty = server.character.x, server.character.y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_boy_nearby(self, r):
        if self.distance_less_than(server.character.sx, server.character.sy, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_character(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(server.character.sx, server.character.sy)
        if self.distance_less_than(server.character.boy.sx, server.character.boy.sy, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        # select random location around boy
        # self.tx = random.randint(int(server.character.x) - 600, int(server.character.x) + 600)
        # self.ty = random.randint(int(server.character.y) - 400, int(server.character.y) + 400)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # a1 = Action('Set random location', self.set_random_location)
        a1 = Action('Set target location', self.set_target_location)
        # c1 = Condition('소년이 근처에 있는가?', self.is_boy_nearby, 7)
        a2 = Action('Move to', self.move_to)
        root = SEQ_wander = Sequence('Wander', a1, a2)
        # root = SEQ_chase_ch = Sequence('Wander', c1, a2)
        self.bt = BehaviorTree(root)


class M2:
    images = None

    def load_images(self):
        if M2.images == None:
            M2.images = {}
            for name in animation_names:
                M2.images[name] = [load_image("./png/monster/M2/png/walk/" + name + "-%d" % i + ".png")
                                   for i in range(0, 19)]

    def __init__(self):
        self.x, self.y = random.randint(1600 - 800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 19)
        self.dir = random.choice([-1, 1])

        self.x = random.randint(100, server.map.w - 100)
        self.y = random.randint(100, server.map.h - 100)
        self.size = clamp(0.7, random.random() * 2, 1.3)
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 19)
        self.state = 'Walk'

        self.i_state = 'Idle'
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

        # hp
        self.hp = 2

    def get_bb(self):
        return (
            self.x - 50 * self.size - server.map.window_left,
            self.y - 50 * self.size - server.map.window_bottom,
            self.x + 50 * self.size - server.map.window_left,
            self.y + 50 * self.size - server.map.window_bottom
        )

    def update(self):
        self.frame = (self.frame + FRAMES_PER_M1_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_M1_ACTION
        self.tx, self.ty = server.character.x, server.character.y
        self.bt.run()

    def draw(self):
        sx, sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        if math.cos(self.dir) < 0:
            M2.images[self.state][int(self.frame)].composite_draw(0, 'h', sx, sy, 100 * self.size, 100 * self.size)
        else:
            M2.images[self.state][int(self.frame)].draw(sx, sy, 100 * self.size, 100 * self.size)



    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        match group:
            case 'M2:sword1':
                self.hp -= server.character.sword1_level
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M2:sword2':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M2:shield':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M2:axe':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = server.character.sx, server.character.sy
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        # select random location around boy
        self.tx = random.randint(int(server.character.x) - 600, int(server.character.x) + 600)
        self.ty = random.randint(int(server.character.y) - 400, int(server.character.y) + 400)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        root = SEQ_wander = Sequence('Wander', a1, a2)
        self.bt = BehaviorTree(root)


class M3:
    images = None

    def load_images(self):
        if M3.images == None:
            M3.images = {}
            for name in animation_names:
                M3.images[name] = [load_image("./png/monster/M3/png/walk/" + name + "_%d" % i + ".png")
                                   for i in range(0, 19)]

    def __init__(self):
        self.x, self.y = random.randint(1600 - 800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 19)
        self.dir = random.choice([-1, 1])

        self.x = random.randint(100, server.map.w - 100)
        self.y = random.randint(100, server.map.h - 100)
        self.size = clamp(0.7, random.random() * 2, 1.3)
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 19)
        self.state = 'Walk'

        self.i_state = 'Idle'
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

        # hp
        self.hp = 3

    def get_bb(self):
        return (
            self.x - 50 * self.size - server.map.window_left,
            self.y - 50 * self.size - server.map.window_bottom,
            self.x + 50 * self.size - server.map.window_left,
            self.y + 50 * self.size - server.map.window_bottom
        )

    def update(self):
        self.frame = (self.frame + FRAMES_PER_M1_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_M1_ACTION
        self.tx, self.ty = server.character.x, server.character.y
        self.bt.run()

    def draw(self):
        sx, sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        if math.cos(self.dir) < 0:
            M3.images[self.state][int(self.frame)].composite_draw(0, 'h', sx, sy, 100 * self.size, 100 * self.size)
        else:
            M3.images[self.state][int(self.frame)].draw(sx, sy, 100 * self.size, 100 * self.size)



    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        match group:
            case 'M3:sword1':
                self.hp -= server.character.sword1_level
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M3:sword2':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M3:shield':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M3:axe':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = server.character.sx, server.character.sy
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        # select random location around boy
        self.tx = random.randint(int(server.character.x) - 600, int(server.character.x) + 600)
        self.ty = random.randint(int(server.character.y) - 400, int(server.character.y) + 400)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        root = SEQ_wander = Sequence('Wander', a1, a2)
        self.bt = BehaviorTree(root)


class M4:
    images = None

    def load_images(self):
        if M4.images == None:
            M4.images = {}
            for name in animation_names:
                M4.images[name] = [load_image("./png/monster/M4/png/walk/" + name + "_%d" % i + ".png")
                                   for i in range(0, 19)]

    def __init__(self):
        self.x, self.y = random.randint(1600 - 800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 19)
        self.dir = random.choice([-1, 1])

        self.x = random.randint(100, server.map.w - 100)
        self.y = random.randint(100, server.map.h - 100)
        self.size = clamp(0.7, random.random() * 2, 1.3)
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 19)
        self.state = 'Walk'

        self.i_state = 'Idle'
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

        # hp
        self.hp = 4

    def get_bb(self):
        return (
            self.x - 50 * self.size - server.map.window_left,
            self.y - 50 * self.size - server.map.window_bottom,
            self.x + 50 * self.size - server.map.window_left,
            self.y + 50 * self.size - server.map.window_bottom
        )

    def update(self):
        self.frame = (self.frame + FRAMES_PER_M1_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_M1_ACTION
        self.tx, self.ty = server.character.x, server.character.y
        self.bt.run()
    def draw(self):
        sx, sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        if math.cos(self.dir) < 0:
            M4.images[self.state][int(self.frame)].composite_draw(0, 'h', sx, sy, 100 * self.size, 100 * self.size)
        else:
            M4.images[self.state][int(self.frame)].draw(sx, sy, 100 * self.size, 100 * self.size)



    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        match group:
            case 'M4:sword1':
                self.hp -= server.character.sword1_level
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M4:sword2':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M4:shield':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M4:axe':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = server.character.sx, server.character.sy
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        # select random location around boy
        self.tx = random.randint(int(server.character.x) - 600, int(server.character.x) + 600)
        self.ty = random.randint(int(server.character.y) - 400, int(server.character.y) + 400)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        root = SEQ_wander = Sequence('Wander', a1, a2)
        self.bt = BehaviorTree(root)


class M5:
    images = None

    def load_images(self):
        if M5.images == None:
            M5.images = {}
            for name in animation_names:
                M5.images[name] = [load_image("./png/monster/M5/png/walk/" + name + "_%d" % i + ".png")
                                   for i in range(0, 19)]

    def __init__(self):
        self.x, self.y = random.randint(1600 - 800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 19)
        self.dir = random.choice([-1, 1])

        self.x = random.randint(100, server.map.w - 100)
        self.y = random.randint(100, server.map.h - 100)
        self.size = clamp(0.7, random.random() * 2, 1.3)
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 19)
        self.state = 'Walk'

        self.i_state = 'Idle'
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

        # hp
        self.hp = 5

    def get_bb(self):
        return (
            self.x - 50 * self.size - server.map.window_left,
            self.y - 50 * self.size - server.map.window_bottom,
            self.x + 50 * self.size - server.map.window_left,
            self.y + 50 * self.size - server.map.window_bottom
        )

    def update(self):
        self.frame = (self.frame + FRAMES_PER_M1_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_M1_ACTION
        self.tx, self.ty = server.character.x, server.character.y
        self.bt.run()

    def draw(self):
        sx, sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        if math.cos(self.dir) < 0:
            M5.images[self.state][int(self.frame)].composite_draw(0, 'h', sx, sy, 100 * self.size, 100 * self.size)
        else:
            M5.images[self.state][int(self.frame)].draw(sx, sy, 100 * self.size, 100 * self.size)



    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        match group:
            case 'M5:sword1':
                self.hp -= server.character.sword1_level
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M5:sword2':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M5:shield':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

            case 'M5:axe':
                self.hp -= 1
                if self.hp <= 0:
                    game_world.remove_object(self)
                    server.character.exp += 100 / server.character.next_level
                    if server.character.exp >= 1000:
                        server.character.exp -= 1000
                        server.character.level += 1
                        server.character.next_level += 1

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = server.character.sx, server.character.sy
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        # select random location around boy
        self.tx = random.randint(int(server.character.x) - 600, int(server.character.x) + 600)
        self.ty = random.randint(int(server.character.y) - 400, int(server.character.y) + 400)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        root = SEQ_wander = Sequence('Wander', a1, a2)
        self.bt = BehaviorTree(root)
