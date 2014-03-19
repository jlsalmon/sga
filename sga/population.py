#-------------------------------------------------------------------------------
# Author: Justin Lewis Salmon <mccrustin@gmail.com>
#-------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

import random
from itertools import izip
from classifier.gene import Gene
from sga.genome import Genome
from sga.plotter import Plotter


class Population(object):
    """
    Class which represents an entire population of individuals.
    """

    def __init__(self, representation, size, fitness_func, selection_func,
                 crossover_func, mutation_func, natural_fitness,
                 crossover_probability, mutation_probability, elite_count,
                 tournament_size):
        """
        Constructor

        :param        representation: the representation dictionary for each
                                      genome in this population
        :param                  size: the number of genomes in this population
        :param          fitness_func: the user-specified fitness function
        :param        selection_func: the user-specified selection function
        :param        crossover_func: the user-specified crossover function
        :param         mutation_func: the user-specified mutation function
        :param       natural_fitness: use natural fitness values, i.e. higher
                                      fitness value implies fitter individual
        :param crossover_probability: the user-specified crossover probability
        :param  mutation_probability: the user-specified mutation probability
        :param           elite_count: the number of fittest individuals to
                                      exclude from selection/crossover/mutation
        :param       tournament_size: the size of a tournament selection group
        """
        self.population = list()
        self.elites = list()

        #-----------------------------------------------------------------------
        # Ensure even population size
        #-----------------------------------------------------------------------
        if size % 2 != 0:
            size += 1
        self.size = size

        #-----------------------------------------------------------------------
        # Ensure 0 < probability < 1
        #-----------------------------------------------------------------------
        if not (0 < float(crossover_probability) < 1) \
            or not (0 < float(mutation_probability) < 1):
            raise ValueError('probabilities must be between 0 and 1')

        self.selection_func = selection_func
        self.crossover_func = crossover_func
        self.mutation_func = mutation_func
        self.fitness_func = fitness_func

        self.representation = representation
        self.natural_fitness = natural_fitness
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        #-------------------------------------------------------------------
        # Ensure even elite count
        #-------------------------------------------------------------------
        if elite_count % 2 != 0:
            elite_count += 1
        self.elite_count = elite_count

        self.tournament_size = tournament_size

        self.plotter = Plotter()

        self.average_sigmas = list()

    def run(self, generations):
        """
        Apply selection, crossover and mutation on the given population as many
        times as the given number of generations.

        :param generations: the number of generations/cycles to perform
        """
        self.calculate_fitnesses()

        #-----------------------------------------------------------------------
        # Print a short summary
        #-----------------------------------------------------------------------
        print 'population size=%d, representation=%s, ' \
              'crossover probability=%f, mutation probability=%f, ' \
              'elite count=%d' \
              % (len(self.population), self.representation,
                 self.crossover_probability, self.mutation_probability,
                 self.elite_count)
        print 'selection scheme=%s, crossover scheme=%s, mutation scheme=%s, ' \
              'fitness function=%s, natural_fitness=%s' \
              % (self.selection_func, self.crossover_func,
                 self.mutation_func,
                 self.fitness_func, self.natural_fitness)

        print 'generation=0, total fitness=%d, mean fitness=%s, ' \
              'min individual=%s (len=%d), max individual=%s (len=%d)' \
              % (self.total_fitness(), self.mean_fitness(),
                 self.min_individual().fitness(),
                 len(self.min_individual()),
                 self.max_individual().fitness(),
                 len(self.max_individual()))

        self.plotter.update(self.mean_fitness(),
                            self.max_individual().fitness(),
                            self.min_individual().fitness())

        for i in self.population:
            if hasattr(i, 'average_sigmas') and i.average_sigmas is not None:
                self.average_sigmas.append(sum(i.average_sigmas)
                                           / len(i.average_sigmas))

        # print self.average_sigmas
        # print len(self.average_sigmas)

        #-----------------------------------------------------------------------
        # Loop for each generation
        #-----------------------------------------------------------------------
        for i in xrange(1, generations):
            #-------------------------------------------------------------------
            # Perform elitism
            #-------------------------------------------------------------------
            self.store_elites()

            #-------------------------------------------------------------------
            # Select the mating pool
            #-------------------------------------------------------------------
            self.select_parents()

            #-------------------------------------------------------------------
            # Apply crossover
            #-------------------------------------------------------------------
            self.crossover(self.crossover_probability)

            #-------------------------------------------------------------------
            # Apply mutation
            #-------------------------------------------------------------------
            self.mutate(self.mutation_probability)

            #-------------------------------------------------------------------
            # Re-add the elites to the population
            #-------------------------------------------------------------------
            self.load_elites()

            #-------------------------------------------------------------------
            # Recalculate fitnesses
            #-------------------------------------------------------------------
            self.calculate_fitnesses()

            min_individual = self.min_individual()
            max_individual = self.max_individual()

            # print 'generation=%d, total fitness=%d, mean fitness=%s, ' \
            #       'min individual=%s (%s), max individual=%s (%s)' \
            #       % (i, self.total_fitness(), self.mean_fitness(),
            #          min_individual.genes,
            #          min_individual.raw_fitness(),
            #          max_individual.genes,
            #          max_individual.raw_fitness())

            print 'generation=%d, total fitness=%d, mean fitness=%s, ' \
                  'min individual=%s (len=%d), max individual=%s (len=%d)' \
                  % (i, self.total_fitness(), self.mean_fitness(),
                     self.min_individual().fitness(),
                     len(self.min_individual()),
                     self.max_individual().fitness(),
                     len(self.max_individual()))

            self.plotter.update(self.mean_fitness(),
                                max_individual.fitness(),
                                min_individual.fitness())

            for i in self.population:
                if hasattr(i, 'average_sigmas') and i.average_sigmas is not None:
                    self.average_sigmas.append(sum(i.average_sigmas)
                                               / len(i.average_sigmas))

            # print self.average_sigmas
            # print len(self.average_sigmas)

    def __iter__(self):
        return iter(self.population)

    def __len__(self):
        return len(self.population)

    def __getitem__(self, item):
        return self.population[item]

    def gen_population(self):
        """
        Generate an initial, random population based on the given representation
        dictionary.
        """

        #-----------------------------------------------------------------------
        # Generate binary population
        #-----------------------------------------------------------------------
        if self.representation.type == 'binary':
            for _ in xrange(self.size):
                fmt = '{0:0' + str(self.representation.length) + 'b}'
                gene = Genome(fmt.format(
                    random.randint(0, 2 ** self.representation.length)),
                              representation=self.representation,
                              fitness_func=self.fitness_func,
                              natural_fitness=self.natural_fitness)
                self.population.append(gene)

        #-----------------------------------------------------------------------
        # Generate float value population
        #-----------------------------------------------------------------------
        elif self.representation.type == 'float':
            for _ in xrange(self.size):
                gene = Genome([random.uniform(self.representation.min,
                                              self.representation.max)
                               for _ in xrange(self.representation.length)],
                              representation=self.representation,
                              fitness_func=self.fitness_func,
                              natural_fitness=self.natural_fitness)
                self.population.append(gene)

        #-----------------------------------------------------------------------
        # Generate integer value population
        #-----------------------------------------------------------------------
        elif self.representation.type == 'int':
            for _ in xrange(self.size):
                gene = Genome([random.randint(self.representation.min,
                                              self.representation.max)
                               for _ in xrange(self.representation.length)],
                              representation=self.representation,
                              fitness_func=self.fitness_func,
                              natural_fitness=self.natural_fitness)
                self.population.append(gene)

        #-----------------------------------------------------------------------
        # Generate fixed value population
        #-----------------------------------------------------------------------
        elif self.representation.type == 'enum':
            for _ in xrange(self.size):

                #---------------------------------------------------------------
                # Allow duplicates
                #---------------------------------------------------------------
                if self.representation.duplicates:
                    gene = [self.representation.values[random.randint(0,
                                len(self.representation.values)) - 1]
                            for _ in xrange(self.representation.length)]
                #---------------------------------------------------------------
                # Disallow duplicates
                #---------------------------------------------------------------
                else:
                    import copy

                    gene = copy.copy(self.representation.values)
                    random.shuffle(gene)

                gene = Genome(gene,
                              representation=self.representation,
                              fitness_func=self.fitness_func,
                              natural_fitness=self.natural_fitness)
                self.population.append(gene)

    def calculate_fitnesses(self):
        """"""
        for i in self.population:
            i.fitness(recalculate=True)

    def update_population(self, population):
        """
        Change the existing population to the new one

        :param population: the new population to use
        """
        self.population = population

    def total_fitness(self):
        """
        Return the total fitness of all of the individuals in the population
        """
        return sum([i.fitness() for i in self.population])

    def mean_fitness(self):
        """
        Return the mean fitness of all of the individuals in the population
        """
        return self.total_fitness() / len(self.population)

    def max_individual(self):
        """
        Return the individual with the maximum (highest) fitness of all the
        individuals in the population
        """
        max_indiv = self.population[0]

        for i in self.population:
            if i.fitness() > max_indiv.fitness():
                max_indiv = i

        return max_indiv

    def min_individual(self):
        """
        Return the individual with the  minimum (lowest) fitness of all the
        individuals in the population
        """
        min_indiv = self.population[0]

        for i in self.population:
            if i.fitness() < min_indiv.fitness():
                min_indiv = i

        return min_indiv

    def store_elites(self):
        """
        Perform elitism by withholding a certain number of the fittest
        individuals from selection/crossover/mutation.
        """
        del self.elites[:]

        for i in xrange(self.elite_count):
            max_indiv = self.max_individual()
            self.elites.append(max_indiv)
            self.population.remove(max_indiv)

    def load_elites(self):
        """
        Re-add the withheld elites back into the population
        """
        self.population += self.elites

    def select_parents(self):
        """
        Perform population selection using the user-supplied selection function.
        """
        selected_parents = self.selection_func(self)
        self.update_population([self.make_copy(i) for i in selected_parents])

    def crossover(self, probability):
        """
        Perform crossover using the user-supplied crossover function

        :param probability: the probability that crossover will occur for each
                            pair of individuals
        """
        result = list()

        #-----------------------------------------------------------------------
        # Loop the population in twos
        #-----------------------------------------------------------------------
        for male, female in self.pairwise(self.population):
            child1, child2 = self.make_copy(male), self.make_copy(female)

            #-------------------------------------------------------------------
            # Maybe do the crossover... maybe not
            #-------------------------------------------------------------------
            if random.random() <= probability:
                child1.genes, child2.genes = self.crossover_func(child1.genes,
                                                                 child2.genes)

                # male.genes   = child1[:]
                # female.genes = child2[:]

            result.append(child1)
            result.append(child2)

                # result.append(Genome(child1, self.representation,
                #                      self.fitness_func, self.natural_fitness))
                # result.append(Genome(child2, self.representation,
                #                      self.fitness_func, self.natural_fitness))

        assert len(result) == len(self.population)

        #-----------------------------------------------------------------------
        # Switch to the new population
        #-----------------------------------------------------------------------
        self.update_population(result)

    def mutate(self, probability):
        """
        Perform mutation using the user-supplied mutation function

        :param probability: the probability that mutation will occur for each
                            individual
        """
        result = list()

        for i in self.population:
            #-------------------------------------------------------------------
            # Make a copy of the genes
            #-------------------------------------------------------------------
            # i.genes = self.mutation_func(copy.deepcopy(i.genes), probability)
            indiv_copy = self.make_copy(i)
            genes = self.mutation_func(indiv_copy, probability)
            indiv_copy.genes = genes
            result.append(indiv_copy)

        assert len(result) == len(self.population)
        self.update_population(result)

    def make_copy(self, individual):
        if isinstance(individual.genes[0], Gene):

            genes_copy = list()
            for gene in individual.genes:
                gene_copy = Gene(gene.alleles[:])
                gene_copy.class_label = gene.class_label
                if gene.mutation_step_sizes is not None:
                    gene_copy.mutation_step_sizes = gene.mutation_step_sizes[:]
                genes_copy.append(gene_copy)

            genome = Genome(genes_copy, individual.representation,
                    individual.fitness_func,
                    individual.natural_fitness)

        else:
            genome = Genome(individual.genes[:], individual.representation,
                            individual.fitness_func,
                            individual.natural_fitness)

        genome._fitness = individual._fitness
        if hasattr(individual, 'strategy_params') \
                and individual.strategy_params is not None:
            genome.strategy_params = individual.strategy_params.copy()
        if hasattr(individual, 'average_sigmas') \
                and individual.average_sigmas is not None:
            genome.average_sigmas = individual.average_sigmas[:]

        return genome

    def pairwise(self, iterable):
        """
        Make the given iterable into pairs, i.e.:
        s -> (s0,s1), (s2,s3), (s4, s5), ...
        """
        a = iter(iterable)
        return izip(a, a)

    def show_plot(self):
        self.plotter.show()

    def add_to_plot(self, data, label):
        self.plotter.add_to_plot(data, label)

