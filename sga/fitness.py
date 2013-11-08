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
from itertools import izip


def all_ones(genome):
    """
    Fitness function based upon the number of 1s in the representation. This
    function only makes sense to use for binary representations.

    :param genome: the individual genome to evaluate
    :returns:      the number of 1s in the genome
    """
    return len([i for i in genome if int(i) == 1])


def matching_bits(genome):
    """
    Fitness function based upon the number of pairs of matching bits in the
    representation. E.g. the genome 11001100 would have a fitness value of 4,
    while the genome 10101010 would have a fitness of 0.

    :param genome: the individual genome to evaluate
    :returns:      the number of consecutive pairs of matching bits in the
                   genome
    """
    a = iter(genome)
    total = 0

    for gene1, gene2 in izip(a, a):
        if gene1 == gene2:
            total += 1

    return total

#-------------------------------------------------------------------------------
# Static map for the TSP problem with 5 cities
#-------------------------------------------------------------------------------
tsp5_map = [
    [0,  5,  7, 4, 15],
    [5,  0,  3, 4, 10],
    [7,  3,  0, 2, 7],
    [4,  4,  2, 0, 9],
    [15, 10, 7, 9, 0]
]

tsp15_map = [
    [0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46],
    [29,  0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21],
    [82, 55,  0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51],
    [46, 46, 68,  0, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
    [68, 42, 46, 82,  0, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
    [52, 43, 55, 15, 74,  0, 61, 23, 55, 31, 33, 37, 51, 29, 59],
    [72, 43, 23, 72, 23, 61,  0, 42, 23, 31, 77, 37, 51, 46, 33],
    [42, 23, 43, 31, 52, 23, 42, 0, 33,  15, 37, 33, 33, 31, 37],
    [51, 23, 41, 62, 21, 55, 23, 33,  0, 29, 62, 46, 29, 51, 11],
    [55, 31, 29, 42, 46, 31, 31, 15, 29,  0, 51, 21, 41, 23, 37],
    [29, 41, 79, 21, 82, 33, 77, 37, 62, 51,  0, 65, 42, 59, 61],
    [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65,  0, 61, 11, 55],
    [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61,  0, 62, 23],
    [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62,  0, 59],
    [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59,  0]
]


def tsp_15(genome):
    """
    TSP for 15 cities
    """
    if len(genome) != len(set(genome)):
        print genome
        raise ValueError('TSP tour not valid. Fix the crossover/mutation func')

    v = list()

    for i, gene in enumerate(genome):
        j = i + 1 if i != (len(genome) - 1) else 0
        v.append(tsp15_map[ord(genome[i]) - 65][ord(genome[j]) - 65])

    return sum(v)


def tsp_5(genome):
    """
    Travelling salesman problem with 5 cities:

        A   B   C   D   E
    ----------------------
    A | -   5   7   4   15
    B | 5   -   3   4   10
    C | 7   3   -   2   7
    D | 4   4   2   -   9
    E | 15  10  7   9   -

    The genome is simply the tour, i.e. CDABE

    Shorter tour represents higher fitness
    """
    #---------------------------------------------------------------------------
    # Check that the tour is valid, i.e. hasn't been screwed up by crossover or
    # mutation
    #---------------------------------------------------------------------------
    if len(genome) != len(set(genome)):
        print genome
        raise ValueError('TSP tour not valid. Fix the crossover/mutation func')

    v0 = tsp5_map[ord(genome[0]) - 65][ord(genome[1]) - 65]
    v1 = tsp5_map[ord(genome[1]) - 65][ord(genome[2]) - 65]
    v2 = tsp5_map[ord(genome[2]) - 65][ord(genome[3]) - 65]
    v3 = tsp5_map[ord(genome[3]) - 65][ord(genome[4]) - 65]
    v4 = tsp5_map[ord(genome[4]) - 65][ord(genome[0]) - 65]

    v = v0 + v1 + v2 + v3 + v4
    return v


def all_small(genome):
    """
    Return the number of floats less than 0.1
    """
    return len([i for i in genome if i < 0.1])


def all_a(genome):
    """
    Return the number of "a"s in the given genome
    """
    return len([i for i in genome if i == 'a'])
