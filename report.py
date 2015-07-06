#! /usr/bin/env python

import sys
import os
import re
from datetime import timedelta
import calendar

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

    distance = 0
    duration = 0

    for track in gpx.tracks:
        for segment in track.segments:
            distance += segment.length_2d()
            duration += segment.get_duration()

    return date, distance


def guess_sport(filename):
    '''
    decide if this is cycling or running
    '''
    if re.compile("Cycling|Ride").search(filename):
        return "Cycling"
    if re.compile("Run(ning)?").search(filename):
        return "Running"
    if re.compile("Walk").search(filename):
        return "Walking"
    else:
        return "Unknown"

totals = {}

def run(gpx_files):
    if not gpx_files:
        print('No GPX files given')
        sys.exit(1)

    for gpx_file in gpx_files:
        try:
            start_date, distance = distance_for(gpx_file)
            month = "%4d %s" % (start_date.year, calendar.month_name[start_date.month])
            if not totals.has_key(month):
                totals[month] = {}
            sport = guess_sport(gpx_file)
            if totals[month].has_key(sport):
                totals[month][sport] += distance
            else:
                totals[month][sport] = distance
        except Exception as e:
            sys.stderr.write('Error processing %s: %s\n' % (gpx_file, e))

    for month in sorted(totals):
        sys.stdout.write("%s," % (month))
        for sport in totals[month]:
            sys.stdout.write("%s,%.1f," % (sport, totals[month][sport] / 1000))
        sys.stdout.write("\n")

if __name__ == '__main__':
    run(sys.argv[1:])
