class Parser:

    def __init__(self, inputfile):
        self.num_vars = 0
        self.num_clauses = 0
        self.clauses = []
        self.parse(inputfile)

    def parse(self, inputfile):
        """ Retorna una llista de llistes, amb les clausules, si hi ha algun error,
            retorna error.
        """

        with open(inputfile) as f:
            for line in f:
                if line[0] == "c":
                    continue

                if line[0] == "p":
                    line_split = line.split()
                    self.num_clauses = int(line_split[3])
                    self.num_vars = int(line_split[2])
                    continue

                line_split = line.split()
                line_split.pop()
                self.clauses.append(list(map(int, line_split)))