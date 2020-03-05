from random import random


class Interpretation:

    def __init__(self, num_vars, vars_values=None):
        self.num_vars = num_vars
        if vars_values is None:
            self.vars = list(range(1, num_vars + 1))
            self.get_random_interpretation()
        else:
            self.vars = vars_values

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

    def best_neighbour(self, problem):
        neighbours = self.get_neighbours()
        best_neighbour = neighbours[0]
        best_cost = best_neighbour.cost(problem)
        for elem in neighbours:
            if elem.cost(problem) < best_cost:
                best_neighbour = elem
        return best_neighbour

    def cost(self, problem):
        cost = 0
        for clause in problem:
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
        print(self.vars)
