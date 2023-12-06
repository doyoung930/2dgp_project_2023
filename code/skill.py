from pico2d import *
import game_world
import game_framework
import server
import monster

import math

# 검이 전방으로 날아감 ( 짧은 사거리 공격 속도 빠름)
class Sword1:
    image = None

    def __init__(self, x=100000, y=100000, velocity=10, dir = 0, velocity2 = 10):
        if Sword1.image == None:
            Sword1.image = load_image("./png/weapon/Sword-02.png")
        self.x, self.y, self.velocity, self.velocity2 = x, y, velocity, -velocity2
        self.image_w = 40
        self.image_h = 40
        self.dir = dir

    def draw(self):
        # /1 right 2 3 /4 left /5 6 /7 up /8 down
        if self.dir == 7:
            self.image.composite_draw(0, ' ', self.x, self.y, self.image_w, self.image_h)
        elif self.dir == 8:
            self.image.composite_draw(0, 'v', self.x, self.y, self.image_w, self.image_h)
        elif self.dir == 1:
            self.image.composite_draw(-89.5, ' ', self.x, self.y, self.image_w, self.image_h)
        elif self.dir == 4:
            self.image.composite_draw(89.5, ' ', self.x, self.y, self.image_w, self.image_h)
        elif self.dir == 2:#RunRightUp
            self.image.composite_draw(-89.5/2, ' ', self.x, self.y, self.image_w, self.image_h)
        elif self.dir == 3:#RunRightdown
            self.image.composite_draw(-89.5-89.5/2, ' ', self.x, self.y, self.image_w, self.image_h)
        elif self.dir == 5:#Runleftup
            self.image.composite_draw(89.5/2, ' ', self.x, self.y, self.image_w, self.image_h)
        elif self.dir == 6:#Runleftdown
            self.image.composite_draw(89.5*3/2, ' ', self.x, self.y, self.image_w, self.image_h)

    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        # 방향에 따라
        if self.dir == 7:
            self.y += 10 * 100 * game_framework.frame_time
        elif self.dir == 8:
            self.y -= 10 * 100 * game_framework.frame_time
        elif self.dir == 1:
            self.x += 10 * 100 * game_framework.frame_time
        elif self.dir == 2: #RunRightUp
            self.x += 10 * 100 * game_framework.frame_time
            self.y += 10 * 100 * game_framework.frame_time
        elif self.dir == 3: #RunRightdown
            self.x += 10 * 100 * game_framework.frame_time
            self.y -= 10 * 100 * game_framework.frame_time
        elif self.dir == 4:
            self.x -= 10 * 100 * game_framework.frame_time
        elif self.dir == 5: #RunLeftup
            self.x -= 10 * 100 * game_framework.frame_time
            self.y += 10 * 100 * game_framework.frame_time
        elif self.dir == 6: ##RunLeftDown
            self.x -= 10 * 100 * game_framework.frame_time
            self.y -= 10 * 100 * game_framework.frame_time

        if self.x < 50 + server.character.sx - 600:
            game_world.remove_object(self)
        if self.x > server.character.sx + 600 - 50:
            game_world.remove_object(self)
        if self.y < 50 + server.character.sy - 360:
            game_world.remove_object(self)
        if self.y > server.character.sy + 360 - 50:
            game_world.remove_object(self)


    def handle_collision(self, group, other):
        match group:
            case 'M1:sword1':
                game_world.remove_object(self)
            case 'M2:sword1':
                game_world.remove_object(self)
            case 'M3:sword1':
                game_world.remove_object(self)
            case 'M4:sword1':
                game_world.remove_object(self)
            case 'M5:sword1':
                game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

