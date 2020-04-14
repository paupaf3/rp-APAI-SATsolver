from random import random
import sys

class Interpretation:
    problem = []  # Static variable to represent the problem variables

    def __init__(self, num_vars=0, num_clauses=0,vars=None):
        self.vars = list(range(1, num_vars + 1))
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.satisfied_clauses = [False] * num_clauses
        self.satisfied_clauses_un = [False] * num_clauses
        self.get_random_interpretation()

    def get_random_interpretation(self):
        for i in range(self.num_vars):
            p = random()
            if p < 0.5:
                self.vars[i] *= -1

    def cost(self):

        ''' Mira el numero de clausules insatisfetes '''

        cost = 0
        for var in self.vars: # per cada variable de la interpretacio
            index = var
            if index > 0:
                index -= 1
            if self.problem[index] is None:
                continue
            for n_clause in self.problem[index]:
                self.satisfied_clauses[n_clause - 1] =  True

        for false in self.satisfied_clauses:
            if false == False:
                cost += 1

        self.satisfied_clauses_un = self.satisfied_clauses.copy()
        self.satisfied_clauses = [False] * self.num_clauses

        return cost

    def get_unsat_clause(self):

        ''' Retorna la primera clausula no satisfeta que es troba '''

        unsat_clause = []
        clause_index = self.satisfied_clauses_un.index(False) + 1
        var_index = 1
        var_index_reverse = self.num_vars * 2 * (-1)
        for var in self.problem:
            if var is None:
                continue
            if clause_index in var:
                if var_index <= (self.num_vars):
                    unsat_clause.append(var_index)
                elif var_index > (self.num_vars):
                    unsat_clause.append(var_index_reverse)
            var_index += 1
            var_index_reverse += 1
        return unsat_clause

    def show(self):
        sys.stdout.write('v ')
        for var in self.vars:
            sys.stdout.write(str(var) + " ")
        sys.stdout.write('0\n')

    def is_solution(self):
        return self.cost() == 0

    def flip(self, var):
        self.vars[abs(var) - 1] *= -1
