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
// TODO should go off spawn markers or something instead of being hardcoded
player1 = instance_create_layer(805, 425, "Instances", obj_Player)
with player1 {
	control_type = other.p1_control_type
	name = "Player 1"
}
player2 = instance_create_layer(885, 425, "Instances", obj_Player)
with player2 {
	control_type = other.p2_control_type
	name = "Player 2"
}

//if control type is http instead set the http requests going
control_dir = "left"
if p2_control_type = CONTROL_TYPE.HTTP {
	//set an alarm for 1 second before requests start to ensure initialization is complete
alarm[0] = 60
}