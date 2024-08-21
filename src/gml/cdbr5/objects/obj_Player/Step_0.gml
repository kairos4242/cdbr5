/// @description Insert description here
// You can write your code in this editor

// don't allow movement if we're being acted on by an outside force
if outside_force_x == 0 and outside_force_y == 0 {
	var x_dir = keyboard_check(key_right) - keyboard_check(key_left)
	var y_dir = keyboard_check(key_down) - keyboard_check(key_up)
	move_tangible(x_dir * movespeed, y_dir * movespeed)
}
else {
	move_tangible(outside_force_x, outside_force_y)
}