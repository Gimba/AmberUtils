#!/usr/bin/env python

import sys
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Plot residue interactions.')
    parser.add_argument('infile', help='pdb file as input')
    parser.add_argument('outfile', help='outfile')
    args = parser.parse_args()

    table = []
    table_line = []
    column = 0
    header = []
    with open(args.infile, 'r') as f:
        for line in f:
            line = filter(None, line.split(" "))
            if line[0] == 'ATOM' and line[1].isdigit():
                header.append(int(line[1]))

                # add lines to table
                table_line.append(line[5])
                table_line.append(line[6])
                table_line.append(line[7])

            if line[0] == 'ENDMDL\n':
                table.append(table_line)
                table_line = []

    header = sorted(set(header))

    first_line = []
    for item in header:
        first_line.append('ATOM ' + str(item) + ' X')
        first_line.append('ATOM ' + str(item) + ' Y')
        first_line.append('ATOM ' + str(item) + ' Z')

    first_line = ','.join(first_line)

    with open(args.outfile, 'w') as f:
        f.write(first_line)
        for item in table:
            item = ','.join(item)
            f.write(item + '\n')

if __name__ == "__main__":
    main(sys.argv)