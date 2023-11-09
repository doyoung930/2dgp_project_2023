from pico2d import *


class DungeonMap:
    def __init__(self):
        #self.image = load_image("./map/dungeon/png/dungeon.png")
        self.image = load_image("dungeon.png")

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        # self.image.draw(1200, 30)
