// Script assets have changed for v2.3.0 see
// https://help.yoyogames.com/hc/en-us/articles/360005277377 for more information

// move but dont move into an object
function move_tangible(_xdist, _ydist){
	if not place_meeting_solid(x + _xdist, y + _ydist) {
		x += _xdist
		y += _ydist
	}
	else {
		while _xdist != 0 or _ydist != 0 {
			
			if place_meeting_solid(x + sign(_xdist), y) _xdist = 0
			else {
				x += sign(_xdist)
				_xdist -= sign(_xdist)
			}
			
			if place_meeting_solid(x, y + sign(_ydist)) _ydist = 0
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