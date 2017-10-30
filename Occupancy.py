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

import cairo
from PyPDF2 import PdfFileMerger

__author__ = 'Martin Rosellen'
__docformat__ = "restructuredtext en"


def main(argv):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-r', '--residue', help='investigated residue')
    parser.add_argument('-i', '--input', nargs='?', help='list of inputs (e.g. model1.prmtop model1.incprd, mutation.prmtop, prod_1.nc 1 20, ...')
    parser.add_argument('-a', '--avrgs', help='calculate averages', action='store_true')
    parser.add_argument('-w', '--wat', help='strip water', action='store_true')
    parser.add_argument('-hy', '--hydro', help='strip hydrogen', action='store_true')
    args = parser.parse_args()

    input_list = args.input
    input_list = parse_input_list(input_list)

    investigated_residue = args.residue

    avrgs = 0
    wat = 0
    hydro = 0

    if args.avrgs:
        avrgs = args.avrgs
    print "calculate averages " + str(bool(avrgs))

    if args.wat:
        wat = args.wat
    print "strip water " + str(bool(wat))

    if args.hydro:
        hydro = args.hydro
    print "strip hydrogen " + str(bool(hydro))

    results_folder = 'occupancies/'

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    for item in input_list:
        os.system("cp " + item[0] + " " + results_folder)
        os.system("cp " + item[1] + " " + results_folder)

    os.chdir(os.getcwd() + '/' + results_folder)

    ##### get occupancy averages of types #####

    # get a list of all atoms of all residues
    pdb_file_unmutated = generate_pdb(input_list[0][0], input_list[0][1], wat, hydro)
    atom_list_unmutated = read_pdb_atoms(input_list[0][0], wat)

    # get a list of all residues with residue numbers
    residues = get_all_residues(atom_list_unmutated)

    # convert residue numbers
    temp = []
    for item in residues:
        temp.append(item.split(','))

    residues = temp
    res_numbers = c_get(residues, 1)
    residues = c_del(residues, 1)
    residues = c_bind(residues, res_numbers)
    types = convert_res_types(c_get(residues, 0))
    residues = c_del(residues, 0)
    residues = c_bind(types, residues)

    # atoms in contact with the to-be substituted residue (contacting atoms)
    atoms = get_contacting_atoms(input_list[0][0], input_list[0][1], investigated_residue, wat, hydro)

    # get types of contacting atoms
    atom_types = get_atom_types(atoms)

    # get non solvent residues for quicker computation, since otherwise contacts between solvent molecules would be
    # calculated as well
    non_solvent_residues = get_non_solvent_residues(pdb_file_unmutated)
    # TODO: proper calculation of residue number spans (e.g. 1-30, 69-399, etc.)
    mask1 = str(non_solvent_residues[0]) + "-" + str(non_solvent_residues[-1])

    # mask2 set to an arbitrary high value to include all possible contacts
    mask2 = "1-50000"

    ##### get occupancy of atoms in contact with the mutation #####
    occs = []
    averages = []
    for item in input_list:
        if len(item) < 3:
            # get occupancy of atoms contacting mutation residue
            occs.append(get_occupancy_of_atoms(item[0], item[1], atoms, wat, hydro))
            if avrgs:
                averages.append(get_contact_averages_of_types(item[0], item[1], atom_types, mask1, mask2, wat, hydro))

        else:
            # get occupancy of atoms contacting mutation residue after its mutation and after simulation ran selecting
            # frames
            trajin = "\"" + item[1] + " " + item[2] + " " + item[3] + "\""
            occs.append(get_occupancy_of_atoms(item[0], trajin, atoms, wat, hydro))

            if avrgs:
                trajin = "\"" + item[1] + " " + item[2] + " " + item[3] + "\""
                averages.append(get_contact_averages_of_types(item[0], trajin, atom_types, mask1, mask2, wat, hydro))

    ##### reformat data #####
    # create list with residue, atom identifier and occupancies
    occ_list = []
    for item in occs:
        if not occ_list:
            occ_list = c_get(item, 0)
        occ_list = c_bind(occ_list, c_get(item, 1))

    res_numb = c_get(occ_list, 0)
    occ_list = c_del(occ_list, 0)
    occ_list = c_bind(res_numb, occ_list)

    if avrgs:
        for item in averages:
            occ_list = add_averages_column(occ_list, item)

    occ_list = sorted(occ_list)

    top_header = ["", "", "Occupancies", ""]
    if avrgs:
        top_header.extend(["", "Averages", "", ""])

    header = ["Atom", "#0", "#1", "#2"]

    if avrgs:
        header.extend(["#0", "#1", "#2"])
    occ_list = [header] + occ_list
    occ_list = [top_header] + occ_list

    # format output
    output = output_2D_list(occ_list)
    output = prepare_output(output, avrgs)
    output = add_residue_types(output, residues)

    # write output
    write_output(output, input_list[1][0].split('.')[0] + '_occupancies.dat')
    output_to_pdf(output, input_list[1][0].split('.')[0] + '_occupancies.dat', avrgs, wat, hydro, input_list, investigated_residue)


