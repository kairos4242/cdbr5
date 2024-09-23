// Script assets have changed for v2.3.0 see
// https://help.yoyogames.com/hc/en-us/articles/360005277377 for more information

// move but dont move into an object
function move_tangible(_xdist, _ydist){
	if not collide {
		x += _xdist
		y += _ydist
		return
	}
	if not place_meeting_solid(x + _xdist, y + _ydist) {
		x += _xdist
		y += _ydist
	}
	else {
		while floor(_xdist) != 0 or floor(_ydist) != 0 {
			
			if place_meeting_solid(x + sign(_xdist), y) {
				if has_effect(effect_list, EFFECT_TYPE.KNOCKBACK) {
					var target = instance_place(x + sign(_xdist), y, obj_GameObject)
					if abs(speed_x) > 1 {
						show_debug_message("bodyslam hit! targeting {0}", object_get_name(target.object_index))
						deal_damage(30, target)//prevents retriggering unless speed boost again
					}
					with target {
						speed_x = 10 * sign(_xdist)
					}
				}
				_xdist = 0
				speed_x = 0
				
			}
			else {
				x += sign(_xdist)
				_xdist -= sign(_xdist)
			}
			
			if place_meeting_solid(x, y + sign(_ydist)) {
				if has_effect(effect_list, EFFECT_TYPE.KNOCKBACK) {
					var target = instance_place(x, y + sign(_ydist), obj_GameObject)
					if abs(speed_y) > 1 {
						show_debug_message("bodyslam hit! targeting {0} {1}", object_get_name(target.object_index), target)
						deal_damage(30, target)
					}
					with target {
						speed_y = 10 * sign(_ydist)
					}
				}
				_ydist = 0
				speed_y = 0
			}
			else {
				y += sign(_ydist)
				_ydist -= sign(_ydist)
			}
		}
	}
}

// check for a collision with a solid object with the collide flag enabled
function place_meeting_solid(_x, _y) {
	var _collision = instance_place(_x, _y, obj_GameObject)
	if _collision == noone return false
	else return _collision.collide
}

function apply_friction() {
	if x_dir == 0 or abs(speed_x) > movespeed {
		if abs(speed_x) < ground_friction speed_x = 0
		else speed_x = speed_x - (ground_friction * sign(speed_x))
	}
	if y_dir == 0 or abs(speed_y) > movespeed {
		if abs(speed_y) < ground_friction speed_y = 0
		else speed_y = speed_y - (ground_friction * sign(speed_y))
	}
	if not (sign(x_dir) == sign(speed_x) and abs(speed_x) > movespeed) {
		speed_x += acceleration * x_dir
	}
	if not (sign(y_dir) == sign(speed_y) and abs(speed_y) > movespeed) {
		speed_y += acceleration * y_dir
	}
}