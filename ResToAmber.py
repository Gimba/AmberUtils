#! /usr/bin/env python

# Copyright (c) 2015 William Lees

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

__author__ = 'William Lees'
__docformat__ = "restructuredtext en"

import sys
import os
import argparse


def main(argv):
    parser = argparse.ArgumentParser(description='Analyse the protonation of histidines in a PDB file and produce a control file for ConvertRes'
            ' that will rename HIS residues to Amber standards. Analyse SSBOND records and produce control file records that will rename corresponding'
            ' CYS records to CYX.')
    parser.add_argument('infile', help='input file (PDB format')
    parser.add_argument('outfile', help='output file (ConvertRes control file format)')
    args = parser.parse_args()
    
    histnum = None
    found_HD1 = False
    found_HE2 = False
    ssbonds = {}
    
    with open(args.infile, "r") as f, open(args.outfile, "w") as cf:
        for line in f:
            if len(line) >= 26 and line[:6] == 'ATOM  ':
                resname = line[17:20]
                resnum = line[22:27].strip()
                chain = line[21]
                atomname = line[12:16].strip()
                if histnum and histnum != resnum:
                    histype = None
                    if found_HD1 and found_HE2:
                        histype = 'HIP'
                    elif found_HD1:
                        histype = 'HID'
                    elif found_HE2:
                        histype = 'HIE'

                    if histype:
                        cf.write("%s %s %s\n" % (histnum, hischain, histype))
                    else:
                        print 'HIS at chain %s residue %s has no HD1 or HE2.' % (chain, histnum)
                    histnum = None
                if resname == 'HIS':
                    if not histnum:
                        found_HD1 = False
                        found_HE2 = False
                        histnum = resnum
                        hischain = chain
                    if atomname == 'HD1':
                        found_HD1 = True
                    elif atomname == 'HE2':
                        found_HE2 = True
            elif len(line) >= 35 and line[0:6] == 'SSBOND':
                chain1 = line[15]
                num1 = line[17:22].strip()
                chain2 = line[29]
                num2 = line[31:35].strip()
                ssbonds[chain1+num1] = (chain1, num1)
                ssbonds[chain2+num2] = (chain2, num2)

        if histnum and histnum != resnum:
            histype = None
            if found_HD1 and found_HE2:
                histype = 'HIP'
            elif found_HD1:
                histype = 'HID'
            elif found_HE2:
                histype = 'HIE'

            if histype:
                cf.write('%d %s %s\n' % (histnum, hischain, histype))
            else:
                print 'HIS at %d has no HD1 or HE2.' % histnum

        for (chain, num) in ssbonds.values():
            cf.write("%s %s %s\n" % (num, chain, 'CYX'))


if __name__ == "__main__":
    main(sys.argv)
