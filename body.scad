tent = 15;
split = 25;

left_x = 250;
right_x = 350;
y = 225;
z = opp(tent,right_x);
gap = opp(split/2,y);

left();
right();

function opp(angle,hyp) = hyp * sin(angle);

module left() {
  translate(v=[0,gap,z-opp(tent,left_x)]) {
    rotate(a=split/2, v=[0,0,-1]) {
      rotate(a=tent, v=[0,-1,0]) {
        cube([left_x,y,20]);
      }  
    }
  }
}

module right() {
  translate(v=[opp(90-tent,left_x)+gap*2,0,z]) {
    rotate(a=split/2, v=[0,0,1]) {
      rotate(a=tent, v=[0,1,0]) {
        cube([right_x,y,20]);
      }
    }
  }
}
