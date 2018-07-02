# -*- coding: future_fstrings -*-

import cadquery as cq
import numpy as np
import math
import quaternion as quat
from svgpathtools import svg2paths2, Line
import logging as log
import sys
import itertools
import pyclipper

# import pydevd
log.basicConfig(stream=sys.stderr, level=log.DEBUG)

top_plate_depth = 9.0

# angles
tent = 17.5
split = 25
slope = 7.5

# size
# from http://builder.swillkb.com/
# 4 holes, 6 mm, 20 mm2
# 20 mm padding
# 7.5 mm corners
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
keycap_fillet = 3

left_x = left_plate_x + (2 * extra_base)
right_x = right_plate_x + (2 * extra_base)
y = plate_y + (2 * extra_base)
extrude = 150

SVG_PATH = '/opt/cadquery/build_data/'

arc_tolerance = 100000000

depth_path = cq.Workplane("XZ").lineTo(0, extrude)

# global 0,0,0 is the pivot point where the halves meet on the bottom

def right():
    big_corner_x = right_x-big_corner+(big_corner*math.sin(math.radians(45)))
    big_corner_y = -y-wrist+big_corner-(big_corner*math.cos(math.radians(45)))
    small_corner_x = right_x-small_corner+(small_corner*math.sin(math.radians(45)))
    small_corner_y = -small_corner+(small_corner*math.cos(math.radians(45)))

    wp = cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, tent, split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0))

    return wp.lineTo(0, -(y+wrist)) \
        .lineTo(right_x-big_corner, -(y+wrist)) \
        .threePointArc((big_corner_x, big_corner_y), (right_x, -y-wrist+big_corner)) \
        .lineTo(right_x, -small_corner) \
        .threePointArc((small_corner_x, small_corner_y), (right_x-small_corner, 0)) \
        .close() \
        .sweep(depth_path) \
        .cut(svg('right_top', right_workplane().center(extra_base, -extra_base), -top_plate_depth, [3, 4, 5, 6, 7, 8], fillet=keycap_fillet))


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
        .sweep(depth_path) \
        .cut(svg('left_top', left_workplane().center(-left_plate_x-extra_base, y-extra_base), top_plate_depth, [3, 4, 5], invert=False, fillet=keycap_fillet))


def center():
    wp = cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(-slope, 0, 0))

    right = wp.plane.toLocalCoords(right_gap_bottom())
    left = wp.plane.toLocalCoords(left_gap_bottom())

    return wp \
        .lineTo(right.x, right.y) \
        .lineTo(left.x, left.y) \
        .close() \
        .sweep(depth_path)


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
        .plane.toWorldCoords((right_x-small_corner, 0))


def left_back_corner():
    return cq.Workplane("XY") \
        .transformed(rotate=cq.Vector(0, -tent, -split/2)) \
        .transformed(rotate=cq.Vector(-slope, 0, 0)) \
        .plane.toWorldCoords((-left_x+small_corner, 0))


def build_plane(p1, p2, p3, origin, z_rot=0):
    # These two vectors are in the plane
    v1 = p3 - p1
    v2 = p2 - p1

    # the cross product is a vector normal to the plane
    normal = np.cross(v1, v2)

    return cq.Plane(origin, (math.cos(math.radians(z_rot)), math.sin(math.radians(z_rot)), 0), (normal[0], normal[1], normal[2]))


def right_plane():
    right_corner = right_back_corner()
    right_gap = right_gap_bottom()
    p1 = np.array([0, 0, extrude])
    p2 = np.array([right_corner.x, right_corner.y, right_corner.z+extrude])
    p3 = np.array([right_gap.x, right_gap.y, right_gap.z+extrude])
    return build_plane(p1, p2, p3, (0, 0, extrude), split/2)


def left_plane():
    left_corner = left_back_corner()
    left_gap = left_gap_bottom()
    p1 = np.array([0, 0, extrude])
    p2 = np.array([left_corner.x, left_corner.y, left_corner.z+extrude])
    p3 = np.array([left_gap.x, left_gap.y, left_gap.z+extrude])
    return build_plane(p1, p2, p3, (0, 0, extrude), -split/2)


def right_workplane():
    return cq.Workplane(right_plane())


def left_workplane():
    return cq.Workplane(left_plane())