def add_averages_column(lst, avrgs):
    outlist = []
    for item in lst:
        for avrg in avrgs:
            if item[0].split('@')[1] == avrg[0]:
                item.append(avrg[1])
                outlist.append(item)

    return outlist


def get_occupancy_of_atoms(prmtop, trajin, atoms, wat, hydro):
    model_atom_occupancy = create_contact_cpptraj(trajin, atoms, ['1-500000'], wat, hydro)
    run_cpptraj(prmtop, trajin, model_atom_occupancy[0])
    contacts_init = get_atom_contacts(model_atom_occupancy[1], '')

    # calculate number of frames if range is specified in trajectory
    frames = 1
    trajin = trajin.replace("\"", "")
    trajin = trajin.split()
    if len(trajin) > 1 and "inpcrd" not in trajin[0]:
        frames = (int(trajin[2]) + 1) - int(trajin[1])

    occupancy = get_atom_occupancy(contacts_init, frames)

    return occupancy


# get atoms in contact with specified residue
def get_contacting_atoms(prmtop, trajin, residue, wat, hydro):
    model_contacts = create_contact_cpptraj(trajin, [residue], ['1-500000'], wat, hydro)
    run_cpptraj(prmtop, trajin, model_contacts[0])
    contact_atoms_init = get_atom_contacts(model_contacts[1], residue)
    atoms = extract_atoms(contact_atoms_init)
    return atoms


# returns the averages for all types of atoms in a given prmtop file and trajectory
def get_contact_averages_of_types(prmtop, trajin, types, mask1, mask2, wat, hydro):
    model_contacts_mutated = create_contact_cpptraj_types(trajin, types, mask1, mask2, wat, hydro)
    run_cpptraj(prmtop, trajin, model_contacts_mutated[0])
    avrgs = get_occupancy_averages_of_types(model_contacts_mutated[1], types)
    return avrgs


# calculates the average of contacts of types in the given data
def get_occupancy_averages_of_types(data_file, types):
    data = read_cpptraj_contacts_data(data_file)

    type_occupancy_average = []
    for item in types:
        residue_types = []
        for line in data:
            temp = line[0][0].split('@')[1]
            if item == temp:
                residue_types.append(line[0][0])
        if len(residue_types) != 0:
            type_occupancies = Counter(residue_types).values()
            average = round(sum(type_occupancies) / float(len(type_occupancies)), 2)
            type_occupancy_average.append([item, average])

    return type_occupancy_average


def output_quantify(init_muta, init_sim, totals):
    output = ""
    counter = -1
    header = ["lost far", "gained far", "lost middle", "gained middle", "lost close", "gained close"]
    for item in init_sim:
        counter += 1
        head_line = header[counter] + " values: init -> muta \n"
        output += head_line
        for contact in item:
            output += contact[0] + " " + str(contact[1]) + "\n"
        output += header[counter] + " contacts: " + str(len(item)) + "\n\n"

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


def get_interesting_atoms(init, muta, sim):
    init_muta = list(set(init) ^ set(muta))
    init_sim = list(set(init) ^ set(sim))
    interesting = list(set(init_muta + init_sim))
    return interesting


def get_atom_occupancy(occupancy_atoms, frames):
    # occupancy_atoms = [item[0].split('_')[0] for item in occupancy_atoms]
    counter = 0.0
    last_atom = ""
    out = []
    for item in occupancy_atoms:
        atom = item[0].split('_')[0]
        contacts = float(item[1])
        if last_atom == "":
            last_atom = atom
        if last_atom == atom:
            counter += contacts
        else:
            out.append([atom, round((counter / frames),2)])
            counter = 0.0
            last_atom = atom

    return out


# transform cpptraj writecontacts data file into list
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
                    atom = line[1]
                    contacts = line[2]
                    contact_atoms.append([atom, contacts])

    return contact_atoms


