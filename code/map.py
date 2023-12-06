from pico2d import *

import server

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
        self.window_left = clamp(0, int(server.character.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.character.y) - self.ch // 2, self.h - self.ch - 1)
        pass

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left+100, self.window_bottom+100, self.cw, self.ch, 0, 0)

        #self.image.draw(400 - self.map_x, 30 - self.map_y)