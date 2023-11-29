from pico2d import load_image

class Item_Select:
    def __init__(self):
        self.image = load_image('./png/gui/Shop_screen.png')

    def draw(self):
        self.image.composite_draw(0, ' ', 300, 300, 400, 600)

    def update(self):
        pass