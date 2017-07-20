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
    parser = argparse.ArgumentParser(description='Transform pdb into table that contains atom coordinates as columns.')
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
                header.append(line[1] + " " + line[3] + " " + line[4])

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
        f.write(first_line + '\n')
        for item in table:
            item = ','.join(item)
            f.write(item + '\n')

if __name__ == "__main__":
    main(sys.argv)