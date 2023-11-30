import game_framework
import game_world
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time
import pico2d


def init():
    global fire
    global title
    global skull

    running = True

    title = Title()
    fire = Fire()
    skull = Skull()
    web = Web()
    welly = Welly()
    screen = Screen()
    ch = Ch()

    game_world.add_object(title, 0)
    game_world.add_object(fire, 1)
    game_world.add_object(skull, 2)
    game_world.add_object(web, 2)
    game_world.add_object(welly, 3)
    game_world.add_object(screen, 2)
    game_world.add_object(ch, 3)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_SPACE:
                    game_framework.quit()
                case pico2d.SDLK_ESCAPE:
                    game_framework.quit()


def pause():
    pass


def resume():
    pass


class Title:
    def __init__(self):
        self.image = load_image('./png/gui/lobby.png')


    def update(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 4597, 2643, 0, ' ', 640, 360, 1300, 740)

class Fire:
    def __init__(self):
        self.image = load_image('./png/gui/fire.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 891, 990, 0, ' ',300,400, 189, 209)
        self.image.clip_composite_draw(0, 0, 891, 990, 0, ' ',1280 -300, 400, 189, 209)


class Skull:
    def __init__(self):
        self.image_skull2 = load_image('./png/gui/skull2.png')
        self.image_skull1 = load_image('./png/gui/skull1.png')

    def update(self):
        pass

    def draw(self):
        self.image_skull1.clip_composite_draw(0, 0, 891, 990, 0, ' ', 130, 70, 240, 150)
        self.image_skull2.clip_composite_draw(0, 0, 891, 990, 0, ' ', 1200, 100, 200, 120)

class Web:
    def __init__(self):
        self.image = load_image('./png/gui/dungeon-07.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 891, 990, 0, ' ', 1160, 720-120, 240, 240)

class Welly:
    def __init__(self):
        self.image = load_image('./png/gui/Welly.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 2729, 1353, 0, ' ', 640, 320, 270, 130)


class Screen:
    def __init__(self):
        self.image = load_image('./png/gui/Main screen-02.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 3638, 3299, 0, ' ', 640, 400, 360, 320)

class Ch:
    def __init__(self):
        self.image = load_image('./png/gui/Ch.png')

    def update(self):
        pass

    def draw(self):
        #self.image.clip_composite_draw(0, 4354//5, 3050, 4354, 0, ' ', 640, 466, 90, 129)
        self.image.composite_draw(0, ' ', 640, 466, 90, 129)