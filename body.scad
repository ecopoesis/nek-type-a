include <bosl/masks.scad>
include <bosl/math.scad>
include <bosl/quaternions.scad>

tent = 15;
split = 25;
slope = 7.5;

$fa=10; $fs=10;

left_x = 200;
right_x = 350;
y = 225;

overshoot = 50;
over_z = 150;

radius = 0;

left_quat = Q_Mul(Q_Mul(Quat([0,-1,0],tent), Quat([0,0,-1],split/2)), Quat([-1,0,0],slope));
right_quat = Q_Mul(Q_Mul(Quat([0,1,0],tent), Quat([0,0,1],split/2)), Quat([-1,0,0],slope));

// point where the two halves meet in the back at the top
function left_pivot(h) = Q_Rot_Vector([left_x/2,y/2,h/2], left_quat);
function right_pivot(h) = Q_Rot_Vector([-right_x/2,y/2,h/2], right_quat);

// the point "below" the pivot
function left_npivot(h) = left_pivot(-h);
function right_npivot(h) = right_pivot(-h);

// corners at wide part of gap
function left_gap(h) = Q_Rot_Vector([left_x/2,-y/2,h/2], left_quat);
function right_gap(h) = Q_Rot_Vector([-right_x/2,-y/2,h/2], right_quat);

// the point "below" the gap
function left_ngap(h) = left_gap(-h);
function right_ngap(h) = right_gap(-h);

// front outside corners
function left_fout(h) = Q_Rot_Vector([-left_x/2,-y/2,h/2], left_quat);
function right_fout(h) = Q_Rot_Vector([right_x/2,-y/2,h/2], right_quat);

// total height is the height at the wide part of the gap
z = left_gap(1)[2]-left_pivot(h)[2]-right_fout(h)[2]+right_pivot(h)[2];

left_footprint(1);

left();
right();

module left() {
  difference() {
    linear_extrude(height=z) projection(cut=false) left_footprint(h=1);
    translate(v=[
              -left_npivot(over_z)[0],
              -left_ngap(over_z)[1],
              -left_pivot(-over_z)[2]-right_fout(over_z)[2]+right_pivot(over_z)[2]]) {
      Qrot(left_quat) {
        cube([left_x+overshoot,y+overshoot,over_z], center=true);  
      }
    }
  }
}

module right() {
  difference() {
    linear_extrude(height=z) projection(cut=false) right_footprint(h=1); 
    translate(v=[
              -right_npivot(over_z)[0],
              -right_ngap(over_z)[1],
              right_pivot(over_z)[2]]) {
      Qrot(right_quat) {
        cube([right_x+overshoot,y+overshoot,over_z], center=true);
      }
    }
  } 
}

module left_footprint(h) {
  translate(v=[
            -left_pivot(h)[0],
            -left_gap(h)[1],
            -left_pivot(h)[2]-right_fout(h)[2]+right_pivot(h)[2]]) {
    Qrot(left_quat) {
      cube([left_x,y,h], center=true);  
    }
  }
}

module right_footprint(h) {
  translate(v=[
            -right_pivot(h)[0],
            -right_gap(h)[1],
            -right_fout(h)[2]]) {
    Qrot(right_quat){
      cube([right_x,y,1], center=true);
    }
  }
}
