import os

def read_cpptraj_contacts_data(file_name):

    out = []
    with open(file_name, 'r') as f:
        for line in f:
            if line[0] is not '#':
                line = line.split()
                atom = line[1].replace(':', '')
                atom = atom[1].split('_')
                dist = float(line[4])
                out.append(atom, dist)
    return out


def run_cpptraj(pdb, trajin, cpptraj_file):
    os.system('cpptraj -p ' + pdb + ' -y ' + trajin + ' -i ' + cpptraj_file)


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
