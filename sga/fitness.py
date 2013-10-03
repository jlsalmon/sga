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
    # TODO: implement this
    return 10

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
