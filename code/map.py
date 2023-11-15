from pico2d import *


class DungeonMap:
    def __init__(self):
        # self.image = load_image("./map/dungeon/png/dungeon.png")
        self.image = load_image("dungeon.png")
        self.map_x, self.map_y = 0, 0

    def update(self):
        pass

    def draw(self):
        self.image.draw(400 - self.map_x, 30 - self.map_y)