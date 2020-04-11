#!/usr/bin/python3

import sys
from parseroptimized import Parser
from interpretation import Interpretation
import random

max_tries = 100000

class Solver:

    def __init__(self, input_data):

        Interpretation.problem = input_data.vars
        self.num_clauses = input_data.num_clauses
        self.num_vars = input_data.num_vars
        self.best_interpretation = Interpretation(num_vars=self.num_vars, num_clauses=self.num_clauses)

    def solve(self):

        max_flips = self.num_vars

        for actual_try in range(max_tries):

            self.best_interpretation.get_random_interpretation()

            for flip in range(max_flips):

                sat = self.best_interpretation.satisfied()

                if sat == self.num_clauses:

                    return sat

                best_vars_flip = self.best_interpretation.best_flips(satisfied_clauses = sat)

                if len(best_vars_flip) == 0:

                    rnd = random.randint(0, len(best_vars_flip) - 1)

                else:
                    rnd = 0

                self.best_interpretation.flip(var = best_vars_flip[rnd])

        return sat

    def show_sol(self, sat):
        if sat == self.num_clauses:
            print("c SAT")
            print("s SATISFIABLE")
            self.best_interpretation.show()

        else:

            print("s NO SOLUTION FOUND")

if __name__ == '__main__':

    parser = Parser(sys.argv[1])
    solver = Solver(parser)
    sat = solver.solve()
    solver.show_sol(sat = sat)
