import random
from classifier.RealValueClassifier import RealValueClassifier
from sga.representation import Representation
from sga.selection import tournament


class BcwClassifier(RealValueClassifier):

    def __init__(self, data, num_genes, gene_length):
        """"""
        super(BcwClassifier, self).__init__(data, gene_length, num_genes)

        self.representation = Representation({"length": 50 * gene_length,
                                              "type": "int",
                                              "min": 0,
                                              "max": 10})

        random.shuffle(data)
        # 3/4 training data, 1/4 validation
        self.training_set = data[(len(data) / 4):]
        self.validation_set = data[:(len(data) / 4)]

        self.population_size = 200
        self.generations = 50

        self.crossover_prob = 0.4
        self.elite_count = 2

        self.selection_func = tournament
        self.tournament_size = 10

        # self.mutation_func = self.mutation_func_step
        self.mutation_prob = 0.01
        self.mutation_step_size = 0.01

        # self.mutation_func = self.mutation_func_one_sigma

        self.mutation_func = self.mutation_func_n_sigma
        self.common_sd = 0.5
        self.bound_sd = 1
        self.spread_sd = 1

        print 'bcw mutation operator:', self.mutation_func
