class Genome(object):
    """"""

    def __init__(self, genes, representation, fitness_func):
        """"""
        self.genes          = genes
        self.representation = representation
        self.fitness_func   = fitness_func

    def fitness(self):
        """"""
        return self.fitness_func(self.genes)
