#! /usr/bin/env python

import argparse
import sys

def main(argv):
    parser = argparse.ArgumentParser(description='Plot residue interactions.')
    parser.add_argument('file_1', help='HBond file 1')
    parser.add_argument('file_2', help='HBond file 2')
    parser.add_argument('outfile', help='outfile')
    args = parser.parse_args()

    labels_1 = []
    values_1 = []
    with open(args.file_1, 'r') as f:
        for line in f:
            temp = str.split(line,',')
            labels_1.append(temp[0]+',' +temp[1])
            values_1.append(temp[2])

    labels_2 = []
    values_2 = []
    with open(args.file_2, 'r') as f:
        for line in f:
            temp = str.split(line,',')
            labels_2.append(temp[0]+','+temp[1])
            values_2.append(temp[2])

    labels = []
    values = []

    for i in range(0,len(labels_1)):
        for j in range(0,len(labels_2)):
            if labels_1[i] == labels_2[j]:
                labels.append(labels_1[i])
                values.append(int(values_1[i]) - int(values_2[j]))

    with open(args.outfile, 'w') as f:
        for i in range(0,len(values)):
            f.write(labels[i] + ',' + str(values[i]) + '\r\n')


if __name__ == "__main__":
    main(sys.argv)