
import sys
from parser import parse

def Interpretation:

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./solver.py 'inputfile'\n")

    clauses = parse(sys.argv[1])
    print(clauses)