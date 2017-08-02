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


import argparse
import os
import re
import sys
from collections import Counter

import CalcResNum1iqd
import CpptrajHelper as cpp
import PdbHelper as pdb

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

    prmtop_init = args.pdb_unmutated
    unmutated_name = prmtop_init.split('.')[0]
    trajin_init = args.trajin_unmutated

    prmtop_muta = args.pdb_mutated
    mutated_name = prmtop_muta.split('.')[0]
    trajin_muta = args.trajin_mutated_init
    trajin_sim = args.trajin_mutated_simulation

    results_folder = 'contacts_' + unmutated_name + '_' + mutated_name + '/'

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    os.system("cp " + prmtop_init + " " + results_folder)
    os.system("cp " + prmtop_muta + " " + results_folder)
    os.system("cp " + trajin_init + " " + results_folder)
    os.system("cp " + trajin_muta + " " + results_folder)
    os.system("cp " + trajin_sim + " " + results_folder)
    os.chdir(os.getcwd() + '/' + results_folder)

    # get a list of all atoms of all residues
    pdb_file_unmutated = cpp.generate_pdb(prmtop_init, trajin_init)
    atom_list_unmutated = pdb.read_pdb_atoms(pdb_file_unmutated)

    # get a list of types present in a atom list
    types = pdb.get_all_atom_types(atom_list_unmutated)

    avrg_init = get_contact_averages_of_types(prmtop_init, trajin_init, types)

    avrg_muta = get_contact_averages_of_types(prmtop_muta, trajin_muta, types)

    avrg_sim = get_contact_averages_of_types(prmtop_muta, trajin_sim, types)

    print output_2D_list(avrg_init)
    print output_2D_list(avrg_muta)
    print output_2D_list(avrg_sim)


    # get mutation contacting atoms
    # model_contacts = cpp.create_contact_cpptraj(trajin_init, [mutation], ['1-5000'])
    # cpp.run_cpptraj(prmtop_init, trajin_init, model_contacts[0])
    # contact_atoms_init = get_atom_contacts(model_contacts[1], mutation)
    # residues = extract_residues(contact_atoms_init)

    # get atoms in contact with mutation residue
    # atoms = extract_atoms(contact_atoms_init)

    # get occupancy of atoms contacting mutation residue
    # model_atom_occupancy = cpp.create_contact_cpptraj(trajin_init, atoms, ['1-5000'])
    # cpp.run_cpptraj(pdb_unmutated, trajin_unmutated, model_atom_occupancy[0])
    # contacts_init = get_atom_contacts(model_atom_occupancy[1], '')
    # init = get_atom_occupancy(contacts_init)

    # get occupancy of atoms contating mutation residue after mutation
    # muta_atom_occupancy = cpp.create_contact_cpptraj(trajin_muta, atoms, ['1-5000'])
    # cpp.run_cpptraj(pdb_mutated, trajin_mutated_init, muta_atom_occupancy[0])
    # contacts_muta = get_atom_contacts(muta_atom_occupancy[1], '')
    # muta = get_atom_occupancy(contacts_muta)


    # get occupancy of atoms contacting mutation residue after its mutation and after simulation ran
    # muta_atom_occupancy_sim = cpp.create_contact_cpptraj(trajin_sim, atoms, ['1-5000'])
    # cpp.run_cpptraj(pdb_mutated, trajin_mutated_sim, muta_atom_occupancy_sim[0])
    # contacts_sim = get_atom_contacts(muta_atom_occupancy_sim[1], '')
    # sim = get_atom_occupancy(contacts_sim)

    # print output_occupancy_averages(avrg_init, init, types)

    # get total distances of mutation contacting atoms
    # total_dist_init = quantify_distances(model_atom_occupancy[1])
    # total_dist_muta = quantify_distances(muta_atom_occupancy[1])
    # total_dist_sim = quantify_distances(muta_atom_occupancy_sim[1])

    # categorize distances of contacts
    # init_muta_contacts = quantify_distances_of_contacts(model_atom_occupancy[1], muta_atom_occupancy[1])
    # init_sim_contacts = quantify_distances_of_contacts(model_atom_occupancy[1], muta_atom_occupancy_sim[1])

    # print output_quantify(init_muta_contacts, init_sim_contacts, [total_dist_init, total_dist_muta, total_dist_sim])
    # find atoms that are not present in all three data sets. The resulting list of interesting atoms contains only
    # those ones that changed their occupancy as an effect of mutation or simulation
    # interesting = get_interesting_atoms(contacts_init, contacts_muta, contacts_sim)

    # interesting = convert_res_numbers(interesting)
    # contacts_init = convert_res_numbers(contacts_init)
    # contacts_muta = convert_res_numbers(contacts_muta)
    # contacts_sim = convert_res_numbers(contacts_sim)

    # output_results([trajin_init, trajin_muta, trajin_sim], contacts_init, contacts_muta, contacts_sim, interesting)


