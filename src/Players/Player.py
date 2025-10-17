class Player(object):
    """
    Base class for all players.
    
    Subclasses can define class-level metadata for automatic menu generation.
    """
    
    # Class-level metadata for menu generation
    PLAYER_METADATA = {
        'display_name': 'Player',
        'description': 'Base player class',
        'enabled': False,  # Not selectable by default
        'parameters': []  # List of configurable parameters
    }

    def __init__(self):
        self.name = 'Player'

    def get_name(self):
        return self.name

    def get_move(self, game, move_list, control):
        return move_list[0]
    
    @classmethod
    def get_metadata(cls):
        """Get player metadata for menu generation"""
        return cls.PLAYER_METADATA
