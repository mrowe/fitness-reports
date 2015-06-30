#! /usr/bin/env python

import sys

import gpxpy

from geopy.point import Point
from geopy.distance import vincenty

try:
    filename = sys.argv[1]
    gpx_file = open(filename, 'r')
except IndexError as e:
    print "Usage: %s: <filename>" % sys.argv[0]
    sys.exit(1)

gpx = gpxpy.parse(gpx_file)

def gpx2point(gpx_point):
    return Point(gpx_point.latitude, gpx_point.longitude)

distance = 0

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            this_point = gpx2point(point)
            try:
                distance += vincenty(last_point, this_point).meters
            except NameError:
                None
            last_point = this_point

print "Total distance: %.1f km" % (distance / 1000)
