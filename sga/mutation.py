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


def bit_flip(genome):
    """
    Mutation function which simply flips a random bit.

    Note: only works for binary representations

    :param genome:  the genome representation to be mutated
    :returns:       the newly mutated genome
    """
    fmt = '{0:0' + str(len(genome)) + 'b}'
    return fmt.format(int(genome, 2) ^ 1
                      << random.randint(0, len(genome)))[:len(genome)]


def swap(genome):
    """
    Mutation function which swaps the positions of two alleles.

    :param genome:  the genome representation to be mutated
    :returns:       the newly mutated genome
    """
    r1 = random.randint(0, len(genome) - 1)
    r2 = random.randint(0, len(genome) - 1)
    genome[r1], genome[r2] = genome[r2], genome[r1]
    return genome
