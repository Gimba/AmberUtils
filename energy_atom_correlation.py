#!/usr/bin/env python

import sys
import argparse
import numpy as np
from scipy.stats.stats import pearsonr

def main(argv):
    parser = argparse.ArgumentParser(description='Plot residue interactions.')
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
        for line in f:
            line = line.split(',')
            table.append(line)

    table = np.asarray(table).transpose()

    # convert all items to float
    table = [[float(y) for y in x] for x in table]

    # calculate pearson correlation for every atom
    correlations = []
    for column in table:
        correlations.append(pearsonr(energies[0:50],column))

    with open(args.outfile, 'w') as f:
        if len(correlations) != len(header):
            print "correlations and header differ in length"
            return
        for i in range(0,len(correlations)):
            f.write(header[i] + ", " + str(correlations[i][0]) + ", " + str(correlations[i][1]) + "\n")

if __name__ == "__main__":
    main(sys.argv)