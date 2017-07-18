#!/usr/bin/env python

import sys
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Plot residue interactions.')
    parser.add_argument('infile', help='pdb atom records as table from pdb2table')
    parser.add_argument('energy', help='energy values')
    parser.add_argument('outfile', help='outfile')
    args = parser.parse_args()

    energies = []
    with open(args.energy, 'r') as f:
        for line in f:
            if(line.isdigit()):
                energies.append(float(line))

    table = []
    with open(args.infile, 'r') as f:
        f.readline()
        for line in f:
            table.append(line)

if __name__ == "__main__":
    main(sys.argv)