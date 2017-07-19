#!/usr/bin/env python

import sys
import argparse
import matplotlib.pyplot as plt

def main(argv):
    parser = argparse.ArgumentParser(description='Plot energy atom correlation interactions.')
    parser.add_argument('infile', help='csv file created by energy_atom_correlation.py')
    args = parser.parse_args()
    values = []

    with open(args.infile, 'r') as f:
        for line in f:
            temp = line.split(',')
            temp[1] = float(temp[1])
            temp[2] = float(temp[2][:-1])
            values.append(temp)

    values = sorted(values, key=lambda x: (x[1]))

    outfile = str(args.infile).split('.')[0]

    neg = []
    xticks = []
    for i in range(0, len(values)):
        item = values[i]
        neg.append(item[1])
        xticks.append(item[0])

    plt.figure(figsize=(25, 15))
    plt.xticks(range(len(xticks)), xticks, size='small', rotation='45', ha='right')
    plt.plot(neg)
    plt.ylabel("correlation coefficient")
    plt.suptitle(outfile.split('corr')[0][:-1], fontsize=32, fontweight='bold')
    plt.title("Correlation between pairwise distances and energy values in 30 independent short simulations",
                fontsize=18, ha='center')
    plt.savefig(outfile + ".png")

if __name__ == "__main__":
    main(sys.argv)