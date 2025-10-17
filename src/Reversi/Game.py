
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

ROWNAME = ' ABCDEFGH'

class Move(object):
    """base class to handle moves"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.get_move()
    
    def __eq__(self, other):
        """Compare moves for equality"""
        if not isinstance(other, Move):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        """Make Move hashable for use in sets/dicts"""
        return hash((self.x, self.y))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_move(self):
        return "%s%d"%(ROWNAME[self.x],self.y)


class Game(object):
    """base class with game details"""
    
    def __init__(self, size):

        self.size = size
        self.limit = size + 1
        self.cells_cnt  = size ** 2

        self.turn_cnt = 0
        self.board_position_stack = []
        
        # Game history for opening book (case-sensitive: uppercase=black, lowercase=white)
        self.history = ""

        # first move
        self.turn = 'B'

        # init board
        self.matrix = [['.' for row in range(self.size+2)] for col in range(self.size+2)]

        # board start position
        center = size//2 - 1 + 1
        self.matrix[center][center] = self.matrix[center+1][center+1] = 'W'
        self.matrix[center+1][center] = self.matrix[center][center+1] = 'B'

        # pieces counter
        self.black_cnt = 2
        self.white_cnt = 2

        # precalculted allowed directions (scan available moves)
        # --- x ---> 
        # (-1,-1) | ( 0,-1) | ( 1, -1) | y
        # (-1, 0) |         | ( 1,  0) |
        # (-1, 1) | ( 0, 1) | ( 1,  1) v

        self.direction = []
        for dx in (-1, 0 , 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                self.direction.append((dx, dy));

        # board limits coords and confinant cells
        # to analize all corners
        self.corner = ((1,2), (self.limit-1, self.limit-2))

    def get_turn(self):
        """get the current player side"""
        return self.turn

    def internal_view(self):
        """get internal status of the board"""

        for yy in range(0,self.size+2):
            line = ""
            for xx in range(0,self.size+2):
                line += self.matrix[yy][xx]

            print(line)

    def get_view(self):
        """get the simplest string rappresentation of board status"""

        out = ""
        out += "\n"
        
        # Compact header
        out += "─" * 40 + "\n"
        out += "  Turn: %-2s   ●:%2d  ○:%2d   Move:%2d\n" % (
            self.turn, self.black_cnt, self.white_cnt, self.turn_cnt
        )
        out += "─" * 40 + "\n"
        out += "\n"

        # Compact column headers
        out += "   "
        for n in range(1, self.limit):
            out += " " + ROWNAME[n]
        out += "\n"

        # Top border
        out += "  ┌" + "─" * (self.size * 2 - 1) + "┐\n"

        # Board rows
        for yy in range(1, self.limit):
            out += str(yy) + " │"
            for xx in range(1, self.limit):
                cell = self.matrix[yy][xx]
                
                if cell == '.':
                    out += '·'
                elif cell == 'W':
                    out += '○'
                elif cell == 'B':
                    out += '●'
                else:
                    raise NameError("cell %s unknow" % cell)
                
                # Add space between cells except at the end
                if xx < self.limit - 1:
                    out += ' '
            
            out += "│ " + str(yy) + "\n"

        # Bottom border
        out += "  └" + "─" * (self.size * 2 - 1) + "┘\n"
        
        # Column headers at bottom
        out += "   "
        for n in range(1, self.limit):
            out += " " + ROWNAME[n]
        out += "\n"
        
        return out

    def view(self):
        """print to stdout the simplest rappresentation of board status"""
        print(self.get_view());

    def export_str(self):
        """export the board status into a string"""

        str_out = ''
        for yy in range(1,self.limit):
            for xx in range(1,self.limit):
                str_out += self.matrix[yy][xx]
        return str_out

    def import_str(self,str_in):
        """import the new board status from a string"""

        if (len(str_in) != self.cells_cnt):
            raise NameError("input length doesn't match the board size")

        # reset piece counter
        self.white_cnt = 0
        self.black_cnt = 0

        # import board position
        for yy in range(0,self.size):
            for xx in range(0,self.size):
                status = str_in[yy * self.size + xx]
                self.matrix[yy+1][xx+1] = status

                # pieces counters
                if status == 'W':
                    self.white_cnt += 1
                elif status == 'B':
                    self.black_cnt += 1
            
    def get_move_list(self):
        """get a list of all current available moves"""
        
        move_list=[]

        # scan all board
        for yy in range(1,self.limit):
            for xx in range(1,self.limit):
                # find valid moves only in blank cells
                if self.matrix[yy][xx] == '.':
                    move = Move(xx,yy)
                    if self.valid_move(move):
                        move_list.append(move)

        return move_list
        
    def check_win(self):
        """boolean check if the player is winner"""

        if (self.white_cnt + self.black_cnt == self.cells_cnt):
            if self.turn == 'W' and self.white_cnt > self.black_cnt:
                return True
            if self.turn == 'B' and self.black_cnt > self.white_cnt:
                return True

        return False

    def check_lost(self):
        """boolean check if the player is winner"""

        if (self.white_cnt + self.black_cnt == self.cells_cnt):
            if self.turn == 'B' and self.white_cnt > self.black_cnt:
                return True
            if self.turn == 'W' and self.black_cnt > self.white_cnt:
                return True

        return False


    def valid_move(self, move):
        """boolean check if the move is allowed"""

        x, y = move.x, move.y

        # check if destination is valid
        if self.matrix[y][x] != '.':
            return False 

        # scanning from destination to source   
        for dd in (self.direction):
            dx, dy = dd

            # scanning available flips
            cnt = 0
            for n in range(1,self.size+1):
                    
                sx = x + n * dx
                sy = y + n * dy

                if self.matrix[sy][sx] == '.':
                    # blank cell
                    cnt = 0
                    break

                elif self.matrix[sy][sx] == self.turn:
                    # self piece (found source)
                    break

                else:
                    # flip opponent piece
                    cnt += 1
            
            # first available move stops search 
            if cnt > 0:
                return True

        return False

    def move(self, move):
        """play a move"""

        x , y = move.x, move.y
        
        # store previus move
        self.board_position_stack.append(self.export_str())
        
        # fix destination
        self.matrix[y][x] = self.turn

        # move is valid if one opponent's piece is flipped
        cnt_tot = 0

        # scan from destination and search allowed moves
        for dd in (self.direction):
            dx, dy = dd

            # scanning available flips
            cnt = 0
            for n in range(1,self.size+1):
                    
                sx = x + n * dx
                sy = y + n * dy

                if self.matrix[sy][sx] == '.':
                    # blank cell
                    cnt = 0
                    break

                elif self.matrix[sy][sx] == self.turn:
                    # self piece (found source)
                    break

                else:
                    # flip opponent piece
                    cnt += 1

            # flip pieces
            if cnt > 0:
                cnt_tot += cnt
                for n in range(1,cnt+1):
                    self.matrix[y + n * dy][x + n * dx] = self.turn

        # validate move
        if cnt_tot == 0:
            raise NameError("This move %s is not valid!" %(move))

        # update pieces counter
        if self.turn == 'W':
            self.white_cnt += 1 + cnt_tot
            self.black_cnt -= cnt_tot
        else:
            self.black_cnt += 1 + cnt_tot
            self.white_cnt -= cnt_tot

        # move counter
        self.turn_cnt += 1
        
        # Update game history for opening book
        # Format: uppercase for black, lowercase for white
        move_str = str(move)
        if self.turn == 'B':
            self.history += move_str.upper()
        else:
            self.history += move_str.lower()

        # switch turn player
        self.switch_player()

    def pass_turn(self):
        # store previus move
        self.board_position_stack.append(self.export_str())
        self.switch_player()
        self.turn_cnt += 1

    def switch_player(self):
        """switch the next move player"""

        if self.turn == 'B':
            self.turn = 'W'
        else:
            self.turn = 'B'

    def undo_move(self):
        """undo previus move"""
        previus_move = self.board_position_stack.pop();
        self.import_str(previus_move)
        self.switch_player()
        self.turn_cnt -= 1
        
        # Remove last move from history (2 characters: letter+digit)
        if len(self.history) >= 2:
            self.history = self.history[:-2]

    def get_current_player(self):
        """get the player of the current move"""
        return self.turn

    def __str__(self):
        """board rappresentations"""
        return self.get_view()

    def evaluate(self):
        """evaluate position"""
    
        # opening and midgame
        # maximize mobility, eval corners
        if self.white_cnt + self.black_cnt < self.cells_cnt * 0.7:

            # eval mobility
            out = len(self.get_move_list())

            # eval corners
            for x in self.corner:
                for y in self.corner:
                    xx, dx = x
                    yy, dy = y
                    # the corner is free
                    if self.matrix[yy][xx] == '.':
                        if self.matrix[yy][dx] != '.':
                            if self.matrix[yy][dx] == self.turn:
                                out -= 3
                            else:
                                out += 3
                        if self.matrix[yy][xx] != '.':                        
                            if self.matrix[dy][xx] == self.turn:
                                out -= 3
                            else:
                                out += 3
                        if self.matrix[dy][dx] != '.':
                            if self.matrix[dy][dx] == self.turn:
                                out -= 7
                            else:
                                out += 7
                    # own the corner
                    elif self.matrix[yy][xx] == self.turn:
                        out += 10
                    else:
                        out -= 10
        else:

            # endgame: maximize the number of pieces
            if self.turn == 'W':
                out = self.white_cnt - self.black_cnt
            else:
                out = self.black_cnt - self.white_cnt

        return out

    def is_finish(self):

        if self.white_cnt + self.black_cnt == self.cells_cnt:
            return True
        else:
            return False

    def get_result(self):
        """get last result on game ended"""

        out = ""
 
        out +="\nblack: %d white: %d\n" %(self.white_cnt, self.black_cnt)

        if self.black_cnt > self.white_cnt:
            out += "the winner is black: +%d" %(self.black_cnt-self.white_cnt)
        elif self.white_cnt > self.black_cnt:
            out += "the winner is white: +%d" %(self.white_cnt-self.black_cnt)
        else:
            out += "the game is drawn!"

        return out

    def result(self):
        """print last result on game ended"""
        print(self.get_result())

if __name__ == "__main__":

    g = Game(8)

    while 1:

        g.view()
        
        print("all available moves:")
        moves = g.get_move_list()

        for move in (moves):
            print(move)

        print("next move")
        x = input("move x : ")
        y = input("move y : ")

        move = Move(x,y)
        g.move(move)
        
        print("your last move %s" % move)

        if g.is_finish():
            break

    # print result
    g.result()
