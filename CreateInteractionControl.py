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


entries = []

with open('hbonds_consol.csv', 'r') as fo:
    for line in fo:
        entries.append(line[0:7])
        entries.append(line[8:15])
    entries = list(set(entries))

with open('FINAL_DECOMP_MMPBSA_table.csv', 'r') as fo:
    head = fo.readline()
    # remove /r/n at the end of line
    head = head[0:-2]

    # split at ,
    head = head.split(',',len(head))

    # remove first entry "Res"
    head = head[1:]

    entries.extend(head)

    entries = list(set(entries))

out_lines = []

# assign residues to columns
for entry in entries:
    resnum = int(entry[-3:])
    if(int(entry[-3:]) < 156):
        out_lines.append("0," + entry + "," + str(resnum + 2173) + ",Hydro")
    else:
        if(resnum <= 367):
            resnum = resnum - 156
        else:
            resnum = resnum - 367
        out_lines.append("1," + entry + "," + str(resnum) + ",Hydro")

# sort so that first column residues appear first in the control file

with open('1iqd_interactions_control.csv', 'w') as out:
    out.writelines("Col,Id,Legend,Fill" + '\n')
    for line in out_lines:
        out.writelines(line + '\n')
