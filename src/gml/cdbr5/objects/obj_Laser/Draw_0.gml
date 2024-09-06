/*



// first laser beam
for (var j = 0; j < length_laser; j++ )  {
	//var flicker = random_range(0.6,1.4); // change to make diffrent flicker, or delete flicker and set y_scale back to 1
	var flicker = 1
	// variables set in create to ajust to need!
	draw_sprite_ext(whatImage, 5, x + lengthdir_x(j, direction), y + lengthdir_y(j, direction), 1, flicker, direction,c_white, 1 ); 

                                     }
									 
for (var j2 = 0; j2 < length_laser2; j2++ )  {
	//var flicker2 = random_range(0.6,1.4); // change to make diffrent flicker, or delete flicker and set y_scale back to 1
	var flicker2 = 1
	// variables set in create to ajust to need!
	draw_sprite_ext(whatImage, 1, xEnd + lengthdir_x(j2, direction2), yEnd + lengthdir_y(j2, direction2), 1, flicker2, direction2,c_white, 1 ); 

                                    }									 
  								 
								 
for (var j3 = 0; j3 < length_laser3; j3++ )  {
	//var flicker3 = random_range(0.6,1.4); // change to make diffrent flicker, or delete flicker and set y_scale back to 1
	var flicker3 = 1
	// variables set in create to ajust to need!
	draw_sprite_ext(whatImage, 2, xEnd2 + lengthdir_x(j3, direction3), yEnd2 + lengthdir_y(j3, direction3), 1, flicker3, direction3,c_white, 1 ); 

       	                              }										 
	 		
		
		
		draw_text_color(x,y-140, what_Bounce2, c_red, c_red,c_red,c_red, 1);		
		draw_text_color(x,y-90, direction2, c_red, c_red,c_red,c_red, 1);
		draw_text_color(x,y-60, direction, c_red, c_red,c_red,c_red, 1);		

			//draw_text(x,y-90, xEnd2);			
									 
							 
									 
*/
draw_line(x,y, xEnd, yEnd);  
draw_line_color(xEnd, yEnd, xEnd2, yEnd2, c_red, c_red );
draw_line_color(xEnd2, yEnd2, xEnd3, yEnd3, c_purple, c_purple );



