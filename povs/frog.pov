#include "colors.inc"

#macro eye(sign, rotAng)
    union {
        sphere { 
            0, 0.5 
            pigment { White }
        }
        disc { 
            <sign*0.3, 0.3, -0.3>, <sign*1,1,-1>, 0.1
            pigment { Black }
        }
        rotate rotAng
        translate <sign*0.5, 0.5, -0.5>  
    }
#end 
   
#macro face(leftEye,rightEye)
    
    eye(-1,leftEye)
    eye(1,rightEye)
    
    torus {
        0.3, 0.2   
        rotate 90*x
        translate <0,-0.2,-0.7>   
        
        pigment { Pink } 
    }
#end

#macro arm(sign)
    cylinder {
        -0.4*y, y, 0.3, 1
        rotate <20,sign*-20,0>
        translate <sign*0.8,-2,0>
    }
#end

#macro leg(sign)
    cylinder {
        -0.6*y, 1*y, 0.3, 1
        rotate <-45,-sign*45,0>
        translate <sign*1,-1,1.3>
    } 
    
    cylinder {
        -0.4*z, 1.6*z, 0.3, 1
        rotate 90*x 
        translate <sign*1.6,-0.9,0.75>
    } 
#end

#declare Frog = union {
    blob {
        threshold 0.1 
        
        //head
        sphere { 
            0, 1.1, 2
        } 
        
        //body
        sphere { 
            0, 1.5, 3
            translate <0,-1.5,1>
        }
        sphere { 
            0, 1, 0.5
            translate <0,-1.25,0.3> 
            pigment { White }
        }
        
        leg(-1)
        leg(1)
        
        arm(-1)
        arm(1)
        
        
        pigment { Green }
        normal { bumps 0.2 scale 0.5 }
    }
    
    face(-30*y,30*y)
} 




//display routine

background {Black}
// set viewer's position in the scene
camera {
  location <0,0,-11>
  direction 1.0*z
  right x*image_width/image_height
  look_at <0.0, 0.0, 0.0>
}

light_source {   
    <0, 0, -6>
    White
} 

object { Frog pigment { Grey } rotate clock*360*y }
plane { y, -2.7 pigment { checker Red Blue  } }

/*
//moon
sphere { <-3,3,1>, 1
    pigment { White }
    normal { wrinkles 1 scale 0.5 }
}

//donut
torus { 0.5 0.2 
    pigment { White }
    normal { bumps 0.4 scale 0.2 }
    rotate 90*x translate <0,2,0.3>
}   

plane { <0,1,-0.1>, -2 finish { reflection { Blue 1.0} ambient 0 diffuse 0 } }    
*/