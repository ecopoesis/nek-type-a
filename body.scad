include <bosl/math.scad>
include <bosl/quaternions.scad>

tent = 15;
split = 25;
slope = 7.5;

left_x = 200;
right_x = 350;
y = 225;
top_z = 50;

left_quat = Q_Mul(Q_Mul(Quat([0,-1,0],tent), Quat([0,0,-1],split/2)), Quat([-1,0,0],slope));
right_quat = Q_Mul(Q_Mul(Quat([0,1,0],tent), Quat([0,0,1],split/2)), Quat([-1,0,0],slope));

// point where the two halves meet in the back
left_pivot = Q_Rot_Vector([left_x/2,y/2,top_z/2], left_quat);
right_pivot = Q_Rot_Vector([-right_x/2,y/2,top_z/2], right_quat);

// corners at wide part of gap
left_gap = Q_Rot_Vector([left_x/2,-y/2,top_z/2], left_quat);
right_gap = Q_Rot_Vector([-right_x/2,-y/2,top_z/2], right_quat);

// front outside corners
left_fout = Q_Rot_Vector([-left_x/2,-y/2,top_z/2], left_quat);
right_fout = Q_Rot_Vector([right_x/2,-y/2,top_z/2], right_quat);

echo(right_fout=right_fout[2],right_pivot=right_pivot[2],left_pivot=left_pivot[2]);

left_top();
right_top();

module left_top() {
  translate(v=[-left_pivot[0],-left_gap[1],-left_pivot[2]-right_fout[2]+right_pivot[2]]) {
    Qrot(left_quat) {
      cube([left_x,y,top_z], center=true);  
    }
  }
}

module right_top() {
  translate(v=[-right_pivot[0],-right_gap[1],-right_fout[2]]) {
    Qrot(right_quat){
      cube([right_x,y,top_z], center=true);
    }
  }
}
