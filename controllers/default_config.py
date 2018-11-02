# -*- coding: utf-8 -*-

import os

version = '1.3'

working_directory = os.path.join(os.getcwd(), 'working_directory')
viewer_input_mode = 'pan' # pan, freehand, circle, contour
channel_colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'yellow': (255, 255, 0)
}