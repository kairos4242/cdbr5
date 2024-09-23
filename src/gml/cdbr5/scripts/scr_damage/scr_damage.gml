// Script assets have changed for v2.3.0 see
// https://help.yoyogames.com/hc/en-us/articles/360005277377 for more information

enum DAMAGE_SHAPE {
	CIRCLE//more to come
}
function deal_damage(amount, target) {
	if target.invulnerable exit
	if target.divine_shield {
		target.divine_shield = false
		exit
	}
	target.hp -= amount
	if target.hp <= 0 {
		with target instance_destroy()
	}
}

function deal_area_damage(origin_x, origin_y, shape, size, amount) {
	var targets = ds_list_create()
	if shape == DAMAGE_SHAPE.CIRCLE {
		collision_circle_list(origin_x, origin_y, size, obj_GameObject, false, false, targets, true)
		for (i=0; i < ds_list_size(targets); i++) {
			var target = ds_list_find_value(targets, i)
			deal_damage(amount, target)
		}
	}
}