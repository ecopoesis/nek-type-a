# -*- coding: future_fstrings -*-

from __future__ import print_function
import sys
import logging as log

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
            log.info(p)
            prev = points[idx-1]
            if self.compare(prev[0], p[0]) or self.compare(prev[1], p[1]):
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
        log.info('segments:')
        for s in self.segments:
            log.info(s)
            # remove kinks
            if len(s) >= 3:
                self.arcs.append(Arc(s[0], s[len(s)/2], s[-1]))
            if len(s) == 1:
                self.arcs.append(Line(s[0]))


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


class Line(object):

    def __init__(self, a):
        self.a = a

    def __str__(self):
        return f'Line{{{self.a}}}'

    def __repr__(self):
        return f'Line{{{self.a}}}'
