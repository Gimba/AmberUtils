#! /usr/bin/env python

# Copyright (c) 2017 Martin Rosellen

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import sys
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Merge content of all files \'*distance*.dat\' (generated by '
                                                 'CorrelationEnergyPairwiseDistance.pyhairpin_distance_each.cpptraj) into res_dist_merged.dat')

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

    with open('res_dist_merged.dat','w') as f:
        for column in values:
            column = ', '.join(column)
            f.write(column + "\n")

if __name__ == "__main__":
    main(sys.argv)