/// @description Insert description here
// You can write your code in this editor

enum CONTROL_TYPE {
	PLAYER,
	HTTP,
	GML_AI,
	UNCONTROLLED
}
//whether a step should be performed every step or only when we get http input
enum TIMESCALE {
	REAL_TIME,
	ASYNC
}
// these are related (timescale should only be real time if no HTTP input)
// can we make them a single var somehow? Is that unnecessary simplification?

enum MATERIAL {
	NONE,
	WOOD,
	METAL,
	STONE,
	SAND,
	GLASS
}

timescale = TIMESCALE.REAL_TIME
p1_control_type = CONTROL_TYPE.PLAYER
p2_control_type = CONTROL_TYPE.GML_AI

//HTTP request vars for async_load
player_action_request = -4
get_powers_request = http_get("http://localhost:8080/api/v1/power")
show_debug_message("sending get power request with id " + string(get_powers_request))
get_player_request = -4
get_player_count_request = -4

power_list = []