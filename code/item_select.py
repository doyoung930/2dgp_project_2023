from pico2d import load_image

class item_select:
    def __init__(self):
        self.image = load_image('./png/gui/Shop_screen.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass