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

import sys
import argparse
import numpy as np
from scipy.stats.stats import pearsonr

def main(argv):
    parser = argparse.ArgumentParser(description='Calculate correlation between energy values and atom coordinates.')
    parser.add_argument('infile', help='pdb atom records as table from pdb2table')
    parser.add_argument('energy', help='energy values')
    parser.add_argument('outfile', help='outfile')
    args = parser.parse_args()

    energies = []
    with open(args.energy, 'r') as f:
        f.readline()
        for line in f:
            energies.append(float(line))

    table = []
    header = []
    with open(args.infile, 'r') as f:
        header = f.readline().split(',')
        # remove '/n' at end of line
        header[-1] = header[-1][:-1]
        for line in f:
            line = line.split(',')
            table.append(line)

    table = np.asarray(table).transpose()

    # convert all items to float
    table = [[float(y) for y in x] for x in table]

    # calculate pearson correlation for every atom coordinate
    correlations = []
    for column in table:
        correlations.append(pearsonr(energies,column))

    with open(args.outfile, 'w') as f:
        if len(correlations) != len(header):
            print "correlations and header differ in length"
            return
        for i in range(0,len(correlations)):
            f.write(header[i] + ", " + str(correlations[i][0]) + ", " + str(correlations[i][1]) + "\n")

if __name__ == "__main__":
    main(sys.argv)