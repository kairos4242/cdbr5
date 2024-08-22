// Script assets have changed for v2.3.0 see
// https://help.yoyogames.com/hc/en-us/articles/360005277377 for more information

// registry is intended to be only for game objects
// to be consulted by the controllers every time an action is received and a game step should be performed
function add_to_global_obj_registry(_id){
	if !variable_global_exists("object_registry") {
		global.object_registry = []
	}
	array_push(global.object_registry, _id)
}

function remove_from_global_obj_registry(_id) {
	if !variable_global_exists("object_registry") {
		exit
	}
	array_delete(global.object_registry, array_get_index(global.object_registry, _id),1)
}