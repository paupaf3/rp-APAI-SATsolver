class Parser():

    def __init__(self, inputfile):
        self.num_vars = 0
        self.clauses = []
        self.parse(inputfile)

    def parse(self, inputfile):
        """ Retorna una llista de llistes, amb les clausules, si hi ha algun error,
            retorna error. 
        """
        
        num_clauses = 0

        with open(inputfile) as f:
            for line in f:
                if line[0] == "c":
                    continue

                if line[0] == "p":
                    if line[1] != 'cnf':
                        return None

                    num_clauses = int(line[3])
                    linesplit = line.split()
                    self.num_vars = int(linesplit[2])
                    continue

                linesplit = line.split()
                linesplit.pop()
                self.clauses.append(list(map(int, linesplit)))

        if len(self.clauses) != num_clauses:
            return None

        return self.clauses