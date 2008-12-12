#include "penguin.inc"

//display routine

background {White}
// set viewer's position in the scene
camera {
  location <0,0,-7>
  direction z
  right x*image_width/image_height
  look_at <0.0, 0.0, 0.0>
}

light_source {   
    <0, 0, -6>
    White
} 

object { Penguin }