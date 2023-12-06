from pico2d import open_canvas, delay, close_canvas
import game_framework

import title as start_mode
#import play_mode as start_mode


screen_width = 1280
screen_height = 720
open_canvas(screen_width, screen_height)
game_framework.run(start_mode)
close_canvas()

