/// @description Insert description here
// You can write your code in this editor

//TODO fix this up to be a function
if control_type = CONTROL_TYPE.PLAYER {
	var trigger_step = function(_element, _index)
	{
		with _element {
			event_perform(ev_other, ev_user0)
		}
	}

	array_foreach(global.object_registry, trigger_step);
}
else if control_type = CONTROL_TYPE.GML_AI {
	// AI script goes here
}