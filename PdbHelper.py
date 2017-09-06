

# method reading the 'ATOM' records of a pdb file and returns atom number, atom type, residue type, residue number and
# coordinates in a list (e.g. [[1, N, CYX, 1, 43.390, 49.887, -62.005],[2, CA, ...], ...])
def read_pdb_atoms(pdb_file, wat):
    out = []

    with open(pdb_file, 'r') as f:
        for line in f:
            line = line.split()
            if 'ATOM' in line[0]:
                if (line[3] == 'WAT') == wat:
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
