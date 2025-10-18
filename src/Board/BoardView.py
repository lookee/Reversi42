
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

"""
BoardView - Backward Compatibility Wrapper

This module maintains backward compatibility by importing PygameBoardView.
All new code should use PygameBoardView directly or the abstract interface.

Version: 3.1.0
"""

from .PygameBoardView import PygameBoardView

# Backward compatibility: BoardView is now an alias for PygameBoardView
BoardView = PygameBoardView
