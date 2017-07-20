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
import matplotlib.pyplot as plt


def main(argv):
    parser = argparse.ArgumentParser(description='Plot correlation between pairwise distances and energy values in 30 '
                                                 'independent short simulations. Name of outfile generated from '
                                                 'infile.')
    parser.add_argument('infile', help='csv file created by CorrelationEnergyPairwiseDistance.pyCorrelationEnergyPairwiseDistance.py')
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
