class Parser:

    def __init__(self, inputfile):
        self.num_vars = 0
        self.clauses = []
        self.parse(inputfile)

    def parse(self, inputfile):
        with open(inputfile) as f:
            for line in f:
                if line[0] == "c":
                    continue
                if line[0] == "p":
                    linesplit = line.split()
                    self.num_vars = int(linesplit[2])
                    continue
                linesplit = line.split()
                linesplit.pop()
                self.clauses.append(list(map(int, linesplit)))