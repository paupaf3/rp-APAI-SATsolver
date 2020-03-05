import sys
import parser
import interpretation

max_tries = 100000


class Solver:

    def __init__(self, input_data):
        self.best_interpretation = interpretation.Interpretation(input_data.num_vars)
        self.problem = input_data.clauses
        self.best_cost = self.best_interpretation.cost(self.problem)

    def solve(self):
        for i in range(max_tries):
            if self.best_cost != 0:
                neighbour = self.best_interpretation.best_neighbour(self.problem)
                if neighbour.cost(self.problem) < self.best_cost:
                    self.best_interpretation = neighbour
                    self.best_cost = self.best_interpretation.cost(self.problem)
                    if self.best_cost == 0:
                        return self.best_interpretation.vars
        return self.best_interpretation.vars

    def show(self):
        print(self.best_interpretation)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./solver.py 'input_file'\n")

    parser = parser.Parser(sys.argv[1])
    solver = Solver(parser)
    solution = solver.solve()
    print(solver.problem)
    print(solution)
