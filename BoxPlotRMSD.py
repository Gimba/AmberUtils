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


import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

__author__ = 'Martin Rosellen'
__docformat__ = "restructuredtext en"

def main(argv):
    parser = argparse.ArgumentParser(description='Boxplot values')
    parser.add_argument('--list', nargs='*')
    args = parser.parse_args()

    data = []
    xticks = []

    for file in args.list:

        # extract name of file
        tick = file.replace("_rmsd_prod_long_hairpin", "")
        xticks.append(tick[:-4])


        values = []
        with open(file,'r') as f:
            f.readline()
            for line in f:
                values.append(float(line.split("    ")[2][3:-1]))
        data.append(np.array(values))

    data = np.array(data)

    plt.ylim([0.6, 1.6])
    plt.xticks(range(len(xticks)), xticks, size='small', rotation='45', ha='right')
    plt.boxplot(data)
    plt.savefig("RMSD_boxplot.png")

if __name__ == "__main__":
    main(sys.argv)

