import sys
import argparse
import matplotlib.pyplot as plt

def main(argv):
    parser = argparse.ArgumentParser(description='Plot energy atom correlation interactions.')
    parser.add_argument('infile', help='csv file created by energy_atom_correlation.py')
    args = parser.parse_args()

    values = []

    with open(args.infile, 'r') as f:
        for line in f:
            temp = line.split(',')
            temp[1] = float(temp[1])
            temp[2] = float(temp[2][:-1])
            values.append(temp)

    values = sorted(values, key = lambda x: (x[1]))

    neg = []
    for i in range(0,50):
        item = values[i]
        neg.append(item[1])

    plt.plot(neg)

    pos = []
    for i in range(1,51):
        item = values[-i]
        pos.append(item[1])

    plt.plot(pos)

if __name__ == "__main__":
    main(sys.argv)