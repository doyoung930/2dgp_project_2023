from pico2d import *
import game_world
import game_framework
import math


class Ball:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

    # fill here


# 총 레벨업 5회까지 가능

# 캐릭터 주변을 빙빙 도는 실드
class Shield:
    image = None

    def __init__(self, shield_x, shield_y, velocity=1, radius=100, angular_velocity=10, angle = 0):
        if Shield.image == None:
            Shield.image = load_image("./png/weapon/shield-05.png")
        self.shield_x, self.shield_y, self.velocity = shield_x, shield_y, velocity
        self.radius = radius  # 원운동 반지름
        self.angular_velocity = angular_velocity  # 각속도
        self.angle = angle  # 각도 초기값
        self.image_w = 40
        self.image_h = 40

    def draw(self):
        self.image.composite_draw(0, ' ', self.shield_x, self.shield_y, self.image_w, self.image_h)

    def update(self):
        # 플레이어의 좌표를 중점으로 원운동
        self.angle += 10
        self.shield_x = self.shield_x + self.radius * math.cos(math.radians(self.angle))
        self.shield_y = self.shield_y + self.radius * math.sin(math.radians(self.angle))

        # 각도 업데이트
        #self.angle += self.angular_velocity * game_framework.frame_time * 20
        # 각도가 360도를 넘어가면 360도로 초기화
        if self.angle >= 360:
            self.angle -= 360

# 검이 전방으로 날아감 ( 짧은 사거리 공격 속도 빠름)
class Sword1:
    image = None

    def __init__(self, x=400, y=300, velocity=10, dir = 0, velocity2 = 10):
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
        #print(self.velocity * 100 * game_framework.frame_time)

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
        if self.y < 25 or self.y > 720 - 25:
            game_world.remove_object(self)
# 검이 전방으로 하나 날아감 ( 긴 사거리 공격 속도 느림)
class Sword2:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        if Sword2.image == None:
            Sword2.image = load_image("./png/weapon/Sword-2-03.png")
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        self.x += self.velocity * 100 * game_framework.frame_time


# 도끼가 머리 위로 날아 갔다가 중력을 받으며 떨어짐
class Axe:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        if Axe.image == None:
            Axe.image = load_image("./png/weapon/axe-03.png")
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        self.x += self.velocity * 100 * game_framework.frame_time


# 플레이어 이동속도 증가
class Shoes:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        if Shoes.image == None:
            Shoes.image = load_image("./png/weapon/uiBootsSpeed.png")
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        self.x += self.velocity * 100 * game_framework.frame_time


# 플레이어 체력 증가
class WarriorHat:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        if WarriorHat.image == None:
            WarriorHat.image = load_image("./png/weapon/prop-07.png")
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        self.x += self.velocity * 100 * game_framework.frame_time


# 적에게 날아 가는 파이어 볼 발사
class FireBall:
    images = None

    def __init__(self, x=400, y=300, velocity=1):
        if FireBall.images == None:
            FireBall.images = [load_image("./png/skill/skill1/0" + "%d" % i + ".png") for
                               i in range(0, 5)]
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.images.draw(self.x, self.y)

    def update(self):
        # 실드 움직임 플레이어를 중점으로 원을 그리며 돌아감
        self.x += self.velocity * 100 * game_framework.frame_time