def extract_atoms(contact_atoms):
    out = []

    for item in contact_atoms:
        # :23@N_:22@O -> :22@O
        item = item[0].split('_')[1]
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


def write_results(trajin, init, muta, prod, all_interesting):
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


def write_output(output, file_name):
    with open(file_name, 'w') as f:
        f.write(output)


def prepare_output(output, avrgs):
    output = output.splitlines()
    init_tot = 0
    muta_tot = 0
    sim_tot = 0
    init_res = 0
    muta_res = 0
    sim_res = 0

    if avrgs:
        avg_init_tot = 0
        avg_sim_tot = 0
        avg_muta_tot = 0
        avg_init_res = 0
        avg_sim_res = 0
        avg_muta_res = 0

    last_res = ""
    out = ""

    for line in output:
        l = line
        if line[0] == ':':
            line = line.split(',')
            init_tot += float(line[1])
            muta_tot += float(line[2])
            sim_tot += float(line[3])

            if avrgs:
                avg_init_tot += float(line[4])
                avg_muta_tot += float(line[5])
                avg_sim_tot += float(line[6])

            res = line[0].split('@')[0]
            if last_res == "":
                last_res = res

            # behavior if a new residue starts
            if last_res != res:
                last_res = res

                # add line with sum of contacts a selected residue
                out += "SUM," + str(init_res) + "," + str(muta_res) + "," + str(sim_res)
                if avrgs:
                    out += "," + str(avg_init_res) + "," + str(avg_muta_res) + "," + str(avg_sim_res)
                out += "\n"

                # add line with percentage values
                muta_res_per = (init_res - muta_res) * 100 / init_res
                sim_res_per = (init_res - sim_res) * 100 / init_res

                out += ",," + str(round(muta_res_per, 2)) + "%," + str(round(sim_res_per, 2)) + "%"
                if avrgs:
                    avg_muta_res_per = (avg_init_res - avg_muta_res) * 100 / avg_init_res
                    avg_sim_res_per = (avg_init_res - avg_sim_res) * 100 / avg_init_res
                    out += ",," + str(round(avg_muta_res_per, 2)) + "%," + str(round(avg_sim_res_per, 2)) + "%"
                out += "\n\n"

                # reset values for summing up residue contacts to start from first values of new residue
                init_res = float(line[1])
                muta_res = float(line[2])
                sim_res = float(line[3])
                if avrgs:
                    avg_init_res = float(line[4])
                    avg_muta_res = float(line[5])
                    avg_sim_res = float(line[6])
            else:
                # add up values for the current residue
                init_res += float(line[1])
                muta_res += float(line[2])
                sim_res += float(line[3])

                if avrgs:
                    avg_init_res += float(line[4])
                    avg_muta_res += float(line[5])
                    avg_sim_res += float(line[6])

        out += l + "\n"

    # handling of last residue
    out += "SUM," + str(init_res) + "," + str(muta_res) + "," + str(sim_res)
    if avrgs:
        out += "," + str(avg_init_res) + "," + str(avg_muta_res) + "," + str(avg_sim_res)
    out += "\n"

    # add line with percentage values
    muta_res_per = (init_res - muta_res) * 100 / init_res
    sim_res_per = (init_res - sim_res) * 100 / init_res
    out += ",," + str(round(muta_res_per, 2)) + "%," + str(round(sim_res_per, 2)) + "%"
    if avrgs:
        avg_muta_res_per = (avg_init_res - avg_muta_res) * 100 / avg_init_res
        avg_sim_res_per = (avg_init_res - avg_sim_res) * 100 / avg_init_res
        out += ",," + str(round(avg_muta_res_per, 2)) + "%," + str(round(avg_sim_res_per, 2)) + "%"
    out += "\n\n"

    # total values at the end of document
    out += "total," + str(init_tot) + "," + str(muta_tot) + "," + str(sim_tot)
    if avrgs:
        out += "," + str(round(avg_init_tot, 2)) + "," + str(round(avg_sim_tot, 2)) + "," + str(round(avg_muta_tot, 2))
    out += "\n"

    # total percentages
    muta_tot_per = (init_tot - muta_tot) * 100 / init_tot
    sim_tot_per = (init_tot - sim_tot) * 100 / init_tot

    out += ",," + str(round(muta_tot_per, 2)) + "%," + str(round(sim_tot_per, 2)) + "%"
    if avrgs:
        avg_muta_tot_per = (avg_init_tot - avg_muta_tot) * 100 / avg_init_tot
        avg_sim_tot_per = (avg_init_tot - avg_sim_tot) * 100 / avg_init_tot
        out += ",," + str(round(avg_muta_tot_per, 2)) + "%," + str(
            round(avg_sim_tot_per, 2)) + "%"
    out += "\n"

    return out


