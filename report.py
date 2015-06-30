#! /usr/bin/env python

import sys
import re
from datetime import timedelta

import gpxpy

from geopy.point import Point
from geopy.distance import vincenty

try:
    filename = sys.argv[1]
except IndexError as e:
    print "Usage: %s: <filename>" % sys.argv[0]
    sys.exit(1)


def distance_for(f):
    gpx = gpxpy.parse(open(f, 'r'))

    date = gpx.tracks[0].segments[0].points[0].time + timedelta(hours=10) # yeah that's awesome Michael
    # print "Processing %s ..." % date

    distance = 0
    duration = 0

    for track in gpx.tracks:
        for segment in track.segments:
            distance += segment.length_2d()
            duration += segment.get_duration()

    # print "Total distance: %.1f km" % (distance / 1000)
    # print "Total duration: %d min" % (duration / 60)
    return distance


def guess_sport(filename):
    '''
    decide if this is cycling or running
    '''
    if re.compile("Cycling").search(filename):
        return "Cycling"
    if re.compile("Running").search(filename):
        return "Running"
    else:
        return "Unknown"

totals = {}

def run(gpx_files):
    if not gpx_files:
        print('No GPX files given')
        sys.exit(1)

    for gpx_file in gpx_files:
        try:
            sport = guess_sport(gpx_file)
            if totals.has_key(sport):
                totals[sport] += distance_for(gpx_file)
            else:
                totals[sport] = distance_for(gpx_file)
        except Exception as e:
            print('Error processing %s: %s' % (gpx_file, e))
            sys.exit(1)

    for sport in totals:
        print "%s: %.1f km" % (sport, totals[sport] / 1000)

if __name__ == '__main__':
    run(sys.argv[1:])
