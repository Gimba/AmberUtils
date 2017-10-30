#! /usr/bin/env python

import os
from collections import Counter


def main():
    # get .dat files in folder
    files = os.listdir(".")
    mutations = [item.split("_")[0] for item in files]

    out_list = []
    residues = []

    for f in files:
        with open(f, 'r') as file:
            values = []
            for line in file:
                line = line.split()
                residues.append(line[0])
                # if line[0].isdigit():
                #     line[0] = int(line[0])
                if 'total' == line[0]:
                    values.append(line)
            out_list.append(sorted(values))

    for i in range(0,len(files)):
        print [mutations[i]] + out_list[i]

    print Counter(residues)

if __name__ == "__main__":
    main()
