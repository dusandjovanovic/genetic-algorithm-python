import numpy
import matplotlib.pyplot as plot

no_moves = 256
no_generations = 128
no_chromosomes = 100

dna_size = no_moves * 2
dna_bound = [0, 2]

cross_rate = 0.9
mutation_rate = 0.0001

point_a = [0, 5]
point_b = [10, 5]
obstacle_line = numpy.array([[5, 5], [5, 8]])

class GeneticAlgorithm(object):
    def __init__(self, dna_size, dna_bound, cross_rate, mutation_rate, no_chromosomes):
        self.dna_size = dna_size
        self.dna_bound = dna_bound
        self.cross_date = cross_rate
        self.mutation_rate = mutation_rate
        self.no_chromosomes = no_chromosomes

        self.generation = numpy.random.randint(*dna_bound, size = (no_chromosomes, dna_size))

    def dna_to_product(self, no_moves, point_a):
        dna = self.generation
        generation = (dna - 0.5) / 2
        generation[:, 0], generation[:, no_moves] = point_a[0], point_a[1]
        lines_x = numpy.cumsum(generation[:, :no_moves], axis = 1)
        lines_y = numpy.cumsum(generation[:, no_moves:], axis = 1)
        return lines_x, lines_y

    def get_fitness(self, lines_x, lines_y, point_b, obstacle_line):
        distance_to_goal = numpy.sqrt((point_b[0] - lines_x[:, -1]) ** 2 + (point_b[1] - lines_y[:, -1]) ** 2)
        fitness = numpy.power(1 / (distance_to_goal + 1), 2)
        points = (lines_x > obstacle_line[0, 0] - 0.5) & (lines_x < obstacle_line[1, 0] + 0.5)
        y_values = numpy.where(points, lines_y, numpy.zeros_like(lines_y) - 100)
        bad_lines = ((y_values > obstacle_line[0, 1]) & (y_values < obstacle_line[1, 1])).max(axis = 1)
        fitness[bad_lines] = 1e-6
        return fitness

    def select(self, fitness):
        index = numpy.random.choice(numpy.arange(self.no_chromosomes), size = self.no_chromosomes, replace = True, p = fitness / fitness.sum())
        return self.generation[index]

    def crossover(self, parent, generation):
        if numpy.random.randint(0, self.no_chromosomes, size = 1):
            i_ = numpy.random.randint(0, self.no_chromosomes, size = 1)  # select another individual from generation
            cross_points = numpy.random.randint(0, 2, self.dna_size).astype(numpy.bool)  # choose crossover points
            parent[cross_points] = generation[i_, cross_points] # cross and produce one child
        return parent

    def mutate(self, child):
        for point in range(self.dna_size):
            if numpy.random.rand() < self.mutation_rate:
                child[point] = numpy.random.randint(*self.dna_bound)
        return child

    def evolve(self, fitness):
        generation = self.select(fitness)
        generation_copy = generation.copy()
        for parent in generation:
            child = self.crossover(parent, generation_copy)
            child = self.mutate(child)
            parent[:] = child
        self.generation = generation

class Line(object):
    def __init__(self, no_moves, point_b, point_a, obstacle_line):
        self.no_moves = no_moves
        self.point_b = point_b
        self.point_a = point_a
        self.obstacle_line = obstacle_line

        plot.ion()

    def plotting(self, lines_x, lines_y):
        plot.cla()
        plot.scatter(*self.point_b, s = 100)
        plot.scatter(*self.point_a, s = 100)
        plot.plot(self.obstacle_line[:, 0], self.obstacle_line[:, 1], lw=3, c='k')
        plot.plot(lines_x.T, lines_y.T, c='k')
        plot.xlim((-5, 15))
        plot.ylim((-5, 15))
        plot.pause(0.01)

algorithm = GeneticAlgorithm(dna_size = dna_size, dna_bound = dna_bound, cross_rate = cross_rate, mutation_rate = mutation_rate, no_chromosomes = no_chromosomes)

line = Line(no_moves = no_moves, point_b = point_b, point_a = point_a, obstacle_line = obstacle_line)

for generation in range(no_generations):
    x, y = algorithm.dna_to_product(no_moves, point_a)
    fitness = algorithm.get_fitness(x, y, point_b, obstacle_line)

    algorithm.evolve(fitness)

    print('> Generation: ', generation, ' | Highest fitness: ', fitness.max())

    line.plotting(x, y)

plot.ioff()
plot.show()