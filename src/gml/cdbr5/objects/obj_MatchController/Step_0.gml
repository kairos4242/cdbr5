/// @description Insert description here
// You can write your code in this editor

//TODO fix this up to be a function
if timescale == TIMESCALE.REAL_TIME {
	var trigger_step = function(_element, _index)
	{
		try {
			with _element {
				event_perform(ev_other, ev_user0)
			}
		}
		catch (_exception) {
			// foreach here can sometimes access elements that don't exist if they're deleted in the same step
			show_debug_message("Failed to trigger step for object at index " + string(_index))
		}
	}

	array_foreach(global.object_registry, trigger_step);
}