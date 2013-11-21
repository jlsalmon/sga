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
import copy

import random
from itertools import izip
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
        self.elites     = list()

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
        self.mutation_func  = mutation_func
        self.fitness_func   = fitness_func

        self.representation  = representation
        self.natural_fitness = natural_fitness
        self.crossover_probability = crossover_probability
        self.mutation_probability  = mutation_probability

        #-------------------------------------------------------------------
        # Ensure even elite count
        #-------------------------------------------------------------------
        if elite_count % 2 != 0:
            elite_count += 1
        self.elite_count = elite_count

        self.tournament_size = tournament_size

    def run(self, generations):
        """
        Apply selection, crossover and mutation on the given population as many
        times as the given number of generations.

        :param  population: the initial, random population
        :param generations: the number of generations/cycles to perform
        """
        plotter = Plotter()

        print 'generation=0, total fitness=%d, mean fitness=%s, ' \
              'min individual=%s (%s), max individual=%s (%s)' \
              % (self.total_fitness(), self.mean_fitness(),
                 self.min_individual().genes,
                 self.min_individual().raw_fitness(),
                 self.max_individual().genes,
                 self.max_individual().raw_fitness())

        plotter.update(self.mean_fitness(),
                       self.max_individual().fitness(),
                       self.min_individual().fitness())

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

            min_individual = self.min_individual()
            max_individual = self.max_individual()

            print 'generation=%d, total fitness=%d, mean fitness=%s, ' \
                  'min individual=%s (%s), max individual=%s (%s)' \
                  % (i, self.total_fitness(), self.mean_fitness(),
                     min_individual.genes,
                     min_individual.raw_fitness(),
                     max_individual.genes,
                     max_individual.raw_fitness())
            # print [p.genes for p in population]

            plotter.update(self.mean_fitness(),
                           max_individual.fitness(),
                           min_individual.fitness())

        plotter.plot()

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
                              random.randint(0, 2**self.representation.length)),
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
                            self.representation.length) - 1]
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
        selected_parents = self.selection_func(self.population)
        self.update_population(selected_parents)

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
            child1, child2 = male.genes, female.genes

            #-------------------------------------------------------------------
            # Maybe do the crossover... maybe not
            #-------------------------------------------------------------------
            if random.random() <= probability:
                child1, child2 = self.crossover_func(male.genes, female.genes)

            result.append(Genome(child1, self.representation,
                                 self.fitness_func, self.natural_fitness))
            result.append(Genome(child2, self.representation,
                                 self.fitness_func, self.natural_fitness))

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
            i.genes = self.mutation_func(copy.deepcopy(i.genes), probability)
            result.append(i)

        assert len(result) == len(self.population)
        self.update_population(result)

    def pairwise(self, iterable):
        """
        Make the given iterable into pairs, i.e.:
        s -> (s0,s1), (s2,s3), (s4, s5), ...
        """
        a = iter(iterable)
        return izip(a, a)
