from pico2d import *


class DungeonMap:
    def __init__(self):
        # self.image = load_image("./map/dungeon/png/dungeon.png")
        self.image = load_image("dungeon.png")
        self.map_x, self.map_y = 0, 0
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def update(self):
        pass

    def draw(self):
        self.image.draw(400 - self.map_x, 30 - self.map_y)