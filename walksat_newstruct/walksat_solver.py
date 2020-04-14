#!/usr/bin/python3

import sys
from parseroptimized import Parser
from interpretation import Interpretation
from random import random, choice

max_tries = 10000
max_flips = 10000


class Solver:

    def __init__(self, input_data):
        Interpretation.problem = input_data.vars  # Set static variable problem for Interpretation class
        self.best_interpretation = Interpretation(num_vars=input_data.num_vars, num_clauses=input_data.num_clauses)

    def solve(self):  # Walksat implementation (random walk addition)
        for i in range(max_tries):
            for j in range(max_flips):
                if self.best_interpretation.cost() == 0:
                    self.show()
                    return self.best_interpretation
                unsat_clause = self.best_interpretation.get_unsat_clause()
                flips_cost = []  # How many clauses would be unsatisfied if we flip each variable of the unsat clause
                for var in unsat_clause:
                    self.best_interpretation.flip(var)
                    flips_cost.append(self.best_interpretation.cost())
                    self.best_interpretation.flip(var)
                if min(flips_cost) > 0 and random() < 0.5:  # Random walk
                    self.best_interpretation.flip(choice(unsat_clause))
                else:
                    self.best_interpretation.flip(unsat_clause[flips_cost.index(min(flips_cost))])  # Flip the
                    # variable that minimizes the # of unsat clauses
            self.best_interpretation.get_random_interpretation()

    def show(self):
        print("c SAT")
        print("s SATISFIABLE")
        self.best_interpretation.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./walksat_solver.py 'input_file'\n")

    parser = Parser(sys.argv[1])
    solver = Solver(parser)
    solution = solver.solve()
