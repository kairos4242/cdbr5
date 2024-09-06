
// grab start position and direction/angle
x = owner.x;
y = owner.y;

direction = point_direction(owner.x, owner.y, mouse_x, mouse_y ); 


 #region // define how long the laser can get max plus when hitting something
var max_length = 900;  // change if camera is bigger or smaller then 900
for (var i = 0; i < max_length; i++ ) {

   xEnd = x + lengthdir_x(i, direction);
   yEnd = y + lengthdir_y(i, direction);
   
   length_laser = i;   // how long the laser is in the end
   
   var collision = collision_point(xEnd, yEnd, obj_Wall, 0, 0) 
   if collision {
	   var collision_angle = point_direction(xEnd, yEnd, collision.x, collision.y)
	   var side = "none"
		if (collision_angle <= 45 or collision_angle > 315) side = "right"
		if (collision_angle > 45 and collision_angle <= 135) side = "top"
		if (collision_angle > 135 and collision_angle <= 225) side = "left"
		if (collision_angle > 225 and collision_angle <= 315) side = "bottom"
		if side == "top" or side == "bottom" {
			what_Bounce2 = "horizontal";
			break;
		}
		else if side == "left" or side == "right" {
			what_Bounce2 = "vertical";
			break;
		}
   }
}
  // end of for loop
#endregion

 #region // 2nd laser branch

  // bounce off vertical walls
 if (what_Bounce2 == "vertical") { direction2 = (direction  *-1) + 180 }
 
  // bounce off horizontal walls
 if (what_Bounce2 == "horizontal") { direction2 =  direction  *-1;  }
 
 
var max_length2 = 900;  // change if camera is bigger or smaller then 900
for (var i2 = 0; i2 < max_length2; i2++ ) {

   xEnd2 = xEnd + lengthdir_x(i2 + buffer, direction2);
   yEnd2 = yEnd + lengthdir_y(i2 + buffer, direction2);
   
   length_laser2 = i2;   // how long the laser is in the end
   
   // breaking point change here object to break to or add multiple breaking points
    var collision = collision_point(xEnd2, yEnd2, obj_Wall, 0, 0) 
   if collision {
	   var collision_angle = point_direction(xEnd2, yEnd2, collision.x, collision.y)
	   var side = "none"
		if (collision_angle <= 45 or collision_angle > 315) side = "right"
		if (collision_angle > 45 and collision_angle <= 135) side = "top"
		if (collision_angle > 135 and collision_angle <= 225) side = "left"
		if (collision_angle > 225 and collision_angle <= 315) side = "bottom"
		if side == "top" or side == "bottom" {
			what_Bounce3 = "horizontal";
			break;
		}
		else if side == "left" or side == "right" {
			what_Bounce3 = "vertical";
			break;
		}
   }
}  // end of for loop
#endregion

#region // 3nd laser branch
 
 
  // bounce off vertical walls
 if (what_Bounce3 == "vertical")  {  direction3 = (direction2  *-1) + 180  }

  // bounce off horizontal walls
 if (what_Bounce3 == "horizontal") { direction3 =  direction2  *-1; }
 
 
var max_length3 = 900;  // change if camera is bigger or smaller then 900
for (var i3 = 8; i3 < max_length3; i3++ ) {

   xEnd3 = xEnd2 + lengthdir_x(i3, direction3);
   yEnd3 = yEnd2 + lengthdir_y(i3, direction3);
   
   length_laser3 = i3;   // how long the laser is in the end
   

     // breaking point change here object to break to or add multiple breaking points
   var collision = collision_point(xEnd3, yEnd3, obj_Wall, 0, 0) 
   if collision {
	   var collision_angle = point_direction(xEnd3, xEnd3, collision.x, collision.y)
	   var side = "none"
		if (collision_angle <= 45 or collision_angle > 315) side = "right"
		if (collision_angle > 45 and collision_angle <= 135) side = "top"
		if (collision_angle > 135 and collision_angle <= 225) side = "left"
		if (collision_angle > 225 and collision_angle <= 315) side = "bottom"
		if side == "top" or side == "bottom" {
			what_Bounce3 = "horizontal";
			break;
		}
		else if side == "left" or side == "right" {
			what_Bounce3 = "vertical";
			break;
		}
   }
}  // end of for loop





#endregion



#region    collision  -> with global enemy to change its values (hp or something) 
 /*
 if (instance_exists(o_Enemy)) {
 
      // add
	  if (refresh_hit == true) { refresh_hit = false;
	  
      var _list = ds_list_create();
	  var hits = collision_line_list(x,y, xEnd, yEnd, o_Enemy, 0,0, _list,0 );
	  
	     if (hits > 0 ) {
		 
		       for (var k = 0; k < hits; ++k;) {
			       
				   _list[| k].hp = _list[| k].hp -1;
			   
			   }
		 } 
     ds_list_destroy(_list);
 
     } // end of refresh check
 }  // end of enemy exist check 
 
 
 
 
 //Memory save , "switch"
 if (refresh_hit == false) {
  refresh_hit_timer--;
  if (refresh_hit_timer <= 0) {   refresh_hit_timer = refresh_hit_time; refresh_hit = true;   }
 
                             } 
 
 */
 
#endregion