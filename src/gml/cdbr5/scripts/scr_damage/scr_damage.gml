// Script assets have changed for v2.3.0 see
// https://help.yoyogames.com/hc/en-us/articles/360005277377 for more information
function deal_damage(amount, target){
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