
#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Reversi42 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Reversi42.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

class BoardModel(object):

    def __init__(self, sizex, sizey):
       
        self.sizex = sizex
        self.sizey = sizey

        self.matrix = [[0 for row in range(self.sizey)] for col in range(self.sizex)]

    def setPoint(self, x, y, v):
        self.matrix[x][y] = v

    def unsetPoint(self, x, y):
        self.setPoint(x, y, 0)

    def getPoint(self, x, y):
        return self.matrix[x][y]

