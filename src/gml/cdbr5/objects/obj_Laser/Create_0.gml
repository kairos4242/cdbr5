
event_inherited()



function LaserSegment(_start_x, _start_y, _end_x, _end_y, _length, _search_direction, _bounce_type) constructor
{
	start_x = _start_x
	start_y = _start_y
	end_x = _end_x
	end_y = _end_y
	length = _length
	search_direction = _search_direction
	bounce_type = _bounce_type //horizontal or vertical, determines what direction the next segment should go
}

lifetime = 150
damage = 50

segment_list = []
hits_struct = {}
hit_cooldown = 30

enum BOUNCE_TYPE {
	HORIZONTAL,
	VERTICAL,
	NO_BOUNCE
}

owner = -1
num_bounces = 3
collide = false