#! /usr/bin/env python

import sys
import string
import re
from datetime import timedelta

import gpxpy


def guess_sport(filename):
    '''
    decide if this is cycling or running
    '''
    if re.search("Cycling|Ride", filename):
        return "Cycling"
    if re.search("Run(ning)?", filename):
        return "Running"
    if re.search("Walk", filename):
        return "Walking"
    else:
        return "Unknown"


def run(gpx_files):
    if not gpx_files:
        print('No GPX files given')
        sys.exit(1)

    totals = {}

    for gpx_file in gpx_files:
        try:
            sport = guess_sport(gpx_file)
            gpx = gpxpy.parse(open(gpx_file, 'r'))
            if len(gpx.tracks) == 0:
                continue
            start_date = gpx.get_time_bounds()[0] + timedelta(hours=10) # hope I never run/ride outside AEST
            month_key = start_date.strftime('%Y-%m')
            if not totals.has_key(month_key):
                totals[month_key] = {}
            if totals[month_key].has_key(sport):
                totals[month_key][sport] += gpx.length_3d()
            else:
                totals[month_key][sport] = gpx.length_3d()
        except Exception as e:
            sys.stderr.write('Error processing %s: %s\n' % (gpx_file, e))

    sports = sorted(set([sport for total in totals.itervalues() for sport in total.iterkeys()]))
    sys.stdout.write("month,%s\n" % string.join(sports, ","))

    for month in sorted(totals):
        sys.stdout.write(month)
        for sport in sports:
            if totals[month].has_key(sport):
                total = totals[month][sport] / 1000
            else:
                total = 0
            sys.stdout.write(",%.1f" % (total))
        sys.stdout.write("\n")

if __name__ == '__main__':
    run(sys.argv[1:])
