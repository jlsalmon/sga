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
    while the genome 10101010 would ahve a fitness of 0.

    :param genome: the individual genome to evaluate
    :returns:      the number of consecutive pairs of matching bits in the
                   genome
    """
    # TODO: implement this
    return 10


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
