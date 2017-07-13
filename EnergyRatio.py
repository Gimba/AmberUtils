#! /usr/bin/env python

import os

cwd = os.getcwd()

mutation = cwd.split('/', len(cwd))[-2]

mutation = mutation[-1] + mutation[1:5]

with open('1dqj_interactions_cmp.csv', 'r') as fi:
    fi.readline()
    temp = []
    pos = 0
    neg = 0
    muta = 0
    for line in fi:
        temp = line.split(',',len(line))

        if(mutation in temp[1]):
            muta = temp[2]

        temp[2] = float(temp[2][0:-2])
        if(temp[2] > 0):
            pos += temp[2]
        else:
            neg = neg + temp[2]

with open('energy_ratio.csv','w') as fo:
    # fo.write(mutation + ": " + str(muta))
    # fo.write("Energy gain: " + str(pos) + "\n")
    # fo.write("Energy loss: " + str(neg) + "\n")

    fo.write(str(muta))
    fo.write(str(pos) + "\n")
    fo.write(str(neg) + "\n")