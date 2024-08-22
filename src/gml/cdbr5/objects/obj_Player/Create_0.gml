/// @description Insert description here
// You can write your code in this editor

event_inherited()

enum CONTROL_TYPE {
	PLAYER,
	HTTP,
	GML_AI,
	UNCONTROLLED
}

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


movespeed = 5
reload_time = 60

key_right_pressed = false
key_left_pressed = false
key_down_pressed = false
key_up_pressed = false

control_type = CONTROL_TYPE.UNCONTROLLED