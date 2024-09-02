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

function pwr_cross_cannon_on_use() {
	for (i=0; i<4; i++) {
		var x_diff = lengthdir_x(50, i * 90)
		var y_diff = lengthdir_y(50, i * 90)
		var projectile = instance_create_depth(x + x_diff, y + y_diff, -500, obj_Projectile)
		with projectile {
			sprite_index = spr_CrossProjectile
			speed_x = x_diff / 5
			speed_y = y_diff / 5
			owner = other.id
		}
	}	
}

function pwr_basic_gun_on_use() {
	var projectile = instance_create_depth(x, y, -500, obj_BasicProjectile)
	with projectile {
		speed_x = other.x_dir * 10
		speed_y = other.y_dir * 10
		owner = other.id
	}
}