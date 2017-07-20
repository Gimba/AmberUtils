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


def main(argv):
    parser = argparse.ArgumentParser(description='Generate cpptraj pairwise masks for a list of residue numbers (e.g.'
                                                 ':1:2:3 :4:5 -> :1 :4; :1 :5; :2 :4; :2 :5 etc.)')
    parser.add_argument('-m1', '--mask1', help='residue numbers in first mask')
    parser.add_argument('-m2', '--mask2', help='residue numbers in second mask')
    args = parser.parse_args()

    mask1 = str(args.mask1).split(' ')
    mask2 = str(args.mask2).split(' ')

    for item1 in mask1:
        for item2 in mask2:
            print "distance " + item1 + "-" + item2 + " :" + item1 + " :" + item2 + " out distance_" + item1 + "_" + \
                  item2 + ".dat"

if __name__ == "__main__":
    main(sys.argv)