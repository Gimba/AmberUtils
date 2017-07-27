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
import re

__author__ = 'Martin Rosellen'
__docformat__ = "restructuredtext en"

def main(argv):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('pdb_unmutated', help='unmutated structure')
    parser.add_argument('trajin_unmutated', help='trajectory for unmutated structure')
    parser.add_argument('pdb_mutated', help='mutated structure')
    parser.add_argument('trajin_mutated_init', help='trajectory for mutated structure')
    parser.add_argument('trajin_mutated_simulation', help='trajectory for mutated structure after simulation')
    parser.add_argument('mutation', help='mutated structure')
    args = parser.parse_args()

    mutation = args.mutation

    pdb_unmutated = args.pdb_unmutated
    unmutated_name = pdb_unmutated.split('.')[0]
    trajin_unmutated = args.trajin_unmutated

    pdb_mutated = args.pdb_mutated
    mutated_name = pdb_mutated.split('.')[0]
    trajin_mutated_init = args.trajin_mutated_init
    trajin_mutated_simulation = args.trajin_mutated_simulation

    results_folder ='contacts_' + unmutated_name + '_' + mutated_name + '/'

    contact_muta_res_dat = results_folder + unmutated_name + '_' + mutated_name + '_contacts.dat'
    contact_muta_res_cpptraj = results_folder + unmutated_name + '_' + mutated_name + '.cpptraj'


    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    contact_residues = get_contacting_residues(contact_muta_res_cpptraj, mutation, contact_muta_res_dat,
                                               pdb_unmutated, trajin_unmutated)

    # wild-type
    occupancy1 = get_residue_occupancy(pdb_unmutated, trajin_unmutated, contact_residues, mutation, results_folder)

    # mutant
    occupancy2 = get_residue_occupancy(pdb_mutated, trajin_mutated_init, contact_residues, mutation, results_folder)

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

    # manage lost contacts which show not up in mutated occupancy
    tuples1 = set(tuples1)
    tuples2 = set(tuples2)

    # get all elements that are in tuples1 but not in tuples2
    lost_contacts = list(tuples1 - tuples2)

    lost_residue_contacts = []
    for tuple in lost_contacts:
        # retrieve triples from occupancy data
        res1 = tuple.split('_')[0]
        res2 = tuple.split('_')[1]
        for triple in occupancy1:
            if triple[0] == res1 and triple[1] == res2 and triple[1] == mutation:
                total1 += triple2[2]
                lost_residue_contacts.append(triple)

    contact_atoms = extract_contact_atoms(lost_residue_contacts, mutation, results_folder, pdb_unmutated)
    contact_atoms = list(set(contact_atoms))
    atom_occupancy1 = get_atom_occupancy(contact_atoms, pdb_unmutated, trajin_unmutated, results_folder)
    atom_occupancy2 = get_atom_occupancy(contact_atoms, pdb_mutated, trajin_mutated_simulation, results_folder)

    print lost_residue_contacts
    print atom_occupancy1
    print atom_occupancy2

    for item1 in atom_occupancy1:
        for item2 in atom_occupancy2:
            item1 = item1.replace('.dat','')
            i1 = re.split('_|\.| ', item1)
            item2 = item2.replace('.dat', '')
            i2 = re.split('_|\.| ', item2)
            if i1[3] == i2[3]:
                print i1[3] + ' ' + str(int(i2[4]) - int(i1[4]))
    # print "total unmutated " + str(total1)
    # print "total mutated " + str(total2)


