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


class Representation(object):
    """
    Wrapper class to hold information about the user-supplied representation
    dictionary.
    """

    def __init__(self, representation):
        """
        Constructor

        :param representation: the user-supplied representation dictionary
        """
        self.representation = representation

        self.length = representation['length']
        self.type   = representation['type']

        if 'values' in representation:
            self.values = representation['values']
        else:
            self.values = None

        #-----------------------------------------------------------------------
        # "min" is only valid for int and float representations
        #-----------------------------------------------------------------------
        if 'min' in representation:
            self.min = representation['min']
        else:
            if self.type in ('int', 'float'):
                self.min = 0
            else:
                self.min = None

        #-----------------------------------------------------------------------
        # "max" is only valid for int and float representations
        #-----------------------------------------------------------------------
        if 'max' in representation:
            self.max = representation['max']
        else:
            if self.type == 'int':
                self.max = 100
            elif self.type == 'float':
                self.max = 1
            else:
                self.max = None

        if 'duplicates' in representation:
            self.duplicates = representation['duplicates']
        else:
            self.duplicates = True
