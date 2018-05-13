include <bosl/masks.scad>
include <bosl/math.scad>
include <bosl/quaternions.scad>
include <bosl/shapes.scad>
include <bosl/transforms.scad>

// taps should be >= M6

tent = 17.5;
split = 25;
slope = 7.5;

//$fa=1; $fs=1;

// from http://builder.swillkb.com/
// 20 mm padding, 7.5 mm corners
left_plate_x = 178.114;
right_plate_x = 235.264;
plate_y = 156.778; // for right, left is 154.302

// how much to add to the plates to make the base
extra_base = 15;

left_x = left_plate_x + (2 * extra_base);
right_x = right_plate_x + (2 * extra_base);
y = plate_y + (2 * extra_base);

// dimensions for the slice that gets removed from the top
overshoot = 300;
over_z = 150;

// how deep is the keyboard well
// should be < 3x plate corners
well_z = 20; 

// extra z to make there not be holes in the bottom
extra_z = 5;

// wrist rest depth (y-ish)
wrist = 100;

fillet_r = 7.5;
big_corner = 55;

// feather size
feather = [22.86,50.8,0];

left_quat = Q_Mul(Q_Mul(Quat([0,-1,0],tent), Quat([0,0,-1],split/2)), Quat([-1,0,0],slope));
right_quat = Q_Mul(Q_Mul(Quat([0,1,0],tent), Quat([0,0,1],split/2)), Quat([-1,0,0],slope));

// point where the two halves meet in the back at the top
function left_pivot(h,w=0) = Q_Rot_Vector([left_x/2,y/2+w/2,h/2], left_quat);
function right_pivot(h,w=0) = Q_Rot_Vector([-right_x/2,y/2+w/2,h/2], right_quat);

// the point "below" the pivot
function left_npivot(h) = left_pivot(-h);
function right_npivot(h) = right_pivot(-h);

// corners at wide part of gap
function left_gap(h,w=0) = Q_Rot_Vector([left_x/2,-y/2+w/2,h/2], left_quat);
function right_gap(h,w=0) = Q_Rot_Vector([-right_x/2,(-y/2)+(w/2),h/2], right_quat);

// the point "below" the gap
function left_ngap(h) = left_gap(-h);
function right_ngap(h) = right_gap(-h);

// front outside corners
function left_fout(h) = Q_Rot_Vector([-left_x/2,-y/2,h/2], left_quat);
function right_fout(h,w=0) = Q_Rot_Vector([right_x/2,-y/2+w/2,h/2], right_quat);

// total height is the height at the wide part of the gap
z=right_gap(1,-wrist)[2]-right_fout(1,wrist)[2]+well_z+extra_z;

//projection(cut=false) left_footprint_old(1);
//#projection(cut=false) left_footprint();

//left_fillet(1);
//right_footprint(1);
//right_fillet(1);

difference() {
  union() {
    center();
    left_side();
    right_side();
    //brains();
  }
}

module brains() {
  translate(v=[0,feather[1]/2,0]) rotate([0,0,180]) import("adafruit_feather.stl");
}

pivot_y = right_pivot(1)[1]-right_gap(1)[1];
pivot_z = right_pivot(1)[2]-right_fout(1)[2]+well_z+extra_z;
gap_x = Q_Rot_Vector([-right_x/2,(-y-wrist)/2,1/2], right_quat)[0]-right_pivot(1,wrist)[0];
gap_y = Q_Rot_Vector([-right_x/2,(-y-wrist)/2,1/2], right_quat)[1]-right_gap(1,wrist)[1];
gap_z = z;

function angle(p1, p2, fixed) = atan2(p1[1] - fixed[1], p1[0] - fixed[0]) - atan2(p2[1] - fixed[1], p2[0] - fixed[0]);

true_split = angle([gap_x,gap_y],[0,gap_y],[0,pivot_y]);

echo(true_split=true_split);

echo(pivot_y=pivot_y);
echo(pivot_z=pivot_z);
echo(gap_x=gap_x);
echo(gap_y=gap_y);
echo(gap_z=gap_z);

