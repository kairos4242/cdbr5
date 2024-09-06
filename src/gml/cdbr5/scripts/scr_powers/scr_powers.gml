// Script assets have changed for v2.3.0 see
// https://help.yoyogames.com/hc/en-us/articles/360005277377 for more information
function Power(
	_name, 
	_description, 
	_cooldown, 
	_on_acquire_function,
	_on_use_function,
	_on_remove_function
) constructor {
	name = _name;
	description = _description;
	max_cooldown = _cooldown;
	cooldown = 0;//always the case? maybe can use acquire function for the rare cases of no?
	on_acquire_function = _on_acquire_function;
	on_use_function = _on_use_function;
	on_remove_function = _on_remove_function;
}

enum EFFECT_TYPE {
	KNOCKBACK
}

function Effect(
	_name, 
	_duration, 
	_type
) constructor {
	name = _name;
	duration = _duration;
	type = _type;
}

function has_effect(_effect_list, _effect_type) {
	for (i = 0; i < array_length(_effect_list); i++) {
		if effect_list[i].type == _effect_type return true
	}
	return false
}

function pwr_cross_cannon_on_use() {
	for (i=0; i<4; i++) {
		var x_diff = lengthdir_x(50, i * 90)
		var y_diff = lengthdir_y(50, i * 90)
		var projectile = instance_create_depth(x + x_diff, y + y_diff, -500, obj_Projectile)
		with projectile {
			sprite_index = spr_CrossProjectile
			speed_x = x_diff / 5
			speed_y = y_diff / 5
			if speed_x == 0 and speed_y == 0 speed_x = 10
			owner = other.id
		}
	}	
}

function pwr_basic_gun_on_use() {
	var projectile = instance_create_depth(x, y, -500, obj_Projectile)
	with projectile {
		sprite_index = spr_BasicProjectile
		speed_x = other.x_dir * 10
		speed_y = other.y_dir * 10
		if speed_x == 0 and speed_y == 0 speed_x = 10
		owner = other.id
	}
}

function pwr_body_slam_on_use() {
	if x_dir != 0 {
		speed_x *= 2
	}
	if y_dir != 0 {
		speed_y *= 2
	}
	
	array_push(effect_list, new Effect("Body Slam Knockback", 60, EFFECT_TYPE.KNOCKBACK))
}

function pwr_laser_on_use() {
	var laser = instance_create_depth(x + (10 * sign(x_dir)), y + (10 * sign(y_dir)), -500, obj_Laser)
	with laser {
		owner = other.id
	}
}