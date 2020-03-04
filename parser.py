import sys

def parse(inputfile):
    clauses = []
    with open(inputfile) as f:
        for line in f:
            if line[0] == "c" or line[0] == "p":
                continue
            linesplit = line.split()
            linesplit.pop()
            clauses.append(list(map(int, linesplit)))
        return clauses