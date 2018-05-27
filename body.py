import cadquery as cq
#import numpy as np
import math
#import quaternion as quat

thickness = 10.0

# angles
tent = 17.5
split = 25
slope = 7.5

# size
# from http://builder.swillkb.com/
# 25 mm padding, 7.5 mm corners
left_plate_x = 173.352
right_plate_x = 263.839
plate_y = 159.064

# how much to add to the plates to make the base
extra_base = 15

# wrist rest depth (y-ish)
wrist = 62

# radii
fillet_r = 10
small_corner = 10
big_corner = 90

# quaternions
#right_quat = quat.from_euler_angles(alpha, beta, gamma)
#left_quat = Q_Mul(Q_Mul(Quat([0,-1,0],tent), Quat([0,0,-1],split/2)), Quat([-1,0,0],slope))
#right_quat = Q_Mul(Q_Mul(Quat([0,1,0],tent), Quat([0,0,1],split/2)), Quat([-1,0,0],slope))

#function _Quat(a,s,w) = [a[0]*s, a[1]*s, a[2]*s, w];
#function Quat(ax, ang) = _Quat(ax/norm(ax), sin(ang/2), cos(ang/2));

left_x = left_plate_x + (2 * extra_base)
right_x = right_plate_x + (2 * extra_base)
y = plate_y + (2 * extra_base)

# right side
big_corner_x = right_x-big_corner+(big_corner*math.sin(math.radians(45)))
big_corner_y = big_corner-(big_corner*math.cos(math.radians(45)))

small_corner_x = right_x-small_corner+(small_corner*math.sin(math.radians(45)))
small_corner_y = y+wrist-small_corner+(small_corner*math.cos(math.radians(45)))

path = cq.Workplane("XZ").lineTo(-10, 50)

result = cq.Workplane("XY") \
     .lineTo(right_x-big_corner, 0) \
     .threePointArc((big_corner_x, big_corner_y), (right_x, big_corner)) \
     .lineTo(right_x, y+wrist-small_corner) \
     .threePointArc((small_corner_x, small_corner_y), (right_x-small_corner, y+wrist)) \
     .lineTo(0, y+wrist) \
     .close().sweep(path) \
     .faces("+Z").edges().fillet(fillet_r)

show_object(result)

cq.SubtractSelector