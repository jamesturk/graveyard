#include "colors.inc"

#declare PengFoot = blob {
    threshold 0.2
    cylinder { 0, -0.3*z, 0.1, 1 } 
    cylinder { 0, -0.3*z, 0.1, 1 rotate -30*y }
    cylinder { 0, -0.3*z, 0.1, 1 rotate 30*y}  
    scale 2
    pigment { Orange }
}

#declare Penguin = union {
    
    difference {
    blob {
        threshold 0.2
        sphere { <0, 1,0>, 1, 1 }
        sphere { <0,-0.5,0>, 1.5, 1 } 
        sphere { <0, -0.5, -0.3>, 1, 1 pigment { color White } }
        pigment { rgb (0.3) }
    }
    
    cylinder { 
        0*x, 0.1*x, 0.8
        translate <-1,-0.8,0>  
        pigment { rgb (0.3) }
    }
    
    cylinder { 
        0*x, -0.1*x, 0.8
        translate <1,-0.8,0>  
        pigment { rgb (0.3) }
    } 
    
    }
    
    sphere { <-0.25, 1.1, -0.7>, 0.1 }
    sphere { <0.25, 1.1, -0.7>, 0.1 }    
    
    cone { 
        0, 0.2,
        -0.4*z, 0
        translate <0,1,-0.6>
        pigment { Orange }
    } 
    
    object { PengFoot translate <-0.5,-1.5,-0.1> } 
    object { PengFoot translate <0.5,-1.5,-0.1> } 
}