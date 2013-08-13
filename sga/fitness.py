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
    """Return the number of 1s in the given binary-encoded genome"""
    return len([i for i in genome if int(i) == 1])


def matching_bits(genome):
    """Return the number of consecutive pairs of matching bits"""
    # TODO
    return 10


def all_small(genome):
    """Return the number of floats less than 0.1"""
    return len([i for i in genome if i < 0.1])


def all_a(genome):
    """Return the number of "a"s in the given genome"""
    return len([i for i in genome if i == 'a'])
