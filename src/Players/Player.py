class Player(object):

    def __init__(self):
        self.name = 'Player'

    def get_name(self):
        return self.name

    def get_move(self,game,move_list, control):
        return move_list[0]
