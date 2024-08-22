/// @description Insert description here
// You can write your code in this editor

control_type = CONTROL_TYPE.HTTP
// TODO should go off spawn markers or something instead of being hardcoded
player1 = instance_create_layer(805, 425, "Instances", obj_Player)
with player1 {
	control_type = other.control_type
}
//if control type is http instead set the http requests going
control_dir = "left"
if control_type = CONTROL_TYPE.HTTP {
	//set an alarm for 1 second to ensure initialization is complete
alarm[0] = 60
}