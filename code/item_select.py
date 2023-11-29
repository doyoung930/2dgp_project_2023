from pico2d import load_image


class Item_Select:
    def __init__(self):
        self.image = load_image('./png/gui/Shop_screen.png')
        self.image_up = load_image('./png/gui/Upgrade.png')

    def draw(self):
        self.image.composite_draw(0, ' ', 250, 340, 390, 550)
        self.image.composite_draw(0, ' ', 650, 340, 390, 550)
        self.image.composite_draw(0, ' ', 1050, 340, 390, 550)
        self.image_up.composite_draw(0, ' ', 645, 660, 400, 60)

    def update(self):
        pass
