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
from scipy.stats.stats import pearsonr

def main(argv):
    parser = argparse.ArgumentParser(description='Plot residue interactions.')
    parser.add_argument('infile', help='csv generated by consolidate_distance_cpptraj_each')
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
        # remove '/n' at end of line
        for line in f:
            line = line.split(',')
            header.append(line[0])
            table.append(line[1:])
            # line = line.split(',')
            # table.append(line)
    table = [[float(y) for y in x] for x in table]

    # calculate pearson correlation for every distance
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