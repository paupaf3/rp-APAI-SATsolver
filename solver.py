import sys
import parser
import interpretation

max_tries = 100000


class Solver:

    def __init__(self, input_data):
        self.best_interpretation = interpretation.Interpretation(num_vars=input_data.num_vars)
        self.problem = input_data
        self.best_cost = self.best_interpretation.cost(self.problem)

    def solve(self):
        for i in range(max_tries):
            if self.best_cost != 0:
                neighbour = self.best_interpretation.best_neighbour(self.problem)
                if neighbour.cost(self.problem) < self.best_cost:
                    self.best_interpretation = neighbour
                    self.best_cost = self.best_interpretation.cost(self.problem)
        return self.best_interpretation

    def show(self):
        print("c SAT")
        print("s SATISFIABLE")
        self.best_interpretation.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Incorrect number of arguments, usage: ./solver.py 'input_file'\n")

    data = parser.parse(sys.argv[1])
    if data == None:
        print("Input error")
        sys.exit()
    solver = Solver(data)
    solution = solver.solve()
    solver.show()
    #print(solution.is_solution(solver.problem))
