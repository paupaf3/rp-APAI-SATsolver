#!/usr/bin/python3

import sys
from parser import Parser
from interpretation import Interpretation
from random import random, choice

max_tries = 10000
max_flips = 10000


class Solver:

    def __init__(self, input_data):
        Interpretation.problem = input_data.clauses  # Set static variable problem for Interpretation class
        Interpretation.var_distribution = [None] * 2 * input_data.num_vars
        self.distribute_vars()
        self.best_interpretation = Interpretation(num_vars=input_data.num_vars)
        self.best_cost = self.best_interpretation.cost()

    def solve(self):  # Walksat implementation (random walk addition)
        for i in range(max_tries):
            for j in range(max_flips):
                if self.best_cost == 0:
                    return self.best_interpretation
                unsat_clause = self.best_interpretation.get_unsat_clause()
                flips_cost = []  # How many clauses would be unsatisfied if we flip each variable of the unsat clause
                future_interpretation = self.best_interpretation.copy()
                for var in unsat_clause:
                    future_interpretation.flip(var)
                    flips_cost.append(self.cost_diff(self.best_interpretation, future_interpretation, abs(var)))
                    future_interpretation.flip(var)
                if min(flips_cost) > 0 and random() < 0.5:  # Random walk
                    actual_flip = choice(unsat_clause)
                    self.best_interpretation.flip(actual_flip)
                else:
                    flip_index = flips_cost.index(min(flips_cost))
                    self.best_interpretation.flip(unsat_clause[flip_index])  # Flip the
                    # variable that minimizes the # of unsat clauses
                    self.best_cost += flips_cost[flip_index]
            self.best_interpretation.get_random_interpretation()
            self.best_cost = self.best_interpretation.cost()

    def show(self):
        print("c SAT")
        print("s SATISFIABLE")
        self.best_interpretation.show()

    def cost_diff(self, actual, future, var):
        cost = 0
        for clause in Interpretation.var_distribution[var - 1]:
            is_sat_future = future.is_satisfied(clause)
            is_sat_now = actual.is_satisfied(clause)
            if is_sat_now and not is_sat_future:
                cost += 1
            if not is_sat_now and is_sat_future:
                cost -= 1
        for clause in Interpretation.var_distribution[-var]:
            is_sat_future = future.is_satisfied(clause)
            is_sat_now = actual.is_satisfied(clause)
            if is_sat_now and not is_sat_future:
                cost += 1
            if not is_sat_now and is_sat_future:
                cost -= 1
        return cost

    @staticmethod
    def distribute_vars():
        clause_index = 1  # First clause has index 1

        for clause in Interpretation.problem:
            for literal in clause:
                if literal < 0:
                    if Interpretation.var_distribution[literal] is None:
                        Interpretation.var_distribution[literal] = [clause_index]
                    else:
                        Interpretation.var_distribution[literal].append(clause_index)
                else:
                    if Interpretation.var_distribution[literal - 1] is None:
                        Interpretation.var_distribution[literal - 1] = [clause_index]
                    else:
                        Interpretation.var_distribution[literal - 1].append(clause_index)
            clause_index += 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./walksat_solver.py 'input_file'\n")

    parser = Parser(sys.argv[1])
    solver = Solver(parser)
    solution = solver.solve()
    solver.show()