class Sword2:
    image = None
    def __init__(self, sx=100000, sy=100000, speed=3, level = 0):
        if Sword2.image == None:
            Sword2.image = load_image("./png/weapon/Sword-2-05.png")
        self.sx, self.sy = sx,sy
        self.sword2_pos = [
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
        ]

        self.sword2_speed = 3

        self.sword2_angle1 = -89.5
        self.sword2_angle2 = -89.5/2
        self.sword2_angle3 = -89.5-89.5/2
        self.sword2_angle4 = 89.5
        self.sword2_angle5 = 89.5/2
        self.sword2_angle6 = 89.5*3/2
        self.sword2_angle7 = 0
        self.sword2_angle8 = 0

        self.sword2_angle =[
        -89.5,
        89.5,  # left
        0,  # up
        0,   # down
        -89.5 / 2,# RunRightUp
        89.5 / 2,   # Runleftup
        -89.5 - 89.5 / 2, # RunRightdown
        89.5 * 3 / 2 # Runleftdown
        ]

        self.image_w = 40
        self.image_h = 40

        self.dir = 0

        self.level = level

        self. life_time = 5
    def draw(self):
        # /1 right 2 3 /4 left /5 6 /7 up /8 down

        for i in range(0, self.level):
            if i == 0:
                self.image.composite_draw(self.sword2_angle[i], ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            elif i == 1:# left
                self.image.composite_draw(self.sword2_angle[i], ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            elif i == 2:# up
                self.image.composite_draw(self.sword2_angle[i], ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            elif i == 3:# down
                self.image.composite_draw(self.sword2_angle[i], 'v', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            elif i == 4:# RunRightUp
                self.image.composite_draw(self.sword2_angle[i], ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            elif i == 5:# Runleftup
                self.image.composite_draw(self.sword2_angle[i], ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            elif i == 6:# RunRightdown
                self.image.composite_draw(self.sword2_angle[i], ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            elif i == 7:# Runleftdown
                self.image.composite_draw(self.sword2_angle[i], ' ', self.sword2_pos[i][0], self.sword2_pos[i][1], self.image_w, self.image_h)
            self.sx, self.sy = self.sword2_pos[i][0], self.sword2_pos[i][1]



    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        # 방향에 따라
        for i in range(0, self.level):
            if i == 0:
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0] + self.sword2_speed * 300 * game_framework.frame_time,
                    self.sword2_pos[i][1])
                self.sword2_angle[i] -= 0.5

            elif i == 1:
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0] - self.sword2_speed * 300 * game_framework.frame_time,
                    self.sword2_pos[i][1])
                self.sword2_angle[i] -= 0.5
            elif i == 2:
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0],
                    self.sword2_pos[i][1] + self.sword2_speed * 300 * game_framework.frame_time)
                self.sword2_angle[i] -= 0.5
            elif i == 3:
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0],
                    self.sword2_pos[i][1] - self.sword2_speed * 300 * game_framework.frame_time)
                self.sword2_angle[i] -= 0.5
            elif i == 4: #RunRightUp
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0] + self.sword2_speed * 300 * game_framework.frame_time,
                    self.sword2_pos[i][1] + self.sword2_speed * 300 * game_framework.frame_time)
                self.sword2_angle[i] -= 0.5

            elif i == 5:  # RunLeftup
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0] - self.sword2_speed * 300 * game_framework.frame_time,
                    self.sword2_pos[i][1] + self.sword2_speed * 300 * game_framework.frame_time)
                self.sword2_angle[i] -= 0.5

            elif i == 6: #RunRightdown
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0] + self.sword2_speed * 300 * game_framework.frame_time,
                    self.sword2_pos[i][1] - self.sword2_speed * 300 * game_framework.frame_time)
                self.sword2_angle[i] -= 0.5

            elif i == 7: ##RunLeftDown
                self.sword2_pos[i] = (
                    self.sword2_pos[i][0] - self.sword2_speed * 300 * game_framework.frame_time,
                    self.sword2_pos[i][1] - self.sword2_speed * 300 * game_framework.frame_time)
                self.sword2_angle[i] -= 0.5

            self.sx, self.sy = self.sword2_pos[i][0], self.sword2_pos[i][1]

            if self.life_time > 1:
                if self.sword2_pos[i][0] < 50 + server.character.sx - 1000:
                    game_world.remove_object(self)
                if self.sword2_pos[i][0] > server.character.sx + 1000 - 50:
                    game_world.remove_object(self)
                if self.sword2_pos[i][1] < 50 + server.character.sy - 1000:
                    game_world.remove_object(self)
                if self.sword2_pos[i][1] > server.character.sy + 1000 - 50:
                    game_world.remove_object(self)


    def handle_collision(self, group, other):
        match group:
            case 'M1:sword2':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M2:sword2':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M3:sword2':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M4:sword2':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M5:sword2':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)

    def get_bb(self):
        return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10

