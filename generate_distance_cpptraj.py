#!/usr/bin/env python

mask1 = ['23','24','25','26','27']

mask2 = ['187','188','247','249','252','429','422','427','421','405','469']

for item1 in mask1:
    for item2 in mask2:
        print "distance " + item1 + "-" + item2 + " :" + item1 + " :" + item2 + " out distance_" + item1 + "_" + \
              item2 + ".dat"
