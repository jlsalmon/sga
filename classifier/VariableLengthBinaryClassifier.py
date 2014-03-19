import random
from classifier.BinaryClassifier import BinaryClassifier
from sga.representation import Representation
from sga.selection import tournament


class VariableLengthBinaryClassifier(BinaryClassifier):
    """
    Binary classification with wildcard generalization and variable-length
    genome
    """
    def __init__(self, data, gene_length, genome_length):
        """"""
        BinaryClassifier.__init__(self, data, gene_length, genome_length)

        self.representation = Representation({"length": genome_length,
                                              "type": "enum",
                                              "values": ['0', '1'],
                                              "duplicates": True})

        self.population_size = 100
        self.generations = 250
        self.selection_func = tournament
        self.tournament_size = 10
        self.genome_lengths = list()
        self.mutation_prob = 0.01
        self.mutation_func = self.mutation_func_variable_length
        self.crossover_prob = 0.2
        self.elite_count = 6

    def split_data(self, data):
        # 3/4 training data, 1/4 validation
        self.validation_set = data[:(len(data) / 4)]
        self.training_set = data[(len(data) / 4):]

    def mutation_func_variable_length(self, individual, probability):
        """"""
        # Do the normal mutation func in the superclass
        individual = super(VariableLengthBinaryClassifier,
                           self).mutation_func_generalisation(individual,
                                                              probability)

        length_change_prob = 0.2

        # Randomly delete the last gene, or add a new gene
        # if random.random() < length_change_prob:
        #     if random.random() < 0.99 \
        #             and not len(individual) == self.gene_length:
        #         # Delete the last gene
        #         del individual[len(individual) - self.gene_length:]
        #     else:
        #         # Add a new gene
        #         individual.extend(self.make_new_gene())

        # Delete a random gene
        if random.random() < length_change_prob \
                and not len(individual) == self.gene_length:
            pos = random.randint(0, len(individual))
            rem = pos % self.gene_length

            if rem != 0:
                pos -= rem

            del individual[pos:pos + self.gene_length]

        # Update info for plotter
        self.genome_lengths.append(len(individual))

        assert len(individual) % self.gene_length == 0
        return individual

    def make_new_gene(self):
        gene = [self.representation.values[random.randint(0,
                len(self.representation.values)) - 1]
                for _ in xrange(self.gene_length)]
        if gene[-1] == '#':
            gene[-1] = '1' if random.random() < 0.5 else '0'
        return gene
