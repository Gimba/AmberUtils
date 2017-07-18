#!/usr/bin/env python

import sys
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Plot residue interactions.')
    parser.add_argument('infile', help='pdb file as input')
    parser.add_argument('outfile', help='outfile')
    args = parser.parse_args()

    table = []
    column = 0
    header = []
    with open(args.infile, 'r') as f:
        for line in f:
            line = filter(None, line.split(" "))
            if line[0] == 'ATOM' and line[1].isdigit():
                header.append(int(line[1]))


    header = sorted(set(header))

    
if __name__ == "__main__":
    main(sys.argv)