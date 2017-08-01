

# method reading the 'ATOM' records of a pdb file and returns atom number, atom type, residue type, residue number and
# coordinates in a list (e.g. [[1, N, CYX, 1, 43.390, 49.887, -62.005],[2, CA, ...], ...])
def read_pdb_atoms(pdb_file):
    out = []

    with open(pdb_file, 'r') as f:
        for line in f:
            line = line.split()
            if 'ATOM' in line[0]:
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


# returns a list of residue numbers of a pdb list
def get_all_residue_numbers(atom_list):
    residue_numbers = []
    for atom in atom_list:
        residue_numbers.append(atom[3])

    residue_numbers = list(set(residue_numbers))
    residue_numbers = [int(number) for number in residue_numbers]
    residue_numbers = sorted(residue_numbers)

    return residue_numbers
