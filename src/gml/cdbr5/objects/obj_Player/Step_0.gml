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

//shooting
if keyboard_check_pressed(key_shoot) or keyboard_check_pressed(key_shoot_alt) {
	var projectile = instance_create_depth(x, y, -500, obj_BasicProjectile)
	with projectile {
		speed_x = x_dir * 10
		speed_y = y_dir * 10
		owner = other.id
	}
}