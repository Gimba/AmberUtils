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

    # get contact count for unmutated structure

    contacts = []

    with open(args.contacts, 'r') as f:
        for line in f:
            if line[0] is not '#':
                # get extra residue contacts
                if "_:23@" not in line:
                    line = line.split(' ')
                    line = filter(None, line)
                    line = line[1].split("_")[1]
                    line = line.split('@')[0]
                    line = line.replace(':', '')
                    contacts.append(line)

    residues = list(set(contacts))

    contact_atoms = []
    for item in residues:
        contact_atoms.append([item, contacts.count(item)])


    # get contact count for mutated structure

    mutated = []

    with open(args.mutated, 'r') as f:
        for line in f:
            if line[0] is not '#':
                # get extra residue mutated
                if "_:23@" not in line:
                    line = line.split(' ')
                    line = filter(None, line)
                    line = line[1].split("_")[1]
                    line = line.split('@')[0]
                    line = line.replace(':', '')
                    mutated.append(line)

    residues = list(set(mutated))

    mutated_atoms = []
    for item in residues:
        mutated_atoms.append([item, mutated.count(item)])

    print contact_atoms
    print mutated_atoms

    
    # model 1:
    # remove contacts with itself select all lines with ':23@\l*\d*_:23@'
    # count atom contacts for each residue
    # get contacts of mutation
    # substract mutation contacts from residue atom contact count
    #

if __name__ == "__main__":
    main(sys.argv)
