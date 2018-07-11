import cadquery as cq
import math
import numpy as np


class CoordPlane(object):

    def __init__(self, p1, p2, p3, origin, z_rot=0):
        self.p1 = np.array([p1[0], p1[1], p1[2]])
        self.p2 = np.array([p2[0], p2[1], p2[2]])
        self.p3 = np.array([p3[0], p3[1], p3[2]])
        self.origin = origin
        self.z_rot = z_rot

    def normal(self):
        # These two vectors are in the plane
        v1 = self.p3 - self.p1
        v2 = self.p2 - self.p1

        # the cross product is a vector normal to the plane
        return np.cross(v1, v2)

    def plane(self):
        normal = self.normal()
        return cq.Plane(self.origin, (math.cos(math.radians(self.z_rot)), math.sin(math.radians(self.z_rot)), 0), (normal[0], normal[1], normal[2]))

    def workplane(self):
        return cq.Workplane(self.plane())
