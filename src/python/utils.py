import pygame
import math

def create_rect(x: int, y: int, width: int, height: int):
    return pygame.Rect((x - width // 2, y - height // 2, width, height))
    
def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

def snap_to_grid(value):
    return 64 * round(value/64)

def get_colour_name(colour):
    return str(colour).lstrip("Colours.")

def floor_int_bidirectional(value: float):
    # makes sure floats that tend towards zero don't overshoot zero and start going in the other direction
    if value < 1 and value > -1:
        return 0
    return value
    
def round_float_down_bidirectional(value: float):
    # like floor int bidirectional but doesn't only apply to values within the (-1, 1) range
    abs_val = abs(value)
    abs_floor = math.floor(abs_val)
    return math.copysign(abs_floor, value)