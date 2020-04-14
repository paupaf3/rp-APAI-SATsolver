class Parser:

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
                    line_split = line.split()
                    self.num_clauses = int(line_split[3])
                    self.num_vars = int(line_split[2])
                    self.vars = [None] * self.num_vars * 2
                    continue

                clause += 1
                line_split = line.split()
                line_split.pop()

                for literal in line_split:
                    literal = int(literal)
                    if str(literal).startswith('-'):
                        if self.vars[literal] is None:
                            self.vars[literal] = [clause]
                        else:
                            self.vars[literal].append(clause)
                    else:
                        if self.vars[literal-1] is None:
                            self.vars[literal-1] = [clause]
                        else:
                            self.vars[literal-1].append(clause)
