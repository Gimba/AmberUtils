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

__author__ = 'Martin Rosellen'
__docformat__ = "restructuredtext en"

def main(argv):
    parser = argparse.ArgumentParser(description='Convert a given residue number from 1iqd.pdb '
                                                 'to '
                                                 'range of mutated pdb (e.g. 1-156 to 2174-2329 for C domain)')
    parser.add_argument('number', help='Residue number separated by whitespace that will be converted')
    parser.add_argument('chain', nargs='?', help='chain')

    args = parser.parse_args()

    number = int(args.number)

    # to 1iqd numbering
    if (len(argv) == 2):
        if number < 157:
            print number + 2173
        elif 157 <= number <= 367:
            print str(number - 155) + " A"
        elif 368 <= number <= 582:
            print str(number - 367) + " B"

    # to mutant numbering
    else:
        if number > 2173:
            print number - 2173
        elif 1 <= number <= 212:
            if args.chain == "A":
                print str(number + 155) + " A"
            elif args.chain == "B":
                print str(number + 367) + " B"

if __name__ == "__main__":
    main(sys.argv)
