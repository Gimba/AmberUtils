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
import os

__author__ = 'Martin Rosellen'
__docformat__ = "restructuredtext en"

def main(argv):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('pdb_unmutated', help='unmutated structure')
    parser.add_argument('trajin_unmutated', help='trajectory for unmutated structure')
    parser.add_argument('pdb_mutated', help='mutated structure')
    parser.add_argument('trajin_mutated', help='trajectory for mutated structure')
    parser.add_argument('mutation', help='mutated structure')
    args = parser.parse_args()

    mutation = args.mutation
    trajin_unmutated = args.trajin_unmutated
    pdb_unmutated = args.pdb_unmutated

    pdb_mutated = args.pdb_mutated
    trajin_mutated = args.trajin_mutated
    unmutated_name = pdb_unmutated.split('.')[0]

    contact_muta_res_dat = unmutated_name + '_' + mutation + '_contacts.dat'
    contact_muta_res_cpptraj = unmutated_name + '_' + mutation + '.cpptraj'

    # generate cpptraj infile to get contacting residues of the selected/mutated residue
    with open(contact_muta_res_cpptraj, 'w') as f:
        f.write('strip :WAT\nstrip @H*\nstrip @?H*\nnativecontacts :' + mutation + ' :1-50000 writecontacts ' +
                contact_muta_res_dat + ' distance 3.9\ngo')

    # run cpptraj
    os.system('cpptraj -p ' + pdb_unmutated + ' -y ' + trajin_unmutated + ' -i ' + contact_muta_res_cpptraj)

    # get contact residues and occupancy of atoms for unmutated structure from contact_data file generated by cpptraj
    contact_residues = []

    with open(contact_muta_res_dat, 'r') as f:
        for line in f:
            if line[0] is not '#':
                # get extra residue contacts
                if "_:" + mutation + "@" not in line:
                    line = line.split(' ')
                    line = filter(None, line)
                    line = line[1].split("_")[1]
                    line = line.split('@')[0]
                    line = line.replace(':', '')
                    contact_residues.append(line)


    # store number/occupancy of mutation contacting atoms
    contact_atom_count = []
    for item in contact_residues:
        contact_atom_count.append([item, contact_residues.count(item)])

    contact_residues = list(set(contact_residues))

    # get contact count for mutated structure (not really necessary)

    # mutated = []
    #
    # with open(args.mutated, 'r') as f:
    #     for line in f:
    #         if line[0] is not '#':
    #             # get extra residue mutated
    #             if "_:23@" not in line:
    #                 line = line.split(' ')
    #                 line = filter(None, line)
    #                 line = line[1].split("_")[1]
    #                 line = line.split('@')[0]
    #                 line = line.replace(':', '')
    #                 mutated.append(line)
    #
    #
    # mutated_atoms = []
    # for item in residues:
    #     mutated_atoms.append([item, mutated.count(item)])
    # mutated = list(set(mutated))

    occupancy1 = get_atom_occupancy(pdb_unmutated, trajin_unmutated, contact_residues, mutation)
    occupancy2 = get_atom_occupancy(pdb_mutated, trajin_mutated, contact_residues, mutation)

    total1 = 0
    total2 = 0
    total_mutation = 0
    tuples1 = []
    tuples2 = []
    for triple1 in occupancy1:
        for triple2 in occupancy2:
            tuples1.append(triple1[0] + '_' + triple1[1])
            tuples2.append(triple2[0] + '_' + triple2[1])
            if triple1[0] == triple2[0] and triple1[1] == triple2[1]:
                total1 += triple1[2]
                total2 += triple2[2]
                # a negative value means that the initial structure has lost this number of contacts
                diff = triple2[2] - triple1[2]
                print triple1[0] + " " + triple1[1] + " " + str(diff)
                if triple2[1] == mutation:
                    total_mutation += triple2[2] - triple1[2]

    # manage lost contacts which show not up in mutated occupancy
    tuples1 = set(tuples1)
    tuples2 = set(tuples2)

    lost_contacts = list(tuples1 - tuples2)

    print "lost contacts"
    for tuple in lost_contacts:
        res1 = tuple.split('_')[0]
        res2 = tuple.split('_')[1]
        for triple in occupancy1:
             if triple[0] == res1 and triple[1] == res2:
                 print res1 + " " + res2 + " " + str(0 - triple[2])

    print "total unmutated " + str(total1)
    print "total mutated " + str(total2)
    print "total mutation " + str(total_mutation)


def get_atom_occupancy(pdb, trajin, contact_residues, mutation):

    res_muta_contact_cpptraj = "contact_residues_" + mutation + ".cpptraj"

    # generate cpptraj to get contacts of residues in contact with the mutation
    contact_outfiles = []
    with open(res_muta_contact_cpptraj, 'w') as out:
        out.write('strip :WAT\nstrip @H*\nstrip @?H*\n')
        for item in contact_residues:
            contact_outfiles.append("contacts_" + item + ".dat")
            out.write("nativecontacts :" + item + " :1-50000 writecontacts contacts_" + item +
                      ".dat distance 3.9\n")
        out.write("go")

    os.system('cpptraj -p ' + pdb + ' -y ' + trajin + ' -i ' + res_muta_contact_cpptraj)

    # get total of atomic contacts of residues contacting the mutation

    # all_residue_contacts contains triples, first is the selected residue, second is a contacting residue,
    # and third the number of contacts between the two residues
    all_residue_contacts = []
    for contact_file in contact_outfiles:
        residue_contacts = []
        residue = contact_file.split('_')[1].split('.')[0]
        with open(contact_file, 'r') as f:
            for line in f:
                if line[0] is not '#':
                    # get extra residue contacts
                    if "_:" + residue + "@" not in line:
                        line = line.split(' ')
                        line = filter(None, line)
                        line = line[1].split("_")[1]
                        line = line.split('@')[0]
                        line = line.replace(':', '')
                        residue_contacts.append(line)

        residue_contacts_unique = list(set(residue_contacts))
        for item in residue_contacts_unique:
            all_residue_contacts.append([residue, item, residue_contacts.count(item)])
    return all_residue_contacts

if __name__ == "__main__":
    main(sys.argv)
