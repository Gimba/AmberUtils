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
import CalcResNum1iqd
from collections import Counter

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
    trajin_mutated_sim = args.trajin_mutated_simulation

    results_folder = 'contacts_' + unmutated_name + '_' + mutated_name + '/'

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    os.system("cp " + pdb_unmutated + " " + results_folder)
    os.system("cp " + pdb_mutated + " " + results_folder)
    os.system("cp " + trajin_unmutated + " " + results_folder)
    os.system("cp " + trajin_mutated_init + " " + results_folder)
    os.system("cp " + trajin_mutated_sim + " " + results_folder)
    os.chdir(os.getcwd() + '/' + results_folder)

    # get residues contacting the mutation residue
    model_contacts = create_contact_cpptraj(trajin_unmutated, [mutation], ['1-5000'])
    run_cpptraj(pdb_unmutated, trajin_unmutated, model_contacts[0])
    contact_atoms_init = get_atom_contacts(model_contacts[1], mutation)
    # residues = extract_residues(contact_atoms_init)


    # get atoms of contacting residues in contact with mutation residue
    atoms = extract_atoms(contact_atoms_init)


    # get occupancy of atoms contacting mutation residue
    model_atom_occupancy = create_contact_cpptraj(trajin_unmutated, atoms, ['1-5000'])
    run_cpptraj(pdb_unmutated, trajin_unmutated, model_atom_occupancy[0])
    occupancy_atoms_init = get_atom_contacts(model_contacts[1], '')
    init = get_atom_occupancy(occupancy_atoms_init)


    # get occupancy of atoms contating mutation residue after mutation
    muta_atom_occupancy = create_contact_cpptraj(trajin_mutated_init, atoms, ['1-5000'])
    run_cpptraj(pdb_mutated, trajin_mutated_init, muta_atom_occupancy[0])
    occupancy_atoms_muta_init = get_atom_contacts(muta_atom_occupancy[1], '')
    muta = get_atom_occupancy(occupancy_atoms_muta_init)


    # get occupancy of atoms contacting mutation residue after its mutation and after simulation ran
    muta_atom_occupancy_sim = create_contact_cpptraj(trajin_mutated_sim, atoms, ['1-5000'])
    run_cpptraj(pdb_mutated, trajin_mutated_sim, muta_atom_occupancy_sim[0])
    occupancy_atoms_muta_sim = get_atom_contacts(muta_atom_occupancy_sim[1], '')
    sim = get_atom_occupancy(occupancy_atoms_muta_sim)




    # model_contacts = create_contact_cpptraj(trajin_unmutated, residues, [mutation])
    # run_cpptraj(pdb_unmutated, trajin_unmutated, model_contacts[0])


    # model_contacts_init = create_contact_cpptraj(trajin_unmutated, atoms, ['1-5000'])
    # run_cpptraj(pdb_unmutated, trajin_unmutated, model_contacts_init[0])
    # contact_atoms_init = get_atom_contacts(model_contacts_init[1], '')
    # contact_atoms_init = convert_res_numbers(contact_atoms_init)
    contact_atoms_init = flip_residues(contact_atoms_init)

    # get mutation init contacts
    # muta_contacts_init = create_contact_cpptraj(trajin_mutated_init, residues, ['1-5000'])
    # run_cpptraj(pdb_mutated, trajin_mutated_init, muta_contacts_init[0])
    # contact_atoms_muta_init = get_atom_contacts(muta_contacts_init[1],'')
    # contact_atoms_muta_init = convert_res_numbers(contact_atoms_muta_init)

    # get mutation sim contacts
    # muta_contacts_sim = create_contact_cpptraj(trajin_mutated_sim, residues, ['1-5000'])
    # run_cpptraj(pdb_mutated, trajin_mutated_sim, muta_contacts_sim[0])
    # contact_atoms_muta_sim = get_atom_contacts(muta_contacts_sim[1], '')
    # contact_atoms_muta_sim = convert_res_numbers(contact_atoms_muta_sim)

    # compare results
    # lost_contacts_init = list(set(contact_atoms_init) - set(contact_atoms_muta_init))
    # new_contacts_init = list(set(contact_atoms_muta_init) - set(contact_atoms_init))
    #
    # lost_contacts_sim = list(set(contact_atoms_init) - set(contact_atoms_muta_sim))
    # new_contacts_sim = list(set(contact_atoms_muta_sim) - set(contact_atoms_init))

    # print sorted(lost_contacts_init)
    # print sorted(lost_contacts_sim)
    #
    # all_interesting = lost_contacts_sim + lost_contacts_init + new_contacts_init + new_contacts_sim
    # all_interesting = list(set(all_interesting))

    # output_results([trajin_unmutated, trajin_mutated_init, trajin_mutated_sim], contact_atoms_init,
    #                contact_atoms_muta_init, contact_atoms_muta_sim, lost_contacts_init)

    # output_results([trajin_unmutated, trajin_mutated_init, trajin_mutated_sim], contact_atoms_init,
    #                contact_atoms_muta_init, contact_atoms_muta_sim)


