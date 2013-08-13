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


class Genome(object):
    """
    Class representing a single genome.
    """

    def __init__(self, genes, representation, fitness_func):
        """
        Constructor

        :param          genes:  this genome's actual genes
        :param representation:  the representation dictionary for this genome
        :param   fitness_func:  the fitness function for this genome
        """
        self.genes          = genes
        self.representation = representation
        self.fitness_func   = fitness_func

    def fitness(self):
        """
        Calculate the fitness of this genome.

        :returns: the fitness value as returned by the user-specified fitness
                  function
        """
        return self.fitness_func(self.genes)
