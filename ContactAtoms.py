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
    parser.add_argument('contacts', help='unmutated contacts')
    parser.add_argument('mutated', help='mutated contacts')
    args = parser.parse_args()

    contacts = []

    with open(args.contacts, 'r') as f:
        for line in f:
            if line[0] is not '#':
                if "_:23@" in line:
                    print line
                else:
                    contacts.append(line)

    # model 1:
    # remove contacts with itself select all lines with ':23@\l*\d*_:23@'
    # count atom contacts for each residue
    # get contacts of mutation
    # substract mutation contacts from residue atom contact count
    #

if __name__ == "__main__":
    main(sys.argv)
