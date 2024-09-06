
xEnd = 0;     // breakpoints
yEnd = 0;
length_laser = 0; // total length used to determine and draw laser

#region 2nd laser  -> xEnd to xEnd2
xEnd2 = 0;     // breakpoints
yEnd2 = 0;
length_laser2 = 0; // total length used to determine and draw laser
direction2 = 0;
what_Bounce2 = "horizontal";
#endregion

#region 3nd laser  -> xEnd2 to xEnd3
xEnd3 = 0;     // breakpoints
yEnd3 = 0;
length_laser3 = 0; // total length used to determine and draw laser
direction3 = 0;
what_Bounce3 = "horizontal";
#endregion

buffer = 20;
// change here to change color and glow type
color = 1;  //  0 blue, 1 orange, 2 violet, 3 pink, 4 red, 5 green
whatImage  =  spr_Laser_Hard_glow_20px;  // spr_Laser_Hard_glow_38px   or   spr_Laser_Soft_glow_38px   or   spr_Laser_No_glow_38px


// change here to ajust to your needs for "refresh" rate of laser collision check
	// memory space saver, less checks per step
	refresh_hit = false;
	refresh_hit_time = 20;  // 3 times per second  
	refresh_hit_timer = refresh_hit_time;
	
	
// how many time to bounce
bounce = 3;	

testVar = "";

owner = -1
