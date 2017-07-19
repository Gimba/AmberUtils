import sys
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Plot energy atom correlation interactions.')
    parser.add_argument('infile', help='csv file created by energy_atom_correlation.py')
    args = parser.parse_args()

if __name__ == "__main__":
    main(sys.argv)