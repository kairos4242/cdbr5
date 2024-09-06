/// @description get HTTP result and perform a game step

var request_id = ds_map_find_value(async_load, "id")
var request_status = ds_map_find_value(async_load, "status")
var string_data = ds_map_find_value(async_load, "result")
show_debug_message("response received for request id " + string(request_id))
if request_status != 0 throw "request failed!"

//get power
if (request_id == get_powers_request) {
	power_list = json_parse(string_data)
	show_debug_message(power_list)
	//var power_index_chosen = irandom(array_length(power_list))
	var power_index_chosen = 3
	var power_chosen = power_list[power_index_chosen]
	show_debug_message(power_chosen)
	
	// TODO should go off spawn markers or something instead of being hardcoded
	player1 = instance_create_layer(805, 425, "Instances", obj_Player)
	with player1 {
		control_type = other.p1_control_type
		name = "Player 1"
		powers[0] = power_chosen
	}
	player2 = instance_create_layer(885, 425, "Instances", obj_Player)
	with player2 {
		control_type = other.p2_control_type
		name = "Player 2"
		powers[0] = power_chosen
	}

	//if control type is http instead set the http requests going
	control_dir = "left"
	if p2_control_type == CONTROL_TYPE.HTTP {
		//set an alarm for 1 second before requests start to ensure initialization is complete
		alarm[0] = 60
	}
	
}

//perform player action
if (request_id == player_action_request) {
	
	show_debug_message(string_data)

	var json = json_parse(string_data)
	show_debug_message(json.answer)
	if json.answer == "yes" control_dir = "left"
	else control_dir = "right"

	var trigger_step = function(_element, _index)
	{
		with _element {
			if object_index == obj_Player.object_index {
				if other.control_dir == "left" {
					key_left_pressed = true
					key_right_pressed = false
				}
				else if other.control_dir == "right" {
					key_left_pressed = false
					key_right_pressed = true
				}
			}
			event_perform(ev_other, ev_user0)
		}
	}

	array_foreach(global.object_registry, trigger_step);

	//keep going
	show_debug_message("request sent")
	http_get("https://yesno.wtf/api")
}

