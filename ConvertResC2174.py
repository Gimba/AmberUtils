#! /usr/bin/env python

import sys
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Convert a given residue number from 1iqd.pdb C domain (2174-2329) to '
                                                 'range of mutated pdb (1-156)')
    parser.add_argument('number', help='Residue number separated by whitespace that will be converted')

    args = parser.parse_args()

    number = int(args.number)

    if number > 2173:
        print number - 2173
    elif number < 157:
        print number + 2173
    else:
        print "Number must be between 1 and 156 or 2173 and 2329"


if __name__ == "__main__":
    main(sys.argv)