def get_atom_occupancy(occupancy_atoms):
    occupancy_atoms = [item.split('_')[0] for item in occupancy_atoms]
    out = Counter(occupancy_atoms)
    out = out.items()
    return out


def get_atom_contacts(data_file, residue):
    contact_atoms = []
    with open(data_file, 'r') as f:
        for line in f:
            if line[0] is not '#':
                # get lines which do not contain the mutation residue as contact itself (only consider extra mutation
                #  residue contacts)
                if "_:" + residue + "@" not in line:
                    # extract residue number from line
                    line = line.split(' ')
                    line = filter(None, line)
                    # line = line[1].split("_")[1]
                    # line = line.split('@')[0]
                    # line = line.replace(':', '')
                    line = line[1]
                    contact_atoms.append(line)

    return contact_atoms


def extract_atoms(contact_atoms):
    out = []

    for item in contact_atoms:
        # :23@N_:22@O -> :22@O
        item = item.split('_')[1]
        # :22@O -> 22@O
        item = item.replace(':', '')
        out.append(item)

    # consolidate same residues
    out = list(set(out))

    return out

def extract_residues(contact_atoms):
    contact_residues = []

    for item in contact_atoms:
        # :23@N_:22@O -> :22@O
        item = item.split('_')[1]
        # :22@O -> :22
        item = item.split('@')[0]
        # :22 -> 22
        item = item.replace(':', '')
        contact_residues.append(item)

    # consolidate same residues
    contact_residues = list(set(contact_residues))

    return contact_residues


def create_contact_cpptraj(trajin, res1, res2):

    cpptraj_file = trajin.split('.')[0] + "_contacts.cpptraj"
    out_file = cpptraj_file.replace('cpptraj', 'dat')

    with open(cpptraj_file, 'w') as f:
        f.write('strip :WAT\nstrip @H*\nstrip @?H*\n')
        for item1 in res1:
            for item2 in res2:
                f.write('nativecontacts :' + item1 + ' :' + item2 + ' writecontacts ' +
                    out_file + ' distance 3.9\n')
        f.write('go')

    return [cpptraj_file, out_file]


def run_cpptraj(pdb, trajin, cpptraj_file):
    os.system('cpptraj -p ' + pdb + ' -y ' + trajin + ' -i ' + cpptraj_file)


def flip_residues(contact_list):
    out_list = []
    for item in contact_list:
        item = item.split('_')
        out_list.append(item[1] + "_" + item[0])
    return out_list


def output_results(trajin, init, muta, prod, all_interesting):
    model = trajin[0].split('.')[0]
    mutant = trajin[1].split('.')[0]
    production = trajin[2]
    # F2196A_prod_20.rst -> 20.rst
    production = production.split('_')[-1]
    # 20.rst -> 20
    production = production.split('.')[0]
    # 20 -> 40
    production = str(int(production) * 2)
    # 40 -> F2196A 40ns
    production = mutant + " " + production + "ns"

    columns = ["atom", model, mutant, production]

    output = ""

    output = output + ', '.join(columns) + '\n'

    all_atoms = []

    all_atoms = init + muta + prod
    all_atoms = sorted(list(set(all_atoms)))

    all_atoms = list(set(all_atoms) & set(all_interesting))

    init_total = 0
    muta_total = 0
    prod_total = 0

    for item in all_atoms:
        output = output + item + ", "

        if item in init:
            output = output + "1, "
            init_total += 1
        else:
            output = output + "0, "

        if item in muta:
            output = output + "1, "
            muta_total += 1
        else:
            output = output + "0, "

        if item in prod:
            output = output + "1, "
            prod_total += 1
        else:
            output = output + "0, "

        output = output + "\n"
    output = output + "total:, "
    output = output + str(init_total) + ", " + str(muta_total) + ", " + str(prod_total) + "\n"


    outfile_name = model + "_" + mutant + "_results.dat"

    with open(outfile_name, 'w') as f:
        f.write(output)


def convert_res_numbers(contact_atoms):
    out_list = []
    for item in contact_atoms:
        item = item.split('_')
        temp0 = re.findall("\d+", item[0])[0]
        temp1 = re.findall("\d+", item[1])[0]

        temp0_new = CalcResNum1iqd.convert(temp0)
        temp1_new = CalcResNum1iqd.convert(temp1)

        item[0] = item[0].replace(temp0, temp0_new)
        item[1] = item[1].replace(temp1, temp1_new)

        out_list.append('_'.join(item))

    return out_list


if __name__ == "__main__":
    main(sys.argv)