def get_atom_types(atoms):
    atom_types = []
    for item in atoms:
        item = item.split('@')[1]
        atom_types.append(item)
        atom_types = list(set(atom_types))

    return atom_types


# method to add residue types to the output
def add_residue_types(output, types):
    out = []
    output = output.splitlines()
    for line in output:
        if len(line) > 0 and line[0] == ':':
            residue = line.split('@')[0]
            residue = residue.strip(':')
            for item in types:
                if item[1] == residue:
                    # e.g. ":SA32"
                    line = line[0] + item[0] + line[1:]
                    # e.g. "A:S32"
                    line = line[2] + line[0] + line[1] + line[3:]

        out.append(line)
    return '\n'.join(out)


def output_to_pdf(output, file_name, avrgs, wat, hydro, input_list, investigated_residue):
    file_name = investigated_residue
    f = file_name + '0_occupancies.pdf'
    surface = cairo.PDFSurface(f, 595, 842)
    ctx = cairo.Context(surface)

    # title
    ctx.set_font_size(20)
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(20, 30)
    title = investigated_residue

    if hydro:
        title += " - hydrogen stripped"

    if wat:
        title += " - water stripped"

    ctx.show_text(title)

    ctx.set_font_size(12)
    y = 50
    counter = 0
    for item in input_list:
        ctx.move_to(20, y)
        ctx.show_text("#" + str(counter) + " " + ', '.join(item))
        y += 14
        counter += 1

    ctx.set_font_size(20)
    x = 20
    y = y + 15
    ctx.set_font_size(14)
    output = output.splitlines()
    pages = 0
    files = []

    for line in output:
        line = line.split(',')
        ctx.set_source_rgb(0, 0, 0)

        ctx.move_to(x, y)
        ctx.show_text(line[0])
        x += 120

        # coloring
        if len(line[0]) > 0 and line[0][0] == ':' or line[0] == 'SUM':
            ctx.move_to(x, y)
            ctx.show_text(line[1])
            x += 75
            ctx.set_source_rgb(0, 0, 0)

            if float(line[1]) > float(line[2]):
                ctx.set_source_rgb(0.9, 0, 0)
            if float(line[1]) < float(line[2]):
                ctx.set_source_rgb(0, 0.7, 0)
            ctx.move_to(x, y)
            ctx.show_text(line[2])
            x += 75
            ctx.set_source_rgb(0, 0, 0)

            if float(line[1]) > float(line[3]):
                ctx.set_source_rgb(0.9, 0, 0)
            if float(line[1]) < float(line[3]):
                ctx.set_source_rgb(0, 0.7, 0)
            ctx.move_to(x, y)
            ctx.show_text(line[3])
            x += 75
            ctx.set_source_rgb(0, 0, 0)

            if avrgs:
                ctx.move_to(x, y)
                ctx.show_text(str(round(float(line[4]), 2)))
                x += 75
                ctx.move_to(x, y)
                ctx.show_text(str(round(float(line[5]), 2)))
                x += 75
                ctx.move_to(x, y)
                ctx.show_text(str(round(float(line[6]), 2)))
                x += 75
        else:
            for item in line[1:]:
                ctx.move_to(x, y)
                ctx.show_text(item)
                x += 75

        y += 16
        x = 20
        if y > 820:
            pages += 1
            files.append(f)
            surface.finish()
            surface.flush()
            f = file_name + str(pages) + '_occupancies.pdf'
            files.append(f)
            surface = cairo.PDFSurface(f, 595, 842)
            ctx = cairo.Context(surface)
            ctx.set_font_size(14)
            y = 30

    surface.finish()
    surface.flush()

    merger = PdfFileMerger()
    for f in files:
        merger.append(f, 'rb')
    merger.write(file_name + '_occupancies.pdf')


# return list of list of inputs
def parse_input_list(input_list):
    out = []
    input_list = input_list.split()
    temp = []
    for item in input_list:
        if "prmtop" in item:
            out.append(temp)
            temp = []
            temp.append(item)
        elif "inpcrd" in item or "nc" in item:
            temp.append(item)
        elif item.isdigit():
            temp.append(item)
    out.remove(out[0])
    out.append(temp)
    return out


def output_2D_list(list2d):
    output = ""
    for item in list2d:
        for cell in item:
            output += str(cell) + ","
        output += "\n"
    return output


