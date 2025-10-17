
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
import sys

INFINITY = 10000

class MinimaxEngine(object):

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
        
        # Transposition table for caching positions
        self.transposition_table = {}
        
        # Move ordering cache
        self.move_cache = {}
        
        # Corner positions (highest priority)
        self.corners = [(1,1), (1,8), (8,1), (8,8)]
        
        # Edge positions (medium priority)
        self.edges = [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
                      (2,1), (3,1), (4,1), (5,1), (6,1), (7,1),
                      (2,8), (3,8), (4,8), (5,8), (6,8), (7,8),
                      (8,2), (8,3), (8,4), (8,5), (8,6), (8,7)]

    def get_position_hash(self, game):
        """Generate a hash for the current position"""
        return hash(game.export_str() + str(game.get_turn()))

    def alfabeta(self, game, depth, alfa, beta):

        # nodes counter
        self.nodes += 1

        # Check transposition table
        position_hash = self.get_position_hash(game)
        if position_hash in self.transposition_table:
            stored_depth, stored_value, stored_type = self.transposition_table[position_hash]
            if stored_depth >= depth:
                if stored_type == 'exact':
                    return stored_value
                elif stored_type == 'lower' and stored_value >= beta:
                    return stored_value
                elif stored_type == 'upper' and stored_value <= alfa:
                    return stored_value

        # check win/loss
        if game.check_lost():
            return -INFINITY
        if game.check_win():
            return INFINITY

        # evaluate position
        if (depth == 0):
            return game.evaluate()

        # searching all available moves
        move_list = game.get_move_list()

        # handle no move
        if (len(move_list) == 0):
            game.pass_turn()
            value = -self.alfabeta(game, depth-1, -beta, -alfa) 
            game.undo_move()
            return value

        # Enhanced move ordering
        move_list_sorted = self.order_moves(move_list, game)
        
        best_value = -INFINITY
        best_move = None
        original_alfa = alfa
      
        # deep explore all available moves
        for move in move_list_sorted:
            game.move(move)
            value = -self.alfabeta(game, depth-1, -beta, -alfa)
            game.undo_move()

            if value > best_value:
                best_value = value
                best_move = move

            if value > alfa:
                alfa = value

            if alfa >= beta:
                self.pruning += 1
                # Store in transposition table
                self.transposition_table[position_hash] = (depth, beta, 'lower')
                return beta

        # Store in transposition table
        if best_value <= original_alfa:
            self.transposition_table[position_hash] = (depth, best_value, 'upper')
        elif best_value >= beta:
            self.transposition_table[position_hash] = (depth, best_value, 'lower')
        else:
            self.transposition_table[position_hash] = (depth, best_value, 'exact')

        return best_value

    def order_moves(self, move_list, game):
        """Enhanced move ordering for better alpha-beta pruning"""
        move_scores = []
        
        for move in move_list:
            score = 0
            
            # Corner moves (highest priority)
            if (move.x, move.y) in self.corners:
                score += 1000
            
            # Edge moves (medium priority)
            elif (move.x, move.y) in self.edges:
                score += 100
            
            # Priority matrix
            score += self.priority[move.y][move.x]
            
            # Mobility bonus (more moves after this move = better)
            game.move(move)
            mobility = len(game.get_move_list())
            game.undo_move()
            score += mobility * 10
            
            # Stability bonus (pieces that won't be flipped)
            stability = self.calculate_stability(move, game)
            score += stability * 5
            
            move_scores.append((score, move))
        
        # Sort by score (higher is better)
        move_scores.sort(key=lambda x: x[0], reverse=True)
        return [move for score, move in move_scores]

    def calculate_stability(self, move, game):
        """Calculate how stable a move is (pieces that won't be flipped)"""
        # This is a simplified stability calculation
        # In a full implementation, you'd analyze which pieces become stable
        return 0  # Placeholder for now

    def get_best_move(self, game, depth):

        self.nodes = 0
        self.pruning = 0
        # Clear transposition table for new search
        self.transposition_table.clear()

        time_start = time.perf_counter()

        best_value = -INFINITY
        best_move = None

        # searching all available moves
        move_list = game.get_move_list()
        
        # handle no move
        if (len(move_list) == 0):
            return None 

        # Enhanced move ordering
        move_list_sorted = self.order_moves(move_list, game)
        
        # Print header for statistics
        print("\n" + "="*80)
        print("🤖 AI REASONING STATISTICS")
        print("="*80)
        print(f"{'Move':<8} {'Value':<10} {'Best':<10} {'Nodes':<10} {'Pruning':<10} {'Time(s)':<10} {'Rate':<12}")
        print("-"*80)
        
        move_count = 0
        
        # deep explore all available moves
        for move in move_list_sorted:
            game.move(move)
            value = -self.alfabeta(game, depth-1, -INFINITY, -best_value)
            game.undo_move()

            if value > best_value or best_move == None:
                best_value = value
                best_move = move

            # print statistics
            time_diff = time.perf_counter() - time_start
            move_count += 1

            if time_diff > 0:
                time_rate = self.nodes / time_diff
            else:
                time_rate = 0

            # Format statistics with better alignment and symbols
            move_str = str(move)
            value_str = f"{value:>8d}"
            best_str = f"{best_value:>8d}"
            nodes_str = f"{self.nodes:>8d}"
            pruning_str = f"{self.pruning:>8d}"
            time_str = f"{time_diff:>8.3f}"
            rate_str = f"{time_rate:>10.0f}"
            
            # Add visual indicator for best move so far
            if value == best_value and best_move == move:
                move_str = f"⭐{move_str}"
            else:
                move_str = f"🚫{move_str}"

            print(f"{move_str:<8} {value_str:<10} {best_str:<10} {nodes_str:<10} {pruning_str:<10} {time_str:<10} {rate_str:<12}")
        
        # Print summary statistics
        time_total = time.perf_counter() - time_start
        
        print("-"*80)
        print(f"📊 SUMMARY:")
        print(f"   • Total moves evaluated: {move_count}")
        print(f"   • Total nodes analyzed: {self.nodes:,}")
        print(f"   • Pruning operations: {self.pruning:,}")
        print(f"   • Total time: {time_total:.3f} seconds")
        if time_total > 0:
            print(f"   • Average rate: {self.nodes/time_total:,.0f} nodes/second")
        print(f"   • Selected move: {best_move} (value: {best_value})")
        print("="*80 + "\n")

        return best_move
