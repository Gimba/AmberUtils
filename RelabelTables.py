#! /usr/bin/env python

import sys
import argparse


def main(argv):
    parser = argparse.ArgumentParser(
        description='Rename (re-letter) the specified table. If there are multiple chains with the same id in the pdb file, only the first is renamed.')
    parser.add_argument('infile', help='input file (PDB format)')
    parser.add_argument('outfile', help='output file (PDB format)')


if __name__ == "__main__":
    main(sys.argv)