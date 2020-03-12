#!/usr/bin/python3
import sys
import parser
import interpretation

max_tries = 5000


class Solver:

    def __init__(self, input_data):
        self.interpretation = interpretation.Interpretation(num_vars=input_data.num_vars)
        self.problem = input_data.clauses
        self.cost = 0

    def random_search(self):
        current_int = self.interpretation.copy()
        for i in range(max_tries):
            current_int.get_random_interpretation()
            current_cost = current_int.cost(self.problem)
            if current_cost == 0:
                self.interpretation = current_int.copy()
                self.cost = current_cost
                return self.interpretation
        self.interpretation = current_int.copy()
        self.cost = current_cost

    def show(self):
        if self.cost == 0:
            print("c SAT")
            print("s SATISFIABLE")
            sys.stdout.write('v ')
            self.interpretation.show()
        else:
            print("No solution found")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./solver.py 'input_file'\n")

    parser = parser.Parser(sys.argv[1])
    solver = Solver(parser)
    solution = solver.random_search()
    solver.show()
    #print(solution.is_solution(solver.problem))
