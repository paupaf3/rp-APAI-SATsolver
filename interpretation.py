from random import random
import sys


class Interpretation:
    problem = []  # Static variable to represent the problem variables

    def __init__(self, num_vars=0, vars=None):
        if vars is None:
            self.vars = list(range(1, num_vars + 1))
            self.num_vars = len(self.vars)
            self.get_random_interpretation()
        else:
            self.vars = vars
        if num_vars != 0:
            self.num_vars = num_vars
        else:
            self.num_vars = len(self.vars)

    def get_random_interpretation(self):
        for i in range(self.num_vars):
            p = random()
            if p < 0.5:
                self.vars[i] *= -1

    def get_neighbours(self):
        neighbours = []
        for i in range(self.num_vars):
            neighbour = self.copy()
            neighbour.vars[i] *= -1
            neighbours.append(Interpretation(neighbour.num_vars, neighbour.vars))
        return neighbours

    def best_neighbour(self):
        neighbours = self.get_neighbours()
        best_neighbour = neighbours[0]
        best_cost = best_neighbour.cost()
        for elem in neighbours:
            if elem.cost() < best_cost:
                best_neighbour = elem
        return best_neighbour

    def cost(self):
        cost = 0
        for clause in self.problem:
            length = self.num_vars
            for var in self.vars:
                if var in clause:
                    break
                else:
                    length -= 1
                if length == 0:
                    cost += 1
        return cost

    def copy(self):
        copy = Interpretation(self.num_vars)
        copy.vars = list(self.vars)
        return copy

    def show(self):
        for var in self.vars:
            sys.stdout.write(str(var) + " ")
        sys.stdout.write('0\n')

    def is_solution(self):
        return self.cost() == 0

    def get_unsat_clause(self):
        for clause in self.problem:
            length = self.num_vars
            for var in self.vars:
                if var in clause:
                    break
                else:
                    length -= 1
                if length == 0:
                    return clause

    def flip(self, var):
        self.vars[abs(var) - 1] *= -1