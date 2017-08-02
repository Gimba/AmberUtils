import os


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
    os.system('cpptraj -p ' + prmtop + ' -y ' + trajin + ' -i ' + cpptraj_file)


# creates a cpptraj infile that contains commands to get native contacts between the list given by res1 and res2 (
# e.g. nativecontacts :47@C :1-5000 writecontacts F2196A_contacts.dat distance 3.9). The name fo the file is the
# given trajin without file extension followed by "_contacts.cpptraj" (e.g. trajin = F2196A.nc ->
# F2196A_contacts.cpptraj). Water, Chlor and hydrogen stripped
def create_contact_cpptraj(trajin, res1, res2):
    cpptraj_file = trajin.split('.')[0] + "_" + trajin.split('.')[1] + "_contacts.cpptraj"
    out_file = cpptraj_file.replace('cpptraj', 'dat')

    with open(cpptraj_file, 'w') as f:
        f.write('strip :WAT\nstrip @H*\nstrip @?H*\nstrip @Cl-\n')
        for item1 in res1:
            for item2 in res2:
                f.write('nativecontacts :' + item1 + ' :' + item2 + ' writecontacts ' +
                    out_file + ' distance 3.9\n')
        f.write('go')

    return [cpptraj_file, out_file]


# creates a cpptraj file to generate a pdb from the given inputs. Returns name of cpptraj file and name of pdb file.
# Water, Chlor and hydrogen stripped
def create_pdb_cpptraj(prmtop, trajin):
    prmtop = prmtop.split('.')[0]
    trajin = trajin.split('.')[0]
    cpptraj_file = prmtop + "_pdb.cpptraj"
    pdb = prmtop + "_" + trajin + ".pdb"

    with open(cpptraj_file, 'w') as f:
        f.write('strip :WAT\nstrip @H*\nstrip @?H*\nstrip @Cl-\n')
        f.write('trajout ' + pdb)
        f.write('\ngo')
    return [cpptraj_file, pdb]


# returns a list of all atoms with an atom type (e.g. [23@CA, 23@C,...])
def create_all_atom_residue_list(atom_list, atom_types):
    out = []
    for atom in atom_list:
        for atom_type in atom_types:
            if atom_type == atom[1]:
                out.append(atom[3] + '@' + atom_type)

    return out


# generates pdb file in the working directory from parameters. Returns the name of the pdb file. Water and hydrogen
# stripped
def generate_pdb(prmtop, trajin):
    cpptraj = create_pdb_cpptraj(prmtop, trajin)
    run_cpptraj(prmtop, trajin, cpptraj[0])
    pdb_name = cpptraj[1]
    return pdb_name
