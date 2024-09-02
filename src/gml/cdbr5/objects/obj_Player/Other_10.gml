/// @description Insert description here
// You can write your code in this editor

var weapon = powers[0]
if weapon.cooldown > 0 weapon.cooldown--

if control_type = CONTROL_TYPE.PLAYER {
	key_right_pressed = keyboard_check(key_right)
	key_left_pressed = keyboard_check(key_left)
	key_down_pressed = keyboard_check(key_down)
	key_up_pressed = keyboard_check(key_up)
	key_shoot_pressed = keyboard_check_pressed(key_shoot)
	key_shoot_alt_pressed = mouse_check_button_pressed(key_shoot_alt)
}

// don't allow movement if we're being acted on by an outside force
if outside_force_x == 0 and outside_force_y == 0 {
	x_dir = key_right_pressed - key_left_pressed
	y_dir = key_down_pressed - key_up_pressed
	move_tangible(x_dir * movespeed, y_dir * movespeed)
}
else {
	move_tangible(outside_force_x, outside_force_y)
}

//shooting
if key_shoot_pressed or key_shoot_alt_pressed {
	if weapon.cooldown <= 0 {
		script_execute(powers[0].on_use_function)
		weapon.cooldown = weapon.max_cooldown
	}
}