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

import argparse
import sys

__author__ = 'Martin Rosellen'
__docformat__ = "restructuredtext en"

def main(argv):
    parser = argparse.ArgumentParser(description='Convert a given residue number from 1iqd.pdb '
                                                 'to '
                                                 'range of mutated pdb (e.g. 1-156 to 2174-2329 for C domain)')
    parser.add_argument('number', help='Residue number separated by whitespace that will be converted')
    # parser.add_argument('chain', nargs='?', help='chain')

    args = parser.parse_args()

    convert(args.number)

def convert(number):
    number = int(number)
    out = ""
    # to 1iqd numbering

    # C2 domain residues
    if number < 157:
        out = 'C' + str(number + 2173)
    # BO2C11 light chain A (2 - 212)
    elif 157 <= number <= 367:
        out = 'A' + str(number - 155)
    # BO2C11 heavy chain B (1 - 83)
    elif 368 <= number <= 450:
        out = 'B' + str(number - 367)
    # BO2C11 light chain B residue 83 is followed by 83A, 83B, 83C
    elif number == 451:
        out = 'B' + "83A"
    elif number == 452:
        out = 'B' + "83B"
    elif number == 453:
        out = 'B' + "83C"
    # BO2C11 heavy chain B (84 - 212)
    elif 455 <= number <= 582:
        out = 'B' + str(number - 370)
    # other direction
    elif number > 2173:
        out = number - 2173
        # elif 1 <= number <= 212:
        #     if chain == "A":
        #         out = str(number + 155) + " A"
        #     elif chain == "B":
        #         out = str(number + 367) + " B"
    print out
    return str(out)
if __name__ == "__main__":
    main(sys.argv)
