import random
import math
from classifier.BinaryClassifier import BinaryClassifier
from classifier.gene import Gene
from sga.representation import Representation
from sga.selection import tournament, roulette

cdef class RealValueClassifier(object):
    """
    Real-value classification
    """
    cdef public list training_set
    cdef public list validation_set
    cdef public int gene_length
    cdef public int genome_length
    cdef public representation
    cdef public int population_size
    cdef public int generations
    cdef public list genome_lengths
    cdef public list average_sigmas
    cdef public mutation_func
    cdef public mutation_step_size
    cdef public double mutation_prob
    cdef public double crossover_prob
    cdef public int tournament_size
    cdef public int elite_count
    cdef public double tau
    cdef public double tau_
    cdef public double common

    def __init__(self, data, gene_length, genome_length):
        """"""
        self.gene_length = gene_length
        self.genome_length = genome_length

        # Shuffle the data
        random.shuffle(data)

        # Split the data into training/validation sets
        self.split_data(data)

        self.representation = Representation({"length": (gene_length * 40),
                                              "type": "float"})
        self.population_size = 100
        self.generations = 1000
        self.genome_lengths = list()
        self.average_sigmas = list()

        # self.mutation_func = self.mutation_func_step
        self.mutation_step_size = 0.05

        # self.mutation_func = self.mutation_func_one_sigma

        self.mutation_func = self.mutation_func_n_sigma
        self.common_sd = 0.5
        self.bound_sd = 1
        self.spread_sd = 1

        print 'mutation operator:', self.mutation_func
        self.mutation_prob = 0.01
        self.crossover_prob = 0.4

        self.tournament_size = 10
        self.elite_count = 2

        n = self.representation.length
        self.tau = 1 / math.sqrt(2 * math.sqrt(n))
        self.tau_ = 1 / math.sqrt(2 * n)

        # self.fitness_func = fitness_func

    def split_data(self, data):
        # 1/2 training data, 1/2 validation
        self.training_set = data[:(len(data) / 2)]
        self.validation_set = data[(len(data) / 2):]

    def batch_gen(self, data, batch_size):
        """"""
        cdef int i
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]

    cpdef fitness_func(self, genome, validate=False):
        """"""
        cdef list data_set
        data_set = self.validation_set if validate else self.training_set

        return fitness_func(genome, data_set)

    def crossover_func(self, male, female):
        """"""
        if len(male) != len(female):
            minlen = min(len(i) for i in [male, female])
            del male[minlen:]
            del female[minlen:]

        for i, gene in enumerate(male):
            for j, allele in enumerate(gene.alleles):
                if random.random() > 0.5:
                    male[i].alleles[j], female[i].alleles[j] \
                    = female[i].alleles[j], male[i].alleles[j]

            # for j, step in enumerate(gene.mutation_step_sizes):
            #     if random.random() > 0.5:
                    male[i].mutation_step_sizes[j], \
                    female[i].mutation_step_sizes[j] \
                    = female[i].mutation_step_sizes[j], \
                      male[i].mutation_step_sizes[j]

        return male, female

    def mutation_func_step(self, individual, probability):
        """
        Randomly +/- step
        """
        genes = individual.genes
        step = self.mutation_step_size

        for gene in genes:
            for i, pair in enumerate(chunker(gene.alleles, 2)):

                lower = pair[0]
                upper = pair[1]

                # Mutate lower bound
                if random.random() < probability:
                    if random.random() < 0.5:
                        lower += step
                    else:
                        lower -= step

                # Mutate upper bound
                if random.random() < probability:
                    if random.random() < 0.5:
                        upper += step
                    else:
                        upper -= step

                # Make sure lower < upper
                if lower > upper:
                    lower, upper = upper, lower

                if lower < 0: lower = 0.0
                if upper > 1: upper = 1.0

                pos = i * 2
                gene.alleles[pos], gene.alleles[pos + 1] = lower, upper

        # Update info for plotter
        self.genome_lengths.append(len(individual))

        # genes = self.mutate_length(genes)

        return genes

    def mutation_func_one_sigma(self, individual, probability):
        """Squash the upper and lower bounds"""
        genes = individual.genes

        sigma = individual.strategy_params['mutation_step_size']
        tau = 1 / math.sqrt(self.representation.length)
        # tau = 1

        sigma_ = sigma
        # Mutate sigma
        # if random.random < probability:
        sigma_ = sigma * math.exp(tau * random.normalvariate(0, 0.5))

        # Boundary rule
        if sigma_ < 0.001: sigma_ = 0.001

        # Save sigma
        individual.strategy_params['mutation_step_size'] = sigma_

        for gene in genes:
            for i, pair in enumerate(chunker(gene.alleles, 2)):

                lower = pair[0]
                upper = pair[1]

                # Mutate lower bound
                if random.random() < sigma_:
                    lower += (random.normalvariate(0, 1))

                # Mutate upper bound
                if random.random() < sigma_:
                    upper += (random.normalvariate(0, 1))

                # Make sure lower < upper
                if lower > upper:
                    lower, upper = upper, lower

                if lower < 0: lower = 0.0
                if upper > 1: upper = 1.0

                assert lower >= 0
                assert upper <= 1

                pos = i * 2
                gene.alleles[pos], gene.alleles[pos + 1] = lower, upper


        # Update info for plotter
        self.genome_lengths.append(len(individual))

        # genes = self.mutate_length(genes)
        return genes

    def mutation_func_n_sigma(self, individual, probability):
        """"""
        genes = individual.genes
        average_sigmas = list()

        common = random.normalvariate(0, self.common_sd)

        for gene in genes:

            for i, pair in enumerate(self.batch_gen(gene.alleles, 2)):
                pos = i * 2

                lower_sigma = gene.mutation_step_sizes[pos]
                upper_sigma = gene.mutation_step_sizes[pos + 1]

                n = self.representation.length
                tau = 1 / math.sqrt(2 * math.sqrt(n))
                tau_ = 1 / math.sqrt(2 * n)

                # tau = 0.35
                # tau_ = 0.2

                lower_spread = random.normalvariate(0, self.spread_sd)
                upper_spread = random.normalvariate(0, self.spread_sd)

                # Mutate sigma values
                lower_sigma_ = lower_sigma * math.exp(
                    tau_ * common #random.normalvariate(0, 0.5)
                    + tau * lower_spread) #random.normalvariate(0,
                    # lower_sigma))
                upper_sigma_ = upper_sigma * math.exp(
                    tau_ * common #random.normalvariate(0, 0.5)
                    + tau * upper_spread) #random.normalvariate(0,
                    # upper_sigma))

                # Boundary rule
                epsilon = 0.001
                if lower_sigma_ < epsilon: lower_sigma_ = epsilon
                if upper_sigma_ < epsilon: upper_sigma_ = epsilon

                # Save sigma values
                gene.mutation_step_sizes[pos] = lower_sigma_
                gene.mutation_step_sizes[pos + 1] = upper_sigma_

                lower = pair[0]
                upper = pair[1]

                # Mutate lower bound
                if random.random() < lower_sigma_:
                    lower += (random.normalvariate(0, self.bound_sd))
                # lower += lower_sigma_ * random.normalvariate(0, self.bound_sd)

                if lower > 1: lower = 1.0
                if lower < 0: lower = 0.0

                # Mutate upper bound
                if random.random() < upper_sigma_:
                    upper += (random.normalvariate(0, self.bound_sd))
                # upper += upper_sigma_ * random.normalvariate(0, self.bound_sd)

                if upper > 1: upper = 1.0
                if upper < 0: upper = 0.0

                # Make sure lower < upper
                if lower > upper:
                    lower, upper = upper, lower

                gene.alleles[pos], gene.alleles[pos + 1] = lower, upper

            # Update info for plotter
            average_sigmas.append(sum(gene.mutation_step_sizes)
                                  / len(gene.mutation_step_sizes))

        # Update info for plotter
        self.genome_lengths.append(len(individual))

        individual.average_sigmas.append(sum(average_sigmas)
                                         / len(average_sigmas))
        # print self.average_sigmas
        # print len(self.average_sigmas)

        #genes = self.mutate_length(genes)
        return genes

    def mutate_length(self, genes):
        """"""
        length_change_prob = 0.01

        # Randomly delete a gene, or add a new gene
        if random.random() < length_change_prob:
            if random.random() < 0.5 \
                    and not len(genes) == self.gene_length:
                # Delete a random gene
                pos = random.randint(0, len(genes) - 1)
                # rem = pos % self.gene_length
                #
                # if rem != 0:
                #     pos -= rem

                del genes[pos]
            else:
                if not len(genes) > 140:  # Cheating!
                    # Add a new gene
                    genes.append(self.make_new_gene())
        return genes

    def selection_func(self, population):
        return tournament(population)

    def make_new_gene(self):
        gene = Gene([random.uniform(0, 1) for _ in xrange(self.gene_length)])
        gene.class_label = 1 if random.random() < 0.5 else 0
        gene.mutation_step_sizes = [0.05 for _
                                    in xrange(self.gene_length)]
        return gene

