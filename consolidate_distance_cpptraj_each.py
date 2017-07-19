#!/usr/bin/env python

import os

files = []
for i in os.listdir('.'):
    if os.path.isfile(os.path.join('.',i)) and 'distance' in i and '.dat' in i:
        files.append(i)

values = []
for item in files:
    distances = []
    with open(item, 'r') as f:
        for line in f:
            temp = line.split(' ')
            temp = filter(None, temp)
            distances.append(temp[1][:-1])
    values.append(distances)
