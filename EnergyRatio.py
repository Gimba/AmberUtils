#! /usr/bin/env python

with open('1dqj_interactions_cmp.csv', 'r') as fi:
    fi.readline()
    temp = []
    pos = 0
    neg = 0
    for line in fi:
        temp = line.split(',',len(line))
        temp[2] = float(temp[2][0:-2])
        if(temp[2] > 0):
            pos += temp[2]
        else:
            neg = neg + temp[2]

with open('energy_ratio.csv','w') as fo:
    fo.write(str(pos) + "/n")
    fo.write(str(neg) + "/n")
