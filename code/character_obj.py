from pico2d import *
import game_world
import game_framework
import math

class BaseGauge:
    image = None
    def __init__(self):
        if BaseGauge.image == None:
            BaseGauge.image = load_image('./png/gui/base_gauge2.png')
        self.w, self.h = 1250, 40

    def draw(self):
        self.image.composite_draw(0, ' ', 15 + self.w // 2, 710, self.w, 15)

    def update(self):
        pass

class Exp:
    image = None
    def __init__(self, c_exp):
        if Exp.image == None:
            Exp.image = load_image('./png/gui/exp_gauge2.png')
        self.exp = 0
        self.w, self.h = 0, 40
    def draw(self):
        self.image.composite_draw(0, ' ', 20+self.w//2, 710, self.w, 10)
    def update(self):
        self.w = self.exp/100*1240
        pass

class HP:
    image = None
    def __init__(self, c_hp, c_x, c_y):
        if HP.image == None:
            HP.image = load_image('./png/gui/hp_gauge2.png')
        self.c_hp, self.x, self.y = 0, c_x, c_y+5
        self.w, self.h = 0, 40

    def draw(self):
        self.image.composite_draw(0, ' ', self.x, self.y, 100, 10)

    def update(self):
        pass