cdef int fitness_func(genome, data_set) except *:
    """"""
    fitness = 0

    # Is each gene within a specific bound? Creating boxes in the input
    # space

    cdef list item
    cdef list alleles

    for item in data_set:
        for gene in genome:
            alleles = gene.alleles

            # if gene.class_label != item[-1]:
            #     continue
            #
            # match = matches(alleles, item)
            #
            # if match == -1:
            #     fitness -= 1
            #
            # if match == 1:
            #     fitness += 1
            # break

            match = matches(alleles, item[:-1])
            if match == -1:
                fitness -= 1

            if match == 1:
                if gene.class_label == item[-1]:
                    fitness += 1
                break

    return fitness

cdef int matches(gene, data) except *:
    cdef int i, num_generic = 0
    cdef list pair
    cdef double lower, upper

    for i, pair in enumerate(chunker(gene, 2)):

        lower = pair[0]
        upper = pair[1]

        if lower > upper:
            lower, upper = upper, lower

        if lower < 0.1 and upper > 0.9:
            num_generic += 1

        if not lower < data[i] < upper:
            return 0

    #  Have to do a hack to make sure the whole thing isn't generic... What am
    #  I doing wrong?
    #     if num_generic >= (len(gene) / 2):
    #         return -1

    return 1

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
