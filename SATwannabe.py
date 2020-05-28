#!/usr/bin/python3

import sys
from copy import deepcopy


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


class Interpretation:

    def __init__(self, num_vars=0, problem=None, var_distribution=None):
        self.var_distribution = var_distribution
        self.problem = problem  # Now the problem is not static if we want to back track
        self.vars = list(range(1, num_vars + 1))
        self.num_vars = len(self.vars)

    def copy(self):
        copy = Interpretation(self.num_vars, deepcopy(self.problem), deepcopy(self.var_distribution))
        copy.vars = list(self.vars)
        return copy

    def show(self):
        sys.stdout.write('v ')
        for var in self.vars:
            sys.stdout.write(str(var) + " ")
        sys.stdout.write('0\n')

    def unit_propagation(self, literal):
        self.pure_literal(literal)
        opp_literal_in = self.var_distribution[-literal][:]
        for clause in opp_literal_in:
            self.problem[clause - 1].remove(-literal)
            self.var_distribution[-literal].remove(clause)

    def pure_literal(self, literal):
        popped = 1
        literal_in = self.var_distribution[literal][:]
        for clause in literal_in:
            self.problem[clause - popped].remove(literal)
            others = self.problem[clause - popped]
            for other in others:
                self.var_distribution[other].remove(clause + 1 - popped)
            self.problem.pop(clause - popped)  # Clauses that contain the literal can be removed from the formula
            self.update_distribution(clause - popped)
            popped += 1
        self.vars[abs(literal) - 1] = literal  # Update the value for our variable
        self.var_distribution[literal] = []

    def update_distribution(self, clause_index):
        for i, distribution in enumerate(self.var_distribution):
            if distribution:
                j = 0
                while j < len(distribution):
                    clause = self.var_distribution[i][j]
                    if clause == clause_index + 1:
                        self.var_distribution[i].pop(j)
                        j -= 1
                    elif clause > clause_index:
                        self.var_distribution[i][j] -= 1
                    j += 1


class Solver:

    selection = []
    alternate = 0

    def __init__(self, input_data):
        # self.ratio = input_data.num_clauses / input_data.num_vars
        var_distribution = [[]] * (2 * input_data.num_vars + 1)
        distribute_vars(problem=input_data.clauses, var_distribution=var_distribution)
        self.interpretation = Interpretation(num_vars=input_data.num_vars, problem=input_data.clauses, var_distribution=var_distribution)

    def solve(self):  # Basic DPLL
        sol = self.dpll(self.interpretation)
        self.show(sol)

    def dpll(self, interpretation):
        self.unit_propagation(interpretation)
        self.pure_literals_rule(interpretation)
        if not interpretation.problem:  # If the problem is empty we found a solution
            self.interpretation = interpretation.copy()
            return True
        for clause in interpretation.problem:
            if not clause:  # If a clause is empty there's no solution
                return False
        #if Solver.alternate % 50 == 0:
            #Solver.selection = solver_satz(interpretation)
        literal = self.select_literal(interpretation)
        left = interpretation.copy()
        left.problem.append([literal])
        left.var_distribution[literal].append(len(left.problem))
        right = interpretation.copy()
        right.problem.append([-literal])
        right.var_distribution[-literal].append(len(left.problem))
        Solver.alternate += 1
        return self.dpll(left) or self.dpll(right)

    def show(self, sol):
        if sol:
            print("c OptiSat")
            print("s SATISFIABLE")
            self.interpretation.show()
        else:
            print("c OptiSat")
            print("s UNSATISFIABLE")

    def get_satz(self):
        score = max(Solver.selection)
        index = Solver.selection.index(score)
        Solver.selection[index] = 0
        return index + 1

    @staticmethod
    def select_literal(interpretation):  # Most Ocurrences
        mo = find_max_list(interpretation.var_distribution)
        index = interpretation.var_distribution.index(mo)
        num_vars = interpretation.num_vars
        if index <= num_vars:
            return index
        else:
            return (num_vars * 2 + 1) - index

    @staticmethod
    def unit_propagation(interpretation):
        for clause in interpretation.problem:
            if len(clause) == 1:
                interpretation.unit_propagation(clause[0])

    @staticmethod
    def pure_literals_rule(interpretation):
        for literal in range(1, int(len(interpretation.var_distribution) / 2) + 1):  # This value is always int but we cast
            # to suppress warnings
            if not interpretation.var_distribution[literal]:
                if interpretation.var_distribution[-literal]:
                    interpretation.pure_literal(-literal)
            if not interpretation.var_distribution[-literal]:
                if interpretation.var_distribution[literal]:
                    interpretation.pure_literal(literal)


def solver_satz(interpretation):  # Expensive to compute, giving wrong solutions
    weights = [None] * interpretation.num_vars
    clause_lengths = []
    for clause in interpretation.problem:
        clause_lengths.append(len(clause))
    pos_var_distribution = []
    for index in range(1, interpretation.num_vars + 1):
        pos_var_distribution.append(interpretation.var_distribution[index])
    for i, dist in enumerate(pos_var_distribution):
        if dist:
            var = get_var_from_dist(interpretation, i)
            appearance = interpretation.var_distribution[var]
            wpos = 0
            for clause in appearance:
                wpos += pow(2, -clause_lengths[clause - 1])
            wneg = 0
            appearance = interpretation.var_distribution[-var]
            for clause in appearance:
                wneg += pow(2, -clause_lengths[clause - 1])
            weights[i] = (wneg * wpos * pow(2, 10) + wneg + wpos)
        else:
            weights[i] = 0
    return weights


def get_var_from_dist(interpretation, index):
    if index <= interpretation.num_vars:
        return index + 1
    else:
        return -((interpretation.num_vars * 2 + 1) - index)


def find_max_list(array):
    lists = [len(lista) for lista in array]
    index = lists.index(max(lists))
    return array[index]


def distribute_vars(problem, var_distribution):
    clause_index = 1  # First clause has index 1
    for clause in problem:
        for literal in clause:
            if not var_distribution[literal]:
                var_distribution[literal] = [clause_index]
            else:
                var_distribution[literal].append(clause_index)
        clause_index += 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./sadSAT.py 'input_file'\n")

    parser = Parser(sys.argv[1])
    solver = Solver(parser)
    solver.solve()