module center() {
  polyhedron(
    points=[
      [0,pivot_y,pivot_z],  // 0 - top pivot 
      [0,pivot_y,0],        // 1 - bottom pivot
      [-gap_x,gap_y,gap_z], // 2 - top left gap
      [gap_x,gap_y,gap_z],  // 3 - top right gap
      [-gap_x,gap_y,0],     // 4 - bottom left gap
      [gap_x,gap_y,0]       // 5 - bottom right gap
    ],
    faces=[
      [0,3,2],
      [1,4,5],
      [0,2,4,1],
      [3,0,1,5],
      [2,3,5,4]
    ]
  );
}

module left_side() {
  difference() {
    hull() {
      difference() {
        // footprint shadow projected up
        linear_extrude(height=z) projection(cut=false) left_footprint();
        // slice choppped off top to make wedge
        translate(v=[
                  -left_npivot(over_z)[0],
                  -left_ngap(over_z)[1],
                  -left_pivot(-over_z)[2]-right_fout(over_z)[2]+right_pivot(over_z)[2]+well_z+extra_z]) {
          Qrot(left_quat) {
            cube([left_x+overshoot,y+overshoot,over_z], center=true);  
          }
        }
      }
      // fillet top
      translate([0,0,well_z+extra_z]) left_footprint();
    }
    // keyboard well
    translate(v=[
              -left_pivot(well_z)[0],
              -left_gap(well_z)[1],
              -left_pivot(well_z-1)[2]-right_fout(well_z-1)[2]+right_pivot(well_z-1)[2]+well_z+extra_z+fillet_r]) {
      Qrot(left_quat) {
        translate(v=[-left_plate_x/2,-plate_y/2,0]) {
          linear_extrude(height=well_z, center=true) import("left_bottom.dxf");  
        }
      }
    }
  }
}

module right_side() {
  difference() {
    // footprint shadow projected up
    linear_extrude(height=z) projection(cut=false) right_footprint(h=1); 
    // slice choppped off top to make wedge
    translate(v=[
              -right_npivot(over_z)[0],
              -right_ngap(over_z)[1],
              right_pivot(over_z)[2]+well_z+extra_z]) {
      Qrot(right_quat) {
        cube([right_x+overshoot,y+overshoot+wrist,over_z], center=true);
      }
    }
    // keyboard well
    translate(v=[
              -right_pivot(well_z)[0],
              -right_gap(well_z)[1],
              -right_fout(well_z-1)[2]+well_z+extra_z]) {
      Qrot(right_quat) {
        translate(v=[-right_plate_x/2,-plate_y/2,0]) {
          linear_extrude(height=well_z, center=true) import("right_bottom.dxf");  
        }
      }    
    }
  } 
}

module left_footprint_old(h) {
  translate(v=[
            -left_pivot(h,wrist)[0],
            -left_gap(h,wrist)[1],
            -left_pivot(h,wrist)[2]-right_fout(h,wrist)[2]+right_pivot(h,wrist)[2]]) {
    Qrot(left_quat) {
      cube([left_x,y+wrist,h], center=true);  
    }
  }
}

module left_footprint() {
  translate(v=[
            -left_pivot(fillet_r*2,wrist)[0],
            -left_gap(fillet_r*2,wrist)[1],
            -left_pivot(fillet_r*2,wrist)[2]-right_fout(fillet_r*2,wrist)[2]+right_pivot(fillet_r*2,wrist)[2]]) {
  hull() Qrot(left_quat) translate([-left_x/2, -(y+wrist)/2, fillet_r]) {
      translate([big_corner, big_corner, 0]) rcylinder(r=big_corner, h=2*fillet_r, fillet=fillet_r, center=true); // big corner
      translate([fillet_r, y+wrist-fillet_r, 0]) sphere(r=fillet_r, center=true); // back left
      translate([left_x-fillet_r, y+wrist-fillet_r, 0]) sphere(r=fillet_r, center=true); // back right
      translate([left_x-fillet_r, fillet_r, 0]) sphere(r=fillet_r, center=true); // front right     
    }    
  }
}

module right_footprint(h) {
  translate(v=[
            -right_pivot(h,wrist)[0],
            -right_gap(h,wrist)[1],
            -right_fout(h,wrist)[2]]) {
    Qrot(right_quat){
      cube([right_x,y+wrist,h], center=true);
    }
  }
}
