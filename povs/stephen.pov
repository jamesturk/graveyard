#include "colors.inc"

background {Red}

// set viewer's position in the scene
camera {
  location <0,0,-10>
  direction z
  right x*image_width/image_height
  look_at <0.0, 0.0, 0.0> 
  rotate 360*y*clock
}

light_source {   
    <0, 0, -10> 
    Green
    rotate 360*y*clock
} 
 
light_source {
    <0,1,0>
    Yellow
}

cone {
  1*y,  0.0,
  -1*y, 1.0
  pigment { White }
}

// extrude a closed 2-D shape along an axis
prism {                                
  linear_sweep  
  linear_spline
  0,         // height 1
   0.5,         // height 2
  10,           // number of points
  // (--- the <u,v> points ---)
  < 0.2, -1.0>, < 0.2,  0.2>, < 1.0, -0.2>, < 1.0,  0.2>, < 0.2,  1.0>, 
  <-0.2,  1.0>, <-1.0,  0.2>, <-1.0, -0.2>, <-0.2,  0.2>, <-0.2, -1.0>
}
