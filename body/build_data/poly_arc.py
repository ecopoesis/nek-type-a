# -*- coding: future_fstrings -*-

from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class PolyArc(object):

    # take the list of points and divide into arc segments
    # the arc segments will include the start and end points
    # assume there are lines between the arcs
    def __init__(self, threshold, *points):
        self.threshold = threshold
        self.segments = []

        segment = []
        start_with_line = False
        for idx, p in enumerate(points):
            eprint(p)
            prev = points[idx-1]
            if  (self.compare(prev[0], p[0]) or self.compare(prev[1], p[1])):
                # we've detected a line, so save the segment and move on
                if len(segment) > 0:
                    self.segments.append(segment)
                    segment = []
                if idx == 0:
                    start_with_line = True
            segment.append(p)

        # append final segment
        if len(segment) > 0:
            if start_with_line:
                self.segments.append(segment)
            else:
                self.segments[0] = segment + self.segments[0] 

        # convert the segments into three point arcs
        self.arcs = []
        for s in self.segments:
            # remove kinks
            if (len(s) >= 3):
                self.arcs.append(Arc(s[0], s[len(s)/2], s[-1]))


    def compare(self, a, b):
        return abs(a-b) <= self.threshold


class Arc(object):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f'Arc{{{self.a},{self.b},{self.c}}}'

    def __repr__(self):
        return f'Arc{{{self.a},{self.b},{self.c}}}'