def c_get(lst, column):
    outlist = []
    for item in lst:
        outlist.append(item[column])
    return outlist


# add a column to the right
def c_bind(list1, list2):
    outlist = []
    if len(list1) == len(list2):
        for i in range(0, len(list1)):
            if not isinstance(list1[i], list):
                temp1 = [list1[i]]
            else:
                temp1 = list1[i]

            if not isinstance(list2[i], list):
                temp2 = [list2[i]]
            else:
                temp2 = list2[i]

            temp1.extend(temp2)
            outlist.append(temp1)
    else:
        print "fail: lists have different lengths"

    return outlist


# delete a column
def c_del(lst, column):
    outlist = []

    for item in lst:
        outitem = item[:column]
        outitem.extend(item[column + 1:])
        outlist.append(outitem)

    return outlist



# method reading the 'ATOM' records of a pdb file and returns atom number, atom type, residue type, residue number and
# coordinates in a list (e.g. [[1, N, CYX, 1, 43.390, 49.887, -62.005],[2, CA, ...], ...])
def read_pdb_atoms(pdb_file, wat):
    out = []

    with open(pdb_file, 'r') as f:
        for line in f:
            line = line.split()
            if 'ATOM' in line[0]:
                if not ((line[3] == 'WAT') and wat):
                    a_number = line[1]
                    a_type = line[2]
                    res_type = line[3]
                    res_number = line[4]
                    x = line[5]
                    y = line[6]
                    z = line[7]
                    out.append([a_number, a_type, res_type, res_number, x, y, z])
    return out


# returns a list of atom types of a pdb list
def get_all_atom_types(atom_list):
    types = []
    for atom in atom_list:
        types.append(atom[1])

    types = list(set(types))

    return types


# returns a list of residues with numbering of a pdb list
def get_all_residues(atom_list):
    residues = []
    for residue in atom_list:
        if residue[2] != 'WAT' and residue[2] != 'Cl-':
            residues.append(residue[2] + "," + residue[3])

    residues = list(set(residues))

    return residues


# returns a list of residue numbers of a pdb list
def get_all_residue_numbers(atom_list):
    residue_numbers = []
    for atom in atom_list:
        residue_numbers.append(atom[3])

    residue_numbers = list(set(residue_numbers))
    residue_numbers = [int(number) for number in residue_numbers]
    residue_numbers = sorted(residue_numbers)

    return residue_numbers


# convert residue types taxonomy
def convert_res_types(res_types):
    res_codes = {}
    res_codes['ALA'] = 'A'
    res_codes['ARG'] = 'R'
    res_codes['ASN'] = 'N'
    res_codes['ASP'] = 'D'
    res_codes['CYS'] = 'C'
    res_codes['CYX'] = 'C'
    res_codes['GLU'] = 'E'
    res_codes['GLN'] = 'Q'
    res_codes['GLY'] = 'G'
    res_codes['HIS'] = 'H'
    res_codes['HIE'] = 'H'
    res_codes['HID'] = 'H'
    res_codes['HIP'] = 'H'
    res_codes['ILE'] = 'I'
    res_codes['LEU'] = 'L'
    res_codes['LYS'] = 'K'
    res_codes['MET'] = 'M'
    res_codes['PHE'] = 'F'
    res_codes['PRO'] = 'P'
    res_codes['SER'] = 'S'
    res_codes['THR'] = 'T'
    res_codes['TRP'] = 'W'
    res_codes['TYR'] = 'Y'
    res_codes['VAL'] = 'V'

    out = []
    for item in res_types:
        if len(res_types[0]) > 1:
            out.append(res_codes[item])

    return out


def get_non_solvent_residues(pdb_file):
    atoms = read_pdb_atoms(pdb_file, 1)
    residues = get_all_residue_numbers(atoms)
    return residues


import os
import timeit


# reads in the specfied file and returns a list that contains elements consiting of the two contacting atoms and
# their distance to each other (e.g. [[[246@N, 23@C],2.34], [246@H, 23@CB], 3.12],...]
def read_cpptraj_contacts_data(file_name):

    out = []
    with open(file_name, 'r') as f:
        for line in f:
            if line[0] is not '#':
                line = line.split()
                atom = line[1].replace(':', '')
                atom = atom.split('_')
                dist = float(line[4])
                if atom[0] != atom[1]:
                    out.append([atom, dist])
    return out


