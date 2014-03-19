import random
from sga.representation import Representation
from sga.selection import tournament


class BinaryClassifier(object):
    """
    Binary classification with wildcard generalization
    """
    def __init__(self, data, gene_length, genome_length):
        """"""
        self.gene_length = gene_length
        self.genome_length = genome_length

        # Shuffle the data
        random.shuffle(data)

        # Split the data into training/validation sets
        self.split_data(data)

        self.representation = Representation({"length": genome_length,
                                              "type": "enum",
                                              "values": ['0', '1'],
                                              "duplicates": True})

        self.population_size = 50
        self.generations = 300
        self.selection_func = tournament
        self.tournament_size = 6
        self.mutation_func = self.mutation_func_plain
        self.mutation_prob = 0.005
        self.crossover_prob = 0.2
        self.elite_count = 6

    def split_data(self, data):
        self.training_set = data[:(len(data) / 1)]
        self.validation_set = data[(len(data) / 1):]

    def fitness_func(self, genome, validate=False):
        """"""
        fitness = 0
        data_set = self.validation_set if validate else self.training_set

        for item in data_set:
            for gene in self.batch_gen(genome, self.gene_length):
                # Don't allow the stupid catch-all gene (ugly hack)
                if gene[0] == '#' and len(set(gene)) == 2:
                    break

                if self.matches(gene[:-1], item[:-1]):
                    if gene[-1] == item[-1]:
                        fitness += 1
                    break

        return fitness

    def matches(self, gene, data):
        """"""
        for i, allele in enumerate(gene):
            if allele == '#':
                continue
            if allele != data[i]:
                return False

        return True

    def crossover_func(self, male, female):
        """"""
        ratio = 0.5
        child1 = list()
        child2 = list()

        longest = male if len(male) < len(female) else female
        shortest = male if len(male) < len(female) else female

        for i, gene in enumerate(shortest):
            if random.random() > ratio:
                child1.append(gene)
                child2.append(longest[i])
            else:
                child1.append(longest[i])
                child2.append(gene)

        return child1, child2
        # return male, female

    def mutation_func_plain(self, individual, probability):
        genes = individual.genes

        for i, gene in enumerate(individual):
            if random.random() < probability:
                if gene == '1':
                    genes[i] = '0'
                else:
                    genes[i] = '1'

        return genes

    def mutation_func_generalisation(self, individual, probability):
        """
        Like standard bit flipping, but with the wildcard character too
        """
        genes = individual.genes

        for i, gene in enumerate(individual):
            if random.random() < probability:
                if (i + 1) % self.gene_length == 0:
                    # Don't put a wildcard in the class position
                    genes[i] = '1' if gene == '0' else '0'

                elif gene == '1':
                    genes[i] = '#' if random.random() < 0.8 else '0'
                else:
                    genes[i] = '#' if random.random() < 0.8 else '1'

        assert genes[-1] != '#'
        return genes

    def batch_gen(self, data, batch_size):
        """"""
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]

    def chunker(self, seq, size):
        return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))
