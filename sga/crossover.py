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


def single_point(male, female):
    """
    Return two new children after performing single point crossover

    :param   male: the first parent
    :param female: the second parent
    :returns:      tuple containing two newly crossed-over children
    """
    crossover_point = random.randint(0, len(male))

    # sexy time
    child1 = male[:crossover_point] + female[crossover_point:]
    child2 = male[crossover_point:] + female[:crossover_point]

    return child1, child2


def uniform(male, female):
    """
    Return two new children after performing uniform crossover

    :param   male: the first parent
    :param female: the second parent
    :returns:      tuple containing two newly crossed-over children
    """
    # TODO: implement this
    return male, female
