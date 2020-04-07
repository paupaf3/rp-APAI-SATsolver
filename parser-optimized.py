class Parser():

    def __init__(self, inputfile):
        self.num_vars = 0
        self.clauses = []
        self.parse(inputfile)

    def parse(self, inputfile):

        num_clauses = 0
        count = 0

        with open(inputfile) as file:
            for line in file:

                if line[0] == "c":
                    continue

                if line[0] == "p":
                    linesplit = line.split()
                    num_clauses = int(linesplit[3])
                    self.num_vars = int(linesplit[2])
                    clauses = [None] * num_vars * 2
                    continue

                count += 1
                linesplit = line.split()
                linesplit.pop()

                for literal in linesplit:
                    literal = int(literal)
                    if str(literal).startswith('-'):
                        if self.clauses[literal] == None:
                            self.clauses[literal] = [count]
                        else:
                            self.clauses[literal].append(count)
                    else:
                        if self.clauses[literal-1] == None:
                            self.clauses[literal-1] = [count]
                        else:
                            self.clauses[literal-1].append(count)

            if len(self.clauses) != num_clauses:
                return None

            return self.clauses
