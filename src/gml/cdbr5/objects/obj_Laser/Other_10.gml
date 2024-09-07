/// @description Insert description here
// You can write your code in this editor

//check expired
lifetime--
if lifetime <= 0 instance_destroy()

//shouldnt deal damage to targets every frame so check which targets we havent damaged recently
var targets_hit = struct_get_names(hits_struct)
for (var i = 0; i < array_length(targets_hit); i++) {
	var current_target = targets_hit[i]
	var current_target_cooldown = struct_get(hits_struct, current_target)
	if current_target_cooldown <= 0 {
		//we can hit the target again, remove them from the struct
		struct_remove(hits_struct, current_target)
	}
	else {
		//decrement the cooldown
		current_target_cooldown -= 1
		struct_set(hits_struct, current_target, current_target_cooldown)
	}
}

// grab start position and direction/angle
x = owner.x;
y = owner.y;
segment_list = []
direction = point_direction(owner.x, owner.y, mouse_x, mouse_y ); 
var current_segment = new LaserSegment(x, y, x, y, 0, direction, BOUNCE_TYPE.NO_BOUNCE);
var max_length = 900;  // change if camera is bigger or smaller then 900

for (var i = 0; i < num_bounces; i++) {
	var current_start_x = current_segment.start_x
	var current_start_y = current_segment.start_y
	var current_end_x = current_start_x
	var current_end_y = current_start_y
	var current_length = 0
	var current_bounce_type = BOUNCE_TYPE.NO_BOUNCE
	for (var j = 1; j < max_length; j++) {
		current_end_x = current_start_x + lengthdir_x(j, current_segment.search_direction)
		current_end_y = current_start_y + lengthdir_y(j, current_segment.search_direction)
		current_length = j
		var collision = collision_point(current_end_x, current_end_y, obj_Wall, 0, 0)
		if collision {
			var collision_angle = point_direction(current_end_x, current_end_y, collision.x, collision.y)
			var side = "none"
			if (collision_angle <= 45 or collision_angle > 315) side = "right"
			if (collision_angle > 45 and collision_angle <= 135) side = "top"
			if (collision_angle > 135 and collision_angle <= 225) side = "left"
			if (collision_angle > 225 and collision_angle <= 315) side = "bottom"
			if side == "top" or side == "bottom" {
				current_bounce_type = BOUNCE_TYPE.HORIZONTAL;
				break;
			}
			else if side == "left" or side == "right" {
				current_bounce_type = BOUNCE_TYPE.VERTICAL;
				break;
			}
		}
	}
	//this all might be unnecessarily verbose, thought it was computationally cheaper instead of modifying struct
	current_segment.end_x = current_end_x
	current_segment.end_y = current_end_y
	current_segment.length = current_length
	current_segment.bounce_type = current_bounce_type
	array_push(segment_list, current_segment)
	var next_search_direction = -1
	if (current_bounce_type == BOUNCE_TYPE.VERTICAL) { next_search_direction = (current_segment.search_direction  *-1) + 180 }
	else if (current_bounce_type == BOUNCE_TYPE.HORIZONTAL) {next_search_direction =  current_segment.search_direction  *-1;}
	else if (current_bounce_type == BOUNCE_TYPE.NO_BOUNCE) {break;}//we didn't collide with anything so we shouldn't add another segment
	current_segment = new LaserSegment(current_end_x, current_end_y, current_end_x, current_end_y, 0, next_search_direction, BOUNCE_TYPE.NO_BOUNCE)
}


//damage
for (var i = 0; i < array_length(segment_list); i++) {
	var hitcheck_segment = segment_list[i]
	var hit_candidates = ds_list_create()
	var num_hit_candidates = collision_line_list(hitcheck_segment.start_x,hitcheck_segment.start_y, hitcheck_segment.end_x, hitcheck_segment.end_y, obj_GameObject, 0,true,hit_candidates,0 );
	if num_hit_candidates > 0 {
		for (var j = 0; j < num_hit_candidates; j++) {
			var hit_candidate = hit_candidates[| j]
			if (hit_candidate != owner) and (!struct_exists(hits_struct, hit_candidate)) {
				struct_set(hits_struct, hit_candidate, hit_cooldown)
				deal_damage(damage, hit_candidate)
			}
		}
	}
}