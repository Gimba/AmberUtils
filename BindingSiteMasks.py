#! /usr/bin/env python

import sys
import argparse
import csv

def main(argv):
    parser = argparse.ArgumentParser(description='Extract masks for bindingsite from decomp summary csv')
    parser.add_argument('infile', help='summary csv')
    parser.add_argument('mapping', help='mapping of residues')
    args = parser.parse_args()

    f = open(args.infile, 'r')
    reader = csv.DictReader(f)

    chains = []
    residues = []
    for row in reader:
        chains.append(row['Chain'])
        residues.append([row['Chain'], row['Residue']])
    chains = list(set(chains))

    masks = []
    for c in chains:
        temp = []
        for row in residues:
            if row[0] == c:
                temp.append(row[1][1:])
        masks.append(temp)

    print masks

    with open(args.mapping, 'r') as f:
        mapping = csv.DictReader(f)
        mapping = dict((row['to'], [row['from'], row['chain']]) for row in mapping)

    masks_lbl = []
    for mask in masks:
        residues = []
        for item in mask:
            item = mapping[item][0]
            residues.append(item)
        masks_lbl.append(residues)

    print masks_lbl

    all = [int(item) for sublist in masks_lbl for item in sublist]

    # create negative mask
    negative_mask = []
    for i in range(1,5000):
        if i not in all:
            negative_mask.append(i)
    print negative_mask
if __name__ == "__main__":
    main(sys.argv)