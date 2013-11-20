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


def bit_flip(genome, probability):
    """
    Mutation function which flips each bit in the given genome with the given
    probability.

    Note: only works for binary representations

    :param genome:  the genome representation to be mutated
    :returns:       the genome, possibly mutated
    """
    genome = list(genome)

    for i, gene in enumerate(genome):
        if random.random() < probability:
            genome[i] = '1' if gene == '0' else '0'

    return ''.join([gene for gene in genome])


def swap(genome, probability):
    """
    Mutation function which swaps the positions of two genes with the given
    probability.

    :param genome:  the genome representation to be mutated
    :returns:       the genome, possibly mutated
    """
    if random.random() < probability:
        r1 = random.randint(0, len(genome) - 1)
        r2 = random.randint(0, len(genome) - 1)
        genome[r1], genome[r2] = genome[r2], genome[r1]
        return genome

    return genome
