class Parser():

    def __init__(self, inputfile):
        self.num_vars = 0
        self.num_clauses = 0
        self.vars = []
        self.parse(inputfile)

    def parse(self, inputfile):

        clause = 0

        with open(inputfile) as file:
            for line in file:

                if line[0] == "c":
                    continue

                if line[0] == "p":
                    linesplit = line.split()
                    self.num_clauses = int(linesplit[3])
                    self.num_vars = int(linesplit[2])
                    self.vars = [None] * self.num_vars * 2
                    continue

                clause += 1
                linesplit = line.split()
                linesplit.pop()

                for literal in linesplit:
                    literal = int(literal)
                    if str(literal).startswith('-'):
                        if self.vars[literal] == None:
                            self.vars[literal] = [clause]
                        else:
                            self.vars[literal].append(clause)
                    else:
                        if self.vars[literal-1] == None:
                            self.vars[literal-1] = [clause]
                        else:
                            self.vars[literal-1].append(clause)
