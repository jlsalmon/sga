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
from sga.genome import Genome


class Population(object):
    """
    Class which represents an entire population of individuals.
    """

    def __init__(self, representation, size, fitness_func, selection_func,
                 crossover_func, mutation_func, crossover_probability,
                 mutation_probability):
        """
        Constructor

        :param        representation: the representation dictionary for each
                                      genome in this population
        :param                  size: the number of genomes in this population
        :param          fitness_func: the user-specified fitness function
        :param        selection_func: the user-specified selection function
        :param        crossover_func: the user-specified crossover function
        :param         mutation_func: the user-specified mutation function
        :param crossover_probability: the user-specified crossover probability
        :param  mutation_probability: the user-specified mutation probability
        """
        self.population = list()

        #-----------------------------------------------------------------------
        # Ensure even population size
        #-----------------------------------------------------------------------
        if size % 2 != 0:
            size += 1
        self.size = size

        self.representation = representation
        self.fitness_func   = fitness_func
        self.selection_func = selection_func
        self.crossover_func = crossover_func
        self.mutation_func  = mutation_func
        self.crossover_probability = crossover_probability
        self.mutation_probability  = mutation_probability

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
                              fitness_func=self.fitness_func)
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
                              fitness_func=self.fitness_func)
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
                              fitness_func=self.fitness_func)
                self.population.append(gene)

        #-----------------------------------------------------------------------
        # Generate fixed value population
        #-----------------------------------------------------------------------
        elif self.representation.type == 'enum':
            for _ in xrange(self.size):
                # TODO: disallow duplicates if necessary
                gene = [self.representation.values[random.randint(0,
                                            self.representation.length) - 1]
                        for _ in xrange(self.representation.length)]
                gene = Genome(gene,
                              representation=self.representation,
                              fitness_func=self.fitness_func)
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

    def select_parents(self):
        return self.selection_func(self.population)

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

            result.append(Genome(child1, self.representation, self.fitness_func))
            result.append(Genome(child2, self.representation, self.fitness_func))

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
        for i in self.population:
            if random.random() <= probability:
                i.genes = self.mutation_func(i.genes)

    def pairwise(self, iterable):
        """
        Make the given iterable into pairs, i.e.:
        s -> (s0,s1), (s2,s3), (s4, s5), ...
        """
        a = iter(iterable)
        return izip(a, a)
