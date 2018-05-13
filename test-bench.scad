include <bosl/masks.scad>
include <bosl/math.scad>
include <bosl/quaternions.scad>
include <bosl/shapes.scad>
include <bosl/transforms.scad>

x=200;
y=150;
z=100;
overshoot=40;
tent = 17.5;
split = 25;
slope = 7.5;
quat = Q_Mul(Q_Mul(Quat([0,-1,0],tent), Quat([0,0,-1],split/2)), Quat([-1,0,0],slope));

bl_x = Q_Rot_Vector([-x/2,y/2,.5], quat)[0]-Q_Rot_Vector([-x/2,-y/2,.5], quat)[0];
bl_y = Q_Rot_Vector([-x/2,y/2,.5], quat)[1]-Q_Rot_Vector([-x/2,-y/2,.5], quat)[1];
bl_z = Q_Rot_Vector([-x/2,y/2,.5], quat)[2]-Q_Rot_Vector([-x/2,-y/2,.5], quat)[2];

fr_x = Q_Rot_Vector([x/2,-y/2,.5], quat)[0]-Q_Rot_Vector([-x/2,-y/2,.5], quat)[0];
fr_z = Q_Rot_Vector([x/2,-y/2,.5], quat)[2]-Q_Rot_Vector([-x/2,-y/2,.5], quat)[2];
echo(bl_x=bl_x);
echo(bl_y=bl_y);
echo(bl_z=bl_z);
echo(fr_x=fr_x);
echo(fr_z=fr_z);

true_split = angle([bl_x,bl_y],[0,bl_y],[0,0]);
true_tent = angle([fr_x,0],[fr_x,fr_z],[0,0]);
true_slope = angle([bl_y,0],[bl_y,bl_z],[0,0]);

echo(true_split=true_split);
echo(true_tent=true_tent);
echo(true_slope=true_slope);

big_r = 50;
r = 7.5;

$fs = 2;
$fa = 2;

hull() {
translate([0,0,2*r]) hulled();
difference() {
  linear_extrude(fr_z+(2*r)) projection(cut=false) hulled();
   // slice choppped off top to make wedge
  translate(v=[
            -Q_Rot_Vector([-x/2,-y/2,-50-(2*r)], quat)[0],
            -Q_Rot_Vector([-x/2,-y/2,-50-(2*r)], quat)[1],
            -Q_Rot_Vector([-x/2,-y/2,-50-(2*r)], quat)[2]]) {
    Qrot(quat) {
      cube([x+overshoot,y+overshoot,100], center=true);  
    }
  } 
}
};

module hulled() {
  hull() Qrot(quat) {
     translate([big_r, big_r, 0]) rcylinder(r=big_r, h=2*r, fillet=r, center=true);
     translate([r, y-r, 0]) sphere(r=r, center=true); // back left
     translate([x-r, y-r, 0]) sphere(r=r, center=true); // back right
     translate([x-r, r, 0]) sphere(r=r, center=true); // frn right     
  }
}
 
module thing() {
  difference() {
    // footprint shadow projected up
    translate(v=[0,0,-40]) linear_extrude(height=z) projection(cut=false) footprint(h=1);
    // slice choppped off top to make wedge
    translate(v=[
              -Q_Rot_Vector([-x/2,-y/2,-50], quat)[0],
              -Q_Rot_Vector([-x/2,-y/2,-50], quat)[1],
              -Q_Rot_Vector([-x/2,-y/2,-50], quat)[2]]) {
      Qrot(quat) {
        cube([x+overshoot,y+overshoot,100], center=true);  
      }
    }
  };
}

module footprint() {
  translate(v=[
            -Q_Rot_Vector([-x/2,-y/2,.5], quat)[0],
            -Q_Rot_Vector([-x/2,-y/2,.5], quat)[1],
            -Q_Rot_Vector([-x/2,-y/2,.5], quat)[2]]) {
    Qrot(quat) {
      cube([x,y,1], center=true);  
    }
  }
}

function angle(p1, p2, fixed) = atan2(p1[1] - fixed[1], p1[0] - fixed[0]) - atan2(p2[1] - fixed[1], p2[0] - fixed[0]);

