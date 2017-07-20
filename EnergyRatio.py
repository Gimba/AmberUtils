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

import os
import argparse
import sys

__author__ = 'Martin Rosellen'
__docformat__ = "restructuredtext en"


def main(argv):
    parser = argparse.ArgumentParser(description='Calculate the energies due to new and lost bonds. Assumes '
                                                 '\'1dqj_interactions_cmp.csv\' in the working directory. Output to '
                                                 'file energy_ratio.csv')


    cwd = os.getcwd()

    mutation = cwd.split('/', len(cwd))[-2]

    mutation = mutation[-1] + mutation[1:5]

    with open('1dqj_interactions_cmp.csv', 'r') as fi:
        fi.readline()
        temp = []
        pos = 0
        neg = 0
        muta = 0
        for line in fi:
            temp = line.split(',',len(line))

            if(mutation in temp[1]):
                muta = temp[2]

            temp[2] = float(temp[2][0:-2])
            if(temp[2] > 0):
                pos += temp[2]
            else:
                neg = neg + temp[2]

    with open('energy_ratio.csv','w') as fo:

        fo.write(str(muta))
        fo.write(str(pos) + "\n")
        fo.write(str(neg) + "\n")

if __name__ == "__main__":
    main(sys.argv)
