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


cdef class Genome(object):
    """
    Class representing a single genome.
    """
    cdef public list genes
    cdef public representation
    cdef public fitness_func
    cdef public natural_fitness
    cdef public int _fitness
    cdef public list average_sigmas
    cdef public dict strategy_params

    def __init__(self, genes, representation, fitness_func, natural_fitness):
        """
        Constructor

        :param           genes:  this genome's actual genes
        :param  representation:  the representation dictionary for this genome
        :param    fitness_func:  the fitness function for this genome
        :param natural_fitness:  use natural fitness values, i.e. higher
                                 fitness value implies fitter individual
        """
        self.genes = genes
        self.representation = representation
        self.fitness_func = fitness_func
        self.natural_fitness = natural_fitness
        self._fitness = -1

    def __repr__(self):
        return repr(self.genes)

    def __len__(self):
        return len(self.genes)

    def __iter__(self):
        return iter(self.genes)

    cpdef int fitness(self, recalculate=False) except *:
        """
        Calculate the fitness of this genome.

        :param recalculate: recalculate the fitness value
        :returns: the fitness value as returned by the user-specified fitness
                  function, standardised
        """
        if recalculate:

            raw_fitness = self.fitness_func(self.genes)

            if self.natural_fitness:
                self._fitness = raw_fitness
            else:
                #---------------------------------------------------------------
                # If standardised fitness is zero we have found the best
                # possible solution. The evolutionary algorithm should not be
                # continuing after finding it.
                #---------------------------------------------------------------
                self._fitness = float('inf') if raw_fitness == 0 \
                    else 1.0 / raw_fitness

        return self._fitness

    cpdef int raw_fitness(self):
        """
        Calculate the raw (natural) fitness of this genome.

        :returns: the fitness value as returned by the user-specified fitness
                  function
        """
        return self.fitness_func(self.genes)