class Axe:
    axe_image = None
    def __init__ (
            self,
            sx=100000,
            sy=100000,
            level=0):
        if self.axe_image == None:
            self.axe_image = load_image("./png/weapon/axe-03.png")

        self.sx, self.sy = sx, sy

        self.axe_pos = [
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy)
        ]
        self.axe_angle =[
            0,      # 1
            0,      # 2
            0,      # 3
            0      # 4
        ]
        self.axe_x_speed = [
            0.3,
            0.3,
            0.5,
            0.5
        ]
        self.axe_y_speed = [
            1.5,
            1.5,
            1.8,
            1.8
        ]
        self.axe_x_gravity = [
            0.1,
            0.1,
            1.5,
            1.5
        ]
        self.axe_y_gravity = [
            0.01,
            0.01,
            0.01,
            0.01
        ]
        self.axe_level = level


        self.image_w = 60
        self.image_h = 60

        self.dir = 0

        self.level = level

        self.life_time = 10

    def draw(self):
        # /1 right 2 3 /4 left /5 6 /7 up /8 down

        for i in range(0, self.axe_level):
            if i == 0:
                self.axe_image.composite_draw(self.axe_angle[i], ' ', self.axe_pos[i][0],
                                              self.axe_pos[i][1], self.image_w, self.image_h)
            elif i == 1:# left
                self.axe_image.composite_draw(self.axe_angle[i], 'h', self.axe_pos[i][0],
                                              self.axe_pos[i][1], self.image_w, self.image_h)
            elif i == 2:# up
                self.axe_image.composite_draw(self.axe_angle[i], '', self.axe_pos[i][0],
                                              self.axe_pos[i][1], self.image_w, self.image_h)
            elif i == 3:# down
                self.axe_image.composite_draw(self.axe_angle[i], 'h', self.axe_pos[i][0],
                                              self.axe_pos[i][1], self.image_w, self.image_h)

            self.sx, self.sy = self.axe_pos[i][0], self.axe_pos[i][1]


    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        # 방향에 따라

        for i in range(0, self.axe_level):
            if i == 0:
                self.axe_pos[i] = (
                    self.axe_pos[i][0] + self.axe_x_speed[i] * 300 * game_framework.frame_time,
                    self.axe_pos[i][1] + self.axe_y_speed[i] * 300 * game_framework.frame_time)
                self.axe_angle[i] -= 0.01 * 300 * game_framework.frame_time

            elif i == 1:
                self.axe_pos[i] = (
                    self.axe_pos[i][0] - self.axe_x_speed[i] * 300 * game_framework.frame_time,
                    self.axe_pos[i][1] + self.axe_y_speed[i] * 300 * game_framework.frame_time)
                self.axe_angle[i] += 0.01 * 300 * game_framework.frame_time
            elif i == 2:
                self.axe_pos[i] = (
                    self.axe_pos[i][0] + self.axe_x_speed[i] * 300 * game_framework.frame_time,
                    self.axe_pos[i][1] + self.axe_y_speed[i] * 300 * game_framework.frame_time)
                self.axe_angle[i] -= 0.01 * 300 * game_framework.frame_time
            elif i == 3:
                self.axe_pos[i] = (
                    self.axe_pos[i][0] - self.axe_x_speed[i] * 300 * game_framework.frame_time,
                    self.axe_pos[i][1] + self.axe_y_speed[i] * 300 * game_framework.frame_time)
                self.axe_angle[i] += 0.01 * 300 * game_framework.frame_time

            if i < 2:
                if self.axe_x_speed[i] <= 0.2:
                    self.axe_x_speed[i] = 0.2
                    self.axe_x_gravity[i] = 0
                else:
                    self.axe_x_speed[i] -= self.axe_x_gravity[i]
                self.axe_y_speed[i] -= self.axe_y_gravity[i] * 300 * game_framework.frame_time


            if i > 1:
                if self.axe_x_speed[i] <= 0.3:
                    self.axe_x_speed[i] = 0.3
                    self.axe_x_gravity[i] = 0
                else:
                    self.axe_x_speed[i] -= self.axe_x_gravity[i]
                self.axe_y_speed[i] -= self.axe_y_gravity[i] * 300 * game_framework.frame_time


            if self.life_time > 1:
                if self.axe_pos[i][0] < 50 + server.character.sx - 1000:
                    game_world.remove_object(self)
                if self.axe_pos[i][0] > server.character.sx + 1000 - 50:
                    game_world.remove_object(self)
                if self.axe_pos[i][1] < 50 + server.character.sy - 1000:
                    game_world.remove_object(self)
                if self.axe_pos[i][1] > server.character.sy + 1000 - 50:
                    game_world.remove_object(self)


    def handle_collision(self, group, other):
        match group:
            case 'M1:axe':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M2:axe':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M3:axe':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M4:axe':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)
            case 'M5:axe':
                self.life_time -= 1
                if self.life_time <= 0:
                    game_world.remove_object(self)

    def get_bb(self):
        return self.sx - 30, self.sy - 30, self.sx + 30, self.sy + 30
    def get_bb_axe(self, i):
        return self.sx - 30, self.sy - 30, self.sx + 30, self.sy + 30

