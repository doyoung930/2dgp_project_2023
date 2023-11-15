from pico2d import *
import game_world
import game_framework

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
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
    pass

# 검이 전방으로 날아감 ( 짧은 사거리 공격 속도 빠름)
class Sword:
    pass
# 검이 전방으로 하나 날아감 ( 긴 사거리 공격 속도 느림)
class Sword2:
    pass
# 도끼가 머리 위로 날아 갔다가 중력을 받으며 떨어짐
class Axe:
    pass
# 플레이어 이동속도 증가
class Shoes:
    pass

# 플레이어 체력 증가
class WarriorHat:
    pass

# 적에게 날아 가는 파이어 볼 발사
class FireBall:
    pass