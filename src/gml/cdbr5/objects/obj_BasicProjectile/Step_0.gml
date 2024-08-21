/// @description Insert description here
// You can write your code in this editor

x += speed_x
y += speed_y
var collision = instance_place(x, y, obj_Solid)
if collision != noone and collision != owner {
	deal_damage(damage, collision)
	instance_destroy()
}

if x < 0 or x > room_width or y < 0 or y > room_height instance_destroy()