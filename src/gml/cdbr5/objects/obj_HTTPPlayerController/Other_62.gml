/// @description get HTTP result and perform a game step

var status = ds_map_find_value(async_load, "status")
if status != 0 throw "request failed!"

var string_data = ds_map_find_value(async_load, "result")
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