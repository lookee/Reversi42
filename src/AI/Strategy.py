
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
import time

INFINITY = 10000

class Strategy(object):

    def __init__(self):

        # init:
        # alfa-beta priority sorting:
        #
        #  | 1| 2| 3| 4| 5| 6| 7| 8|
        #--+--+--+--+--+--+--+--+--+
        #1 |  |  |  |  |  |  |  |  |
        #--+--+--+--+--+--+--+--+--+
        #2 |  |  |  |  |  |  |  |  |
        #--+--+--+--+--+--+--+--+--+
        #3 |  |  |  |  |  |  |  |  |
        #--+--+--+--+--+--+--+--+--+
        #4 |  |  |  |##|##|  |  |  |
        #--+--+--+--+--+--+--+--+--+
        #5 |  |  |  |##|##| 2| 4| 6|
        #--+--+--+--+--+--+--+--+--+
        #6 |  |  |  |  | 2| 3| 5| 7|
        #--+--+--+--+--+--+--+--+--+
        #7 |  |  |  |  | 4| 7| 9| 8|
        #--+--+--+--+--+--+--+--+--+
        #8 |  |  |  |  | 6| 7| 8| 1|
        #--+--+--+--+--+--+--+--+--+
        
        self.priority = [ 
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 1, 8, 7, 6, 6, 7, 8, 1 ], 
            [ 0, 8, 9, 7, 4, 4, 7, 9, 8 ], 
            [ 0, 7, 5, 3, 2, 2, 3, 5, 7 ], 
            [ 0, 6, 4, 2, 0, 0, 2, 4, 6 ], 
            [ 0, 6, 4, 2, 0, 0, 2, 4, 6 ], 
            [ 0, 7, 5, 3, 2, 2, 3, 5, 7 ], 
            [ 0, 8, 9, 7, 4, 4, 7, 9, 8 ], 
            [ 0, 1, 8, 7, 6, 6, 7, 8, 1 ], 
        ]

    def alfabeta(self, game, depth, alfa, beta):

        # best value
        best_value = -INFINITY

        # nodes counter
        self.nodes += 1

        # check win
        if game.check_lost():
            return -INFINITY

        # evaluate position
        if (depth == 0):
            return game.evaluate()

        # searching all available moves
        move_list = game.get_move_list()

        # handle no move
        if (len(move_list) == 0):
        # pass turn
            game.pass_turn()
            value = -self.alfabeta(game, depth-1, -beta, -alfa) 
            game.undo_move()
            return value

        # sort move list with a weighted matrix
        move_list_sorted =  [];
        for move in move_list:
            move_list_sorted.append((self.priority[move.y][move.x], move))
            
        move_list_sorted = sorted(move_list_sorted, key=lambda row: row[0], reverse=False)
      
        # deep explore all available moves
        for m in (move_list_sorted):
            v, move = m

            game.move(move)
            value = -self.alfabeta(game, depth-1, -beta, -alfa)
            game.undo_move()

            if value > best_value:
                best_value = value

            if value > alfa:
                alfa = value

            if alfa >= beta:
                self.pruning += 1
                break

        return best_value

    def get_best_move(self, game, depth):

        self.nodes = 0
        self.pruning = 0

        time_start = time.clock()

        best_value = -INFINITY
        best_move = None

        # searching all available moves
        move_list = game.get_move_list()
        
        # handle no move
        if (len(move_list) == 0):
            return None 

        # sort move list with a weighted matrix
        move_list_sorted =  [];
        for move in move_list:
            move_list_sorted.append((self.priority[move.y][move.x], move))
            
        move_list_sorted = sorted(move_list_sorted, key=lambda row: row[0], reverse=False)
        
        # deep explore all available moves
        for m in (move_list_sorted):
            v, move = m
            game.move(move)
            value = -self.alfabeta(game, depth-1, -INFINITY, -best_value)
            game.undo_move()

            if value > best_value or best_move == None:
                best_value = value
                best_move = move

            # print statistics
            time_diff = time.clock() - time_start

            if time_diff > 0:
                time_rate = self.nodes / time_diff
            else:
                time_rate = 0

            print "move: %s value: %8d best: %8d nodes: %8d pruning: %8d time: %5d rate %.02f [nodes/s]" \
                 %(move, value, best_value, self.nodes, self.pruning, time_diff, time_rate)

        return best_move