# executes the cpptraj with the given parameters, outputs of will be written as files specified in the cpptraj file
def run_cpptraj(prmtop, trajin, cpptraj_file):
    cpptraj = 'cpptraj -p ' + prmtop + ' -y ' + trajin + ' -i ' + cpptraj_file + ' > ' + cpptraj_file.replace('.',
                                                                                                              '_') + ".log"
    print cpptraj
    start = timeit.default_timer()
    os.system(cpptraj)
    stop = timeit.default_timer()
    elapsed = round(stop - start)
    minutes = str(int(elapsed / 60))
    seconds = str(int(elapsed % 60))
    print minutes + " minutes " + seconds + " seconds"


# creates a cpptraj infile that contains commands to get native contacts between the list given by res1 and res2 (
# e.g. nativecontacts :47@C :1-5000 writecontacts F2196A_contacts.dat distance 3.9). The name fo the file is the
# given trajin without file extension followed by "_contacts.cpptraj" (e.g. trajin = F2196A.nc ->
# F2196A_contacts.cpptraj). Water, Chlor and hydrogen stripped
def create_contact_cpptraj(trajin, mask1, mask2, wat, hydro):
    t = trajin.split()
    frames = ""
    if len(t) > 1:
        frames = "_" + t[1] + "_" + t[2]
        frames = frames.strip("\"")
    cpptraj_file = t[0].split('.')[0].strip("\"") + "_" + t[0].split('.')[1] + frames + "_contacts.cpptraj"
    out_file = cpptraj_file.replace('cpptraj', 'dat')

    with open(cpptraj_file, 'w') as f:
        if wat:
            f.write('strip :WAT\n')
        if hydro:
            f.write('strip @H*\nstrip @?H*\nstrip @Cl-\n')

        for item1 in mask1:
            # TODO: needs proper handling of a list of masks
            for item2 in mask2:
                f.write('nativecontacts :' + item1 + ' :' + item2 + ' writecontacts ' +
                    out_file + ' distance 3.9\n')
        f.write('go')

    return [cpptraj_file, out_file]


# get contacts for atom types
def create_contact_cpptraj_types(trajin, types, mask1, mask2, wat, hydro):
    t = trajin.split()
    frames = ""
    if len(t) > 1:
        frames = "_" + t[1] + "_" + t[2]
        frames = frames.strip("\"")
    cpptraj_file = t[0].split('.')[0].strip("\"") + "_" + t[0].split('.')[1] + frames + "_averages_contacts.cpptraj"
    out_file = cpptraj_file.replace('cpptraj', 'dat')

    with open(cpptraj_file, 'w') as f:
        if wat:
            f.write('strip :WAT\n')
        if hydro:
            f.write('strip @H*\nstrip @?H*\nstrip @Cl-\n')

        for item in types:
            f.write('nativecontacts (:' + mask1 + ')&(@' + item + ') :' + mask2 + ' writecontacts ' + out_file +
                    ' distance 3.9\n')
        f.write('go')

    return [cpptraj_file, out_file]


# creates a cpptraj file to generate a pdb from the given inputs. Returns name of cpptraj file and name of pdb file.
# Water, Chlor and hydrogen stripped
def create_pdb_cpptraj(prmtop, trajin, wat, hydro):
    prmtop = prmtop.split('.')[0]
    prmtop = prmtop.split('/')[-1]
    trajin = trajin.split('.')[0]
    trajin = trajin.split('/')[-1]
    cpptraj_file = prmtop + "_cpptraj"
    pdb = prmtop + "_" + trajin + ".pdb"

    with open(cpptraj_file, 'w') as f:
        if wat:
            f.write('strip :WAT\n')
        if hydro:
            f.write('strip @H*\nstrip @?H*\nstrip @Cl-\n')
        f.write('trajout ' + pdb)
        f.write('\ngo')
    return [cpptraj_file, pdb]


# returns a list of all atoms with an atom type (e.g. [23@CA, 23@C,...])
def create_all_atom_residue_list(atom_list, atom_types):
    out = []
    for atom in atom_list:
        if atom[2]:
            for atom_type in atom_types:
                if atom_type == atom[1]:
                    out.append(atom[3] + '@' + atom_type)

    return out


# generates pdb file in the working directory from parameters. Returns the name of the pdb file.
def generate_pdb(prmtop, trajin, wat, hydro):
    cpptraj = create_pdb_cpptraj(prmtop, trajin, wat, hydro)
    run_cpptraj(prmtop, trajin, cpptraj[0])
    pdb_name = cpptraj[1]
    return pdb_name


if __name__ == "__main__":
    main(sys.argv)
