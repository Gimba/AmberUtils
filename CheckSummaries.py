#! /usr/bin/env python

import sys
import os
import numpy as np

def main(argv):
    files = []
    summaries = ["summary.TEMP", "summary.ETOT", "summary.EKTOT", "summary.EPTOT"]
    for file in os.listdir('.'):
        if any(file in s for s in summaries):
            files.append(file)

    if len(files) != 4:
        print("not all summaries found")
        print("found: " + str(files))



    #  check temperature, total energy, kinetic energy and potential energy
    for name in files:
        with open(name, 'r') as f:
            content = f.readlines()
            content = [float(item.split()[1]) for item in content]

            lowest = min(content)
            highest = max(content)

            avrg = np.average(content)
            perc = avrg / 100

            low_diff = abs(avrg - lowest)
            high_diff = abs(avrg - highest)

            flag = 1
            if low_diff / perc > 1:
                print(name + " --- exceptional low value: " + str(lowest))
                flag = 0
            if high_diff / perc > 1:
                print(name + " --- exceptional high value: " + str(highest))
                flag = 0
            if flag:
                print(name + " ------- OK")

if __name__ == "__main__":
    main(sys.argv)
