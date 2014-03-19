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
        self.lowest_fitnesses  = list()
        self.extra = list()

    def update(self, average_fitness, highest_fitness, lowest_fitness):
        self.average_fitnesses.append(average_fitness)
        self.highest_fitnesses.append(highest_fitness)
        self.lowest_fitnesses.append(lowest_fitness)

    def plot(self):

        fig, ax1 = pyplot.subplots()
        fig.set_size_inches(8, 6)

        p1 = ax1.plot(self.average_fitnesses, '-',
                 self.highest_fitnesses, '-',
                 self.lowest_fitnesses, 'k.')
        p = p1
        ax1.set_ylabel('fitness')
        ax1.set_xlabel('generation')

        # Shink current axis by 20%
        box = ax1.get_position()
        ax1.set_position([box.x0, box.y0, box.width, box.height * 0.9])

        # l1 = pyplot.legend(['average fitness',
        #                     'max individual',
        #                     'min individual'],
        #                    bbox_to_anchor=(-0.01, 1.2),
        #                    loc='upper left',
        #                    ncol=2)

        if len(self.extra):
            ax2 = ax1.twinx()
            p2 = ax2.plot(self.extra, 'r-')
            ax2.set_ylabel(self.extra_label, color='r')

            for tl in ax2.get_yticklabels():
                tl.set_color('r')
            # l2 = pyplot.legend([self.extra_label],
            #                    bbox_to_anchor=(1.0, 1.2),
            #                    loc='upper right')
            # pyplot.gca().add_artist(l1)

            p = p1 + p2
        # labs = [l.get_label() for l in p]
        # ax1.legend(p, labs, loc=0)

        if hasattr(self, 'extra_label'):
            ax1.legend(p, ['average fitness',
                            'max individual',
                            'min individual',
                            self.extra_label],
                           bbox_to_anchor=(0.5, 1.2),
                           loc='upper center',
                           ncol=2)
        else:
            ax1.legend(p, ['average fitness',
                            'max individual',
                            'min individual'],
                           bbox_to_anchor=(0.5, 1.2),
                           loc='upper center',
                           ncol=2)

        # pyplot.legend([self.average_fitnesses, self.highest_fitnesses,
        #                self.lowest_fitnesses, self.extra],
        #               ['average fitness', 'max individual',
        #                   'min individual',
        #                self.extra_label],
        #               loc='lower right')

    def add_to_plot(self, data, label):
        self.extra = data
        self.extra_label = label

    def show(self):
        self.plot()
        pyplot.show()

