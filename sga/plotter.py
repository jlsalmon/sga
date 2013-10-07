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
from matplotlib import pyplot


class Plotter(object):
    """"""
    def __init__(self):
        self.average_fitnesses = list()
        self.highest_fitnesses = list()

    def update(self, average_fitness, highest_fitness):
        self.average_fitnesses.append(average_fitness)
        self.highest_fitnesses.append(highest_fitness)

    def plot(self):
        pyplot.plot(self.average_fitnesses)
        pyplot.plot(self.highest_fitnesses)
        pyplot.ylabel('fitness')
        pyplot.xlabel('generation')
        pyplot.legend(['average fitness', 'max individual'],
                      loc='lower right')
        pyplot.show()