# returns the averages for all types of atoms in a given prmtop file and trajectory
def get_contact_averages_of_types(prmtop, trajin, types):
    pdb_file_mutated = cpp.generate_pdb(prmtop, trajin)
    atom_list_mutated = pdb.read_pdb_atoms(pdb_file_mutated)
    residue_atom_list_mutated = cpp.create_all_atom_residue_list(atom_list_mutated, types)
    model_contacts_mutated = cpp.create_contact_cpptraj(trajin, residue_atom_list_mutated, ['1-5000'])
    cpp.run_cpptraj(prmtop, trajin, model_contacts_mutated[0])
    avrgs = get_occupancy_averages_of_types(model_contacts_mutated[1], types)
    return avrgs


def output_2D_list(list2d):
    output = ""
    for item in list2d:
        output += str(item[0]) + "," + str(item[1]) + "\n"
    return output


def output_occupancy_averages(avrgs, occs, types):
    output = ""

    for t in types:
        output += t + ", "
        for avg in avrgs:
            if t == avg[0]:
                output += str(avg[1]) + ", "
        output += "\n"
    return output


# calculates the average of contacts of types in the given data
def get_occupancy_averages_of_types(data_file, types):
    data = cpp.read_cpptraj_contacts_data(data_file)

    type_occupancy_average = []
    for item in types:
        residue_types = []
        for line in data:
            temp = line[0][0].split('@')[1]
            if item == temp:
                residue_types.append(line[0][0])
        if len(residue_types) != 0:
            type_occupancies = Counter(residue_types).values()
            average = sum(type_occupancies) / float(len(type_occupancies))
            type_occupancy_average.append([item, average])

    return type_occupancy_average


def output_quantify(init_muta, init_sim, totals):
    output = ""
    counter = -1
    header = ["lost far", "gained far","lost middle", "gained middle", "lost close", "gained close"]
    for item in init_sim:
        counter += 1
        head_line = header[counter] + " values: init -> muta \n"
        output += head_line
        for contact in item:
            output += contact[0] + " " + str(contact[1]) + "\n"
        output += header[counter] + " contacts: " + str(len(item)) + "\n\n"

    total = 0
    totalo = []

    # for item1 in totals[0]:
    #     for item2 in totals[1]:
    #         if item1[0] == item2[0]:
    #             print str(item1[1] - item2[1])

    # for list in totals:
    #     for item in list:
    #         total += item[1]
    #     totalo.append(total)
    #     total = 0
    # print totalo
    # exit()
    return output

# returns amount of distance change
def quantify_distances(contacts_data):

    distances = []

    with open(contacts_data, 'r') as f:
        count = 0
        last_atom = ""
        for line in f:
            if line[0] is not '#':
                line = line.split()
                atom = line[1].split('_')
                atom = atom[0].replace(':', '')
                dist = line[4]
                if last_atom == "":
                    last_atom = atom
                if last_atom != atom:
                    distances.append([atom, count])
                    count = 0
                    last_atom = atom
                else:
                    count = count + float(dist)
    return distances

# return amount fo distance lost in each distance category
def quantify_distances_of_contacts(data1, data2):
    data1_categorized = categorize_contacts(data1)
    data2_categorized = categorize_contacts(data2)

    data1_far_keys = [item[0] for item in data1_categorized[0]]
    # # data1_far_values = [item[1] for item in data1_categorized[0]]
    #
    data2_far_keys = [item[0] for item in data2_categorized[0]]

    lost_far = non_mutual(data1_categorized[0], data2_categorized[0])
    gain_far = non_mutual(data2_categorized[0], data1_categorized[0])

    lost_middle = non_mutual(data1_categorized[1], data2_categorized[1])
    gain_middle = non_mutual(data2_categorized[1], data1_categorized[1])

    lost_close = non_mutual(data1_categorized[2], data2_categorized[2])
    gain_close = non_mutual(data2_categorized[2], data1_categorized[2])

    return [lost_far, gain_far, lost_middle, gain_middle, lost_close, gain_close]


# expecting lists with keys in first and values in second column
def non_mutual(list1, list2):
    keys1 = [item[0] for item in list1]
    keys2 = [item[0] for item in list2]
    non_mutuals = list(set(keys1) ^ set(keys2))

    out = []

    for item1 in non_mutuals:
        for item2 in list1:
            if item1 == item2[0]:
                out.append(item2)

    return out


def categorize_contacts(contacts_data):
    far = []
    middle = []
    close = []

    with open(contacts_data, 'r') as f:
        for line in f:
            if line[0] is not '#':
                line = line.split()
                atom = line[1]
                dist = float(line[4])

                # categorize contacts due to distance
                if dist > 3.8:
                    far.append([atom, dist])
                elif dist > 3.0:
                    middle.append([atom, dist])
                else:
                    close.append([atom, dist])

    return [far, middle, close]


# returns spatially sorted distance list
def spatialize_distances():
    pass


# show trend over time
def trendify_distances():
    pass


def get_interesting_atoms(init, muta, sim):
    init_muta = list(set(init)^set(muta))
    init_sim = list(set(init)^set(sim))
    interesting = list(set(init_muta + init_sim))
    return interesting


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
        if item.split('@')[0] != '23':
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

    all_atoms = sorted(list(set(all_atoms) & set(all_interesting)))

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
            output = output + "1"
            prod_total += 1
        else:
            output = output + "0"

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
