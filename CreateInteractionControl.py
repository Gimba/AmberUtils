#! /usr/bin/env python


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