def get_contacting_residues(contact_muta_res_cpptraj, mutation, contact_muta_res_dat, pdb_unmutated, trajin_unmutated ):
    # generate cpptraj infile to get contacting residues of the selected/mutated residue
    with open(contact_muta_res_cpptraj, 'w') as f:
        f.write('strip :WAT\nstrip @H*\nstrip @?H*\nnativecontacts :' + mutation + ' :1-50000 writecontacts ' +
                contact_muta_res_dat + ' distance 3.9\ngo')

    # run cpptraj to create a file that contains all the residues (with atoms) in contact with the specified mutation
    # residue
    os.system('cpptraj -p ' + pdb_unmutated + ' -y ' + trajin_unmutated + ' -i ' + contact_muta_res_cpptraj)

    # get contact residues and occupancy of atoms for unmutated structure from contact_data file generated by cpptraj
    contact_residues = []
    with open(contact_muta_res_dat, 'r') as f:
        for line in f:
            if line[0] is not '#':
                # get lines which do not contain the mutation residue as contact itself (only consider extra mutation
                #  residue contacts)
                if "_:" + mutation + "@" not in line:

                    # extract residue number from line
                    line = line.split(' ')
                    line = filter(None, line)
                    line = line[1].split("_")[1]
                    line = line.split('@')[0]
                    line = line.replace(':', '')
                    contact_residues.append(line)


    # store number of contacts of a selected residue with mutation residue
    contact_atom_count = []
    for item in contact_residues:
        contact_atom_count.append([item, contact_residues.count(item)])

    contact_residues = list(set(contact_residues))

    return contact_residues

def get_residue_occupancy(pdb, trajin, contact_residues, mutation, results_folder):

    res_muta_contact_cpptraj = results_folder + pdb.split('.')[0] + "contact_residues_" + mutation + ".cpptraj"

    # generate cpptraj to get contacts of residues in contact with the mutation
    contact_outfiles = []
    with open(res_muta_contact_cpptraj, 'w') as out:
        out.write('strip :WAT\nstrip @H*\nstrip @?H*\n')
        for item in contact_residues:
            outfile = results_folder + pdb.split('.')[0] + "_contacts_" + item + ".dat"
            contact_outfiles.append(outfile)
            out.write("nativecontacts :" + item + " :1-50000 writecontacts " + outfile + " distance 3.9\n")
        out.write("go")

    os.system('cpptraj -p ' + pdb + ' -y ' + trajin + ' -i ' + res_muta_contact_cpptraj)

    # get total of atomic contacts of residues contacting the mutation

    # all_residue_contacts contains triples, first is the selected residue, second is a contacting residue,
    # and third the number of contacts between the two residues
    all_residue_contacts = []
    for contact_file in contact_outfiles:
        residue_contacts = []
        residue = contact_file.split('_')[4].split('.')[0]
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


def extract_contact_atoms(lost_contact_atoms, mutation, results_folder, pdb):
    contact_atoms = []
    for item in lost_contact_atoms:
        residue = item[0]
        with open(results_folder + pdb.split('.')[0] + "_contacts_" + residue + ".dat", 'r') as f:
            for line in f:
                if "_:" + mutation + "@" in line:
                    contact_atoms.append(line.split(':')[1].replace('_', ''))
    return contact_atoms


def get_atom_occupancy(contact_atoms, pdb, trajin, results_folder):

    cpptraj = results_folder + 'contact_atoms.cpptraj'

    outfiles = []
    with open(cpptraj, 'w') as f:
        f.write("strip :WAT\nstrip @H*\nstrip @?H*\n")
        for item in contact_atoms:
            outfile_name = results_folder + pdb.split('.')[0] + "_" + item + ".dat"
            outfiles.append(outfile_name)
            f.write("nativecontacts :" + item + " :1-50000 writecontacts " + outfile_name + " distance 3.9\n")
        f.write("go")
    os.system('cpptraj -p ' + pdb + ' -y ' + trajin + ' -i ' + cpptraj)

    atom_occupancy = []
    for item in outfiles:
        with open(item, 'r') as f:
            lines = f.read().splitlines()
            lines = [x for x in lines if not x.startswith('#')]
            atom_occupancy.append(item + " " + str(len(lines)))
    return sorted(list(set(atom_occupancy)))


if __name__ == "__main__":
    main(sys.argv)
