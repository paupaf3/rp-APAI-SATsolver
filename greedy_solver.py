import sys
from parser import Parser
from interpretation import Interpretation

max_tries = 100000


class Solver:

    def __init__(self, input_data):
        Interpretation.problem = input_data.clauses  # Set static variable problem for Interpretation class

        self.best_interpretation = Interpretation(num_vars=input_data.num_vars)
        self.best_cost = self.best_interpretation.cost()

    def solve(self):  # Greedy search with random initialisation, finding the best neighbour every time
        for i in range(max_tries):
            if self.best_cost != 0:
                neighbour = self.best_interpretation.best_neighbour()
                if neighbour.cost() < self.best_cost:
                    self.best_interpretation = neighbour
                    self.best_cost = self.best_interpretation.cost()
        return self.best_interpretation

    def show(self):
        print("c SAT")
        print("s SATISFIABLE")
        self.best_interpretation.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./solver.py 'input_file'\n")

    parser = Parser(sys.argv[1])
    solver = Solver(parser)
    solution = solver.solve()
    print(Interpretation.problem)
    solver.show()
    print(solution.is_solution())
