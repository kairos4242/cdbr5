/// @description Insert description here
// You can write your code in this editor

enum CONTROL_TYPE {
	PLAYER,
	HTTP,
	GML_AI,
	UNCONTROLLED
}

control_type = CONTROL_TYPE.PLAYER
// TODO should go off spawn markers or something instead of being hardcoded
player1 = instance_create_layer(805, 425, "Instances", obj_Player)
with player1 {
	control_type = other.control_type
}
//if control type is http instead set the http requests going
control_dir = "left"
if control_type = CONTROL_TYPE.HTTP {
	//set an alarm for 1 second before requests start to ensure initialization is complete
alarm[0] = 60
}