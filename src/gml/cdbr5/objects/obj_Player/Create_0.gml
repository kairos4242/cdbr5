/// @description Insert description here
// You can write your code in this editor

event_inherited()

name = "Anonymous"

outside_force_x = 0
outside_force_y = 0

key_up = ord("W")
key_down = ord("S")
key_left = ord("A")
key_right = ord("D")

key_shoot = vk_space
key_shoot_alt = mb_right

x_dir = 0
y_dir = 0
speed_x = 0
speed_y = 0
acceleration = 0.2
ground_friction = 0.15


movespeed = 5
reload_time = 60

key_right_pressed = false
key_left_pressed = false
key_down_pressed = false
key_up_pressed = false
key_shoot_pressed = false
key_shoot_alt_pressed = false

control_type = CONTROL_TYPE.UNCONTROLLED

powers[0] = new Power("Cross Cannon", "", 30, pointer_null, asset_get_index("pwr_cross_cannon_on_use"), pointer_null)