def back():
    right_corner = right_back_corner()
    left_corner = left_back_corner()

    # compute the plane from these vectors
    p1 = np.array([0, 0, extrude])
    p2 = np.array([right_corner.x, right_corner.y, right_corner.z+extrude])
    p3 = np.array([left_corner.x, left_corner.y, left_corner.z+extrude])
    plane = build_plane(p1, p2, p3, (0, 0, extrude))

    right_transformed = plane.toLocalCoords(cq.Vector(right_corner.x, right_corner.y, right_corner.z+extrude))
    left_transformed = plane.toLocalCoords(cq.Vector(left_corner.x, left_corner.y, left_corner.z+extrude))

    return cq.Workplane(plane) \
        .lineTo(right_transformed.x, right_transformed.y) \
        .lineTo(left_transformed.x, left_transformed.y) \
        .close() \
        .sweep(depth_path)


def chop():
    depth = right_back_corner().z * -2
    return cq.Workplane("XY") \
        .transformed(offset=(0, right_gap_bottom().y / 2, right_gap_bottom().z - depth + (depth / 2) + fillet_r)) \
        .box(800, 400, depth)


def debox(x, y, z):
    return cq.Workplane("XY") \
        .transformed(offset=(x, y, z)) \
        .box(50, 50, 50)

def svg(svg_file, workplane, extrude_length, shapes=None, invert=True, fillet=None):
    """
    extrude shapes in the svg file on the workplane
    :param svg_file: file name of svg file
    :param workplane: workplane to add svg to
    :param extrude_length: amount to extrude by
    :param shapes: list of shapes in the svg file to extrude (null extrudes all)
    :param invert: invert (y * -1) the svg?
    :return: workplane
    """
    paths, attributes, svg_attributes = svg2paths2(f'{SVG_PATH}{svg_file}.svg')
    polys = list(map(lambda path: (list(map(lambda segment: (segment.start.real, (-1 if invert else 1) * segment.start.imag), path))), paths))
    min_x = reduce(lambda acc, i: min(acc, i[0]), itertools.chain.from_iterable(polys), sys.maxsize)
    max_y = reduce(lambda acc, i: max(acc, i[1]), itertools.chain.from_iterable(polys), -sys.maxsize)

    for idx, poly in enumerate(polys):
        if shapes is None or idx in shapes:
            zeroed_poly = map(lambda point: (point[0] - min_x, point[1] - max_y), poly)
            if fillet:
                filleted_poly = fillet_shape(zeroed_poly, fillet)
            else:
                filleted_poly = zeroed_poly
            workplane = workplane.moveTo(*filleted_poly[0]).polyline(filleted_poly[1:]).close().extrude(extrude_length)
    return workplane


def fillet_shape(poly, radius, convex = True):
    """
    fillet a polygon
    :param poly: list of point tuples describing the polygon
    :param radius: radius to fillet by
    :param convex: if true fillet the convex corners, if false fillet the concave corners
    :return: list of point representing the filleted polygon
    """
    scaled_radius = radius * 2 ** 31

    pco = pyclipper.PyclipperOffset()
    pco.ArcTolerance = arc_tolerance

    # shrink
    pco.AddPath(pyclipper.scale_to_clipper(poly), pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    expanded = pco.Execute(-scaled_radius if convex else scaled_radius)

    # expand
    pco.Clear()
    pco.AddPath(expanded[0], pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    result = pyclipper.scale_from_clipper(pco.Execute(scaled_radius if convex else -scaled_radius))

    return map(lambda point: (point[0], point[1]), result[0])


def body():
    return center() \
    .union(right()) \
    .union(left()) \
    .union(back()) \
    .cut(chop()) \
    .cut(svg('right_top', right_workplane().transformed(offset=(0,0,-top_plate_depth)).center(extra_base, -extra_base), -extrude, [0])) \
    .cut(svg('left_top', left_workplane().transformed(offset=(0,0,top_plate_depth)).center(-left_plate_x-extra_base, y-extra_base), extrude, [0]))

#     .edges().fillet(fillet_r) \

def test():
    return svg('right_top', cq.Workplane("XY"), extrude, [4])


def test2():
    return svg('right_top', cq.Workplane("XY").transformed(offset=(100,0,0)), extrude, [4], fillet=3)


show_object(body())
