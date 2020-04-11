from random import random
import sys

class Interpretation:

    problem = [] # Static variable to represent the problem variables

    def __init__(self, num_vars, num_clauses):

        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.vars = list(range(1, num_vars + 1))
        self.get_random_interpretation()

    def get_random_interpretation(self):

        for i in range(self.num_vars):

            if random() < 0.5:

                self.vars[i] *= -1

    def satisfied(self): # Return num of satisfied clauses

        satisfied_clauses = 0
        pos_clause = 1

        for var in self.problem:

            for pos in var:

                if pos == pos_clause:

                    satisfied_clauses += 1
                    pos_clause += 1
                    break

        return satisfied_clauses

    def best_flips(self, satisfied_clauses = 0): # Return list of vars that flipped increments the satisfied clausules

        best_vars_flip = []
        best_difference = 0

        for var in self.vars: # Diference of satisfied clauses per var

            self.flip(var = var)
            total_satisfied_clauses = self.satisfied()
            difference = total_satisfied_clauses - satisfied_clauses

            if difference >= best_difference:

                best_difference = difference
                best_vars_flip.append(var)

        return best_vars_flip

    def flip(self, var):

        self.problem[var], self.problem[var * -1] = self.problem[var * -1], self.problem[var]

    def show(self):

        for var in self.vars:

            sys.stdout.write(str(var) + " ")

        sys.stdout.write('0\n')
