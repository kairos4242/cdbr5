/// @description Insert description here
// You can write your code in this editor
explode_count--
if explode_count == 0 {
	//do area damage
	deal_area_damage(x, y, DAMAGE_SHAPE.CIRCLE, 64, 100)
	//destroy self
	instance_destroy()
}
show_debug_message(speed_x)
move_tangible(speed_x, speed_y)
apply_friction()