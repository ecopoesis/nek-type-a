import cadquery as cq
import numpy as np
import math
import quaternion as quat
import logging as log
import sys
log.basicConfig(stream=sys.stderr, level=log.DEBUG)

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
extrude = 100

path = cq.Workplane("XZ").lineTo(0, extrude)

# global 0,0,0 is the pivot point where the halves meet


def right():
    big_corner_x = right_x-big_corner+(big_corner*math.sin(math.radians(45)))
    big_corner_y = -y-wrist+big_corner-(big_corner*math.cos(math.radians(45)))
    small_corner_x = right_x-small_corner+(small_corner*math.sin(math.radians(45)))
    small_corner_y = -small_corner+(small_corner*math.cos(math.radians(45)))

    return cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, tent, split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0)) \
        .lineTo(0, -(y+wrist)) \
        .lineTo(right_x-big_corner, -(y+wrist)) \
        .threePointArc((big_corner_x, big_corner_y), (right_x, -y-wrist+big_corner)) \
        .lineTo(right_x, -small_corner) \
        .threePointArc((small_corner_x, small_corner_y), (right_x-small_corner, 0)) \
        .close() \
        .sweep(path)


def left():
    big_corner_x = -left_x+big_corner-(big_corner*math.sin(math.radians(45)))
    big_corner_y = -y-wrist+big_corner-(big_corner*math.cos(math.radians(45)))
    small_corner_x = -left_x+small_corner-(small_corner*math.sin(math.radians(45)))
    small_corner_y = -small_corner+(small_corner*math.cos(math.radians(45)))

    return cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, -tent, -split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0)) \
        .lineTo(0, -(y+wrist)) \
        .lineTo(-left_x+big_corner, -(y+wrist)) \
        .threePointArc((big_corner_x, big_corner_y), (-left_x, -y-wrist+big_corner)) \
        .lineTo(-left_x, -small_corner) \
        .threePointArc((small_corner_x, small_corner_y), (-left_x+small_corner, 0)) \
        .close() \
        .sweep(path)


def center():
    wp = cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(-slope, 0, 0))

    right = wp.plane.toLocalCoords(right_gap_bottom())
    left = wp.plane.toLocalCoords(left_gap_bottom())

    return wp \
        .lineTo(right.x, right.y) \
        .lineTo(left.x, left.y) \
        .close() \
        .sweep(path)


def right_gap_bottom():
    return cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, tent, split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0)) \
        .plane.toWorldCoords((0, -(y+wrist)))


def left_gap_bottom():
    return cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, -tent, -split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0)) \
        .plane.toWorldCoords((0, -(y+wrist)))


def right_back_corner():
    return cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, tent, split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0)) \
        .plane.toWorldCoords((right_x, 0))


def left_back_corner():
    return cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, -tent, -split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0)) \
        .plane.toWorldCoords((-left_x, 0))


def back():
    right_corner = right_back_corner()
    left_corner = left_back_corner()

    log.debug(right_corner)
    log.debug(left_corner)

    # compute the plane from these vectors
    p1 = np.array([0, 0, extrude])
    p2 = np.array([right_corner.x, right_corner.y, right_corner.z+extrude])
    p3 = np.array([left_corner.x, left_corner.y, left_corner.z+extrude])

    # These two vectors are in the plane
    v1 = p3 - p1
    v2 = p2 - p1

    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)
    a, b, c = cp

    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    d = np.dot(cp, p3)

    log.debug(cp)
    log.debug(cp[0])
    log.debug(cp[1])
    log.debug(cp[2])

    plane = cq.Plane((0, 0, extrude), (1, 0, 0), (cp[0], cp[1], cp[2]))
    return cq.Workplane(plane) \
        .box(800, 200, 10)


def origin():
    return cq.Workplane("XY") \
        .box(600, 300, 10)


def debox(x, y, z):
    return cq.Workplane("XY") \
        .transformed(offset=(x, y, z)) \
        .box(50, 50, 50)

body = center() \
    .union(right()) \
    .union(left()) \
    .edges().fillet(fillet_r) \
    .union(back())

show_object(body)
