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
