#!/usr/bin/env python

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

from Reversi.Game import Game
from Reversi.Game import Move

from Players.HumanPlayer import HumanPlayer
from Players.AIPlayer import AIPlayer
from Players.Monkey import Monkey

from Board.BoardControl import BoardControl

size = 8

g = Game(size)

players={'B': HumanPlayer(), 'W': AIPlayer(6)}

c = BoardControl(size,size)

game_history = ""
last_move = None

while 1:

    turn = g.get_turn()

    player = players[turn]

    print "%s is moving..." % player.get_name()

    moves = g.get_move_list()
    
    if len(moves)>0:

        # import board position
        c.importModel(g.export_str())

        # show all available moves
        for move in (moves):
            print move
            c.setCanMove(move.get_x(),move.get_y(),turn)

        # render board
        c.renderModel()    
        c.cursorWait()

        # render ascii board
        g.view()

        # history and last move
        print "\ngame history:\n%s\n" % game_history
        print "last move: %s" % last_move

        # get move
        move = player.get_move(g,moves,c)

        # move
        g.move(move)

        # update game history
        if turn == 'B':
            # is a black move
            last_move = str(move).upper()
        else:
            # is a white move
            last_move = str(move).lower()

        game_history += last_move

        print "move: %s" %move

    else:
        g.pass_turn()
        print "%s is passing" % player.get_name()

    if g.is_finish():
        break

# print results

c.importModel(g.export_str())
c.renderModel()

g.view()
g.result()

print "\ngame history:\n%s\n" % game_history
