#! /usr/bin/env python

import sys

import gpxpy

from geopy.point import Point
from geopy.distance import vincenty

try:
    filename = sys.argv[1]
except IndexError as e:
    print "Usage: %s: <filename>" % sys.argv[0]
    sys.exit(1)

gpx = gpxpy.parse(open(filename, 'r'))

distance = 0

for track in gpx.tracks:
    for segment in track.segments:
        distance += segment.length_2d()

print "Total distance: %.1f km" % (distance / 1000)