class Shield:
    shield_image = None
    def __init__ (
            self,
            sx=100000,
            sy=100000,
            level=4):
        if self.shield_image == None:
            self.shield_image = load_image("./png/weapon/shield-05.png")

        self.sx, self.sy = sx, sy

        self.shield_pos = [
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy),
            (self.sx, self.sy)
        ]
        self.shield_angle =[
            0,      # 1
            0,      # 2
            0,      # 3
            0,      # 4
            0,      # 5
            0      # 6
        ]
        self.shield_x_speed = [
            0.3,
            0.3,
            0.5,
            0.5,
            0.5,
            0.5
        ]
        self.shield_y_speed = [
            1.5,
            1.5,
            1.8,
            1.8,
            1.8,
            1.8
        ]
        self.shield_radius = 100

        self.shield_level = level
        self.image_w = 40
        self.image_h = 40

        for i in range(0, 4):
            self.shield_angle[i] = 360/self.shield_level* i
            self.shield_pos[i] = (
                self.sx + 100 * math.sin(math.radians(self.shield_angle[i])),
                self.sy + 100 * math.sin(math.radians(self.shield_angle[i]))
            )
    def draw(self):
        # /1 right 2 3 /4 left /5 6 /7 up /8 down

        for i in range(0, 4):
            self.shield_image.composite_draw(0, ' ', self.shield_pos[i][0], self.shield_pos[i][1], 40, 40)
            self.sx, self.sy = self.shield_pos[i][0], self.shield_pos[i][1]


    def update(self):
        for i in range(0, self.shield_level):
            self.shield_angle[i] += 0.5 / self.shield_level * 250 * game_framework.frame_time
            if self.shield_angle[i] + (360 / self.shield_level) >= 360:
                self.shield_angle[i] -= 360

            # 원운동 업데이트
            self.shield_pos[i] = (
                self.sx + 100 * math.cos(math.radians(self.shield_angle[i])),
                self.sy + 100 * math.sin(math.radians(self.shield_angle[i]))
            )
        # for i in range(0, self.shield_level):
        #     self.shield_angle[i] = 360 / self.shield_level * i
        #     self.shield_pos[i] = (
        #         self.sx + 100 * math.sin(math.radians(self.shield_angle[i])),
        #         self.sy + 100 * math.sin(math.radians(self.shield_angle[i]))
        #     )

        # 플레이어의 좌표를 중점으로 원운동
        #self.shield_x = self.sx + 100 * math.cos(math.radians(self.shield_angle + (360 / self.shield_level) * i))
        #self.shield_y = self.sy + 100 * math.sin(math.radians(self.shield_angle + (360 / self.shield_level) * i))



        # for i in range(0, self.shield_level):
        #     self.shield_angle[i] += 0.5 / self.shield_level * 250 * game_framework.frame_time
        #     if self.shield_angle[i] + (360/(i+1)) >= 360:
        #         self.shield_angle[i] -= 360
        #
        #     if i == 0:
        #         self.shield_pos[i] = (
        #             self.shield_pos[i][0] + 100 * math.cos(math.radians(self.shield_angle[i] + (360 / self.shield_level) * i)),
        #             self.shield_pos[i][1] + 100 * math.sin(math.radians(self.shield_angle[i] + (360 / self.shield_level) * i))
        #         )
        #
        #
        #     elif i == 1:
        #         self.shield_pos[i] = (
        #             self.shield_pos[i][0] + 100 * math.cos(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i)),
        #             self.shield_pos[i][1] + 100 * math.sin(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i))
        #         )
        #     elif i == 2:
        #         self.shield_pos[i] = (
        #             self.shield_pos[i][0] + 100 * math.cos(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i)),
        #             self.shield_pos[i][1] + 100 * math.sin(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i))
        #         )
        #     elif i == 3:
        #         self.shield_pos[i] = (
        #             self.shield_pos[i][0] + 100 * math.cos(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i)),
        #             self.shield_pos[i][1] + 100 * math.sin(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i))
        #         )
        #     elif i == 4:
        #         self.shield_pos[i] = (
        #             self.shield_pos[i][0] + 100 * math.cos(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i)),
        #             self.shield_pos[i][1] + 100 * math.sin(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i))
        #         )
        #     elif i == 5:
        #         self.shield_pos[i] = (
        #             self.shield_pos[i][0] + 100 * math.cos(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i)),
        #             self.shield_pos[i][1] + 100 * math.sin(
        #                 math.radians(self.shield_angle[i] + (360 / self.shield_level) * i))
        #         )

    def handle_collision(self, group, other):
        pass
        # match group:
        #     case 'M1:sword2':
        #         self.life_time -= 1
        #         if self.life_time <= 0:
        #             game_world.remove_object(self)
        #     case 'M2:sword2':
        #         self.life_time -= 1
        #         if self.life_time <= 0:
        #             game_world.remove_object(self)
        #     case 'M3:sword2':
        #         self.life_time -= 1
        #         if self.life_time <= 0:
        #             game_world.remove_object(self)
        #     case 'M4:sword2':
        #         self.life_time -= 1
        #         if self.life_time <= 0:
        #             game_world.remove_object(self)
        #     case 'M5:sword2':
        #         self.life_time -= 1
        #         if self.life_time <= 0:
        #             game_world.remove_object(self)

    def get_bb(self):
        return self.sx - 30, self.sy - 30, self.sx + 30, self.sy + 30
