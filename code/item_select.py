from pico2d import load_image


class Item_Select:
    def __init__(self):
        self.image = load_image('./png/gui/Shop_screen.png')
        self.image_up = load_image('./png/gui/Upgrade.png')
        self.image_sword1 = load_image("./png/weapon/Sword-02.png")
        self.image_sword2 =load_image("./png/weapon/Sword-2-05.png")
        self.image_axe = load_image("./png/weapon/axe-03.png")
    def draw(self):
        self.image.composite_draw(0, ' ', 250, 340, 390, 550)
        self.image_sword1.composite_draw(0, ' ', 250, 440, 200, 250)
        self.image.composite_draw(0, ' ', 650, 340, 390, 550)
        self.image_sword2.composite_draw(0, ' ', 650, 440, 200, 250)
        self.image.composite_draw(0, ' ', 1050, 340, 390, 550)
        self.image_axe.composite_draw(0, ' ', 1050, 440, 200, 250)


        self.image_up.composite_draw(0, ' ', 645, 660, 400, 60)

    def update(self):
        pass
