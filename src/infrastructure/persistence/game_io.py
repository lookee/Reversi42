#!/usr/bin/env python3

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
Game I/O module for saving and loading games in XOT format.

XOT (eXtended Othello Transcript) Format:
- Simple text format
- Contains board state and move history
- Compatible with Reversi analysis tools
"""

from datetime import datetime
import os

class GameIO:
    """Handle game save/load operations in XOT format"""
    
    XOT_VERSION = "1.0"
    
    @staticmethod
    def get_saves_directory():
        """Get the saves directory path (creates if doesn't exist)"""
        # Get project root directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)  # Go up from src/
        saves_dir = os.path.join(project_root, 'saves')
        
        # Create if doesn't exist
        os.makedirs(saves_dir, exist_ok=True)
        
        return os.path.abspath(saves_dir)  # Normalize path
    
    @staticmethod
    def save_game(game, filename, black_player_name, white_player_name, move_history):
        """
        Save game to XOT format file.
        
        Args:
            game: Game instance
            filename: Path to save file
            black_player_name: Name of Black player
            white_player_name: Name of White player
            move_history: String of moves (e.g., "D3e3F4...")
            
        Returns:
            str: Path to saved file
        """
        
        # Get saves directory (creates if needed)
        saves_dir = GameIO.get_saves_directory()
        
        # Full path
        if not filename.endswith('.xot'):
            filename += '.xot'
        filepath = os.path.join(saves_dir, filename)
        
        # Generate XOT content
        content = []
        content.append(f"# Reversi42 Game Save - XOT Format v{GameIO.XOT_VERSION}")
        content.append(f"# Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        
        # Game metadata
        content.append("[GAME]")
        content.append(f"Black={black_player_name}")
        content.append(f"White={white_player_name}")
        content.append(f"Turn={game.turn}")
        content.append(f"BlackScore={game.black_cnt}")
        content.append(f"WhiteScore={game.white_cnt}")
        content.append(f"Size={game.size if hasattr(game, 'size') else 8}")
        content.append("")
        
        # Move history
        content.append("[MOVES]")
        content.append(f"History={move_history}")
        content.append(f"Count={len(move_history)//2}")  # Each move is 2 chars
        content.append("")
        
        # Board state (optional, for verification)
        content.append("[BOARD]")
        board_str = game.export_str()
        # Split into rows
        for i in range(game.size):
            row = board_str[i*game.size:(i+1)*game.size]
            content.append(row)
        content.append("")
        
        # Write file
        with open(filepath, 'w') as f:
            f.write('\n'.join(content))
        
        return filepath
    
    @staticmethod
    def load_game(filepath):
        """
        Load game from XOT format file.
        
        Args:
            filepath: Path to XOT file (can be absolute or just filename)
            
        Returns:
            dict: Game data with keys: move_history, turn, black_score, white_score, size
        """
        
        # If filepath is just a filename, prepend saves directory
        if not os.path.isabs(filepath):
            saves_dir = GameIO.get_saves_directory()
            filepath = os.path.join(saves_dir, filepath)
        
        # Normalize path
        filepath = os.path.abspath(filepath)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")
        
        game_data = {
            'black_player': 'Black',
            'white_player': 'White',
            'turn': 'B',
            'black_score': 2,
            'white_score': 2,
            'size': 8,
            'move_history': '',
            'board_state': None
        }
        
        current_section = None
        board_lines = []
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Section headers
                if line.startswith('['):
                    current_section = line[1:-1]
                    continue
                
                # Parse based on section
                if current_section == 'GAME':
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key == 'Black':
                            game_data['black_player'] = value
                        elif key == 'White':
                            game_data['white_player'] = value
                        elif key == 'Turn':
                            game_data['turn'] = value
                        elif key == 'BlackScore':
                            game_data['black_score'] = int(value)
                        elif key == 'WhiteScore':
                            game_data['white_score'] = int(value)
                        elif key == 'Size':
                            game_data['size'] = int(value)
                
                elif current_section == 'MOVES':
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key == 'History':
                            game_data['move_history'] = value
                
                elif current_section == 'BOARD':
                    # Board state lines
                    if line and not line.startswith('['):
                        board_lines.append(line)
        
        if board_lines:
            game_data['board_state'] = ''.join(board_lines)
        
        return game_data
    
    @staticmethod
    def list_saved_games(directory=None):
        """
        List all saved games.
        
        Args:
            directory: Directory to search (default: saves/)
            
        Returns:
            list: List of .xot filenames (sorted by modification time, newest first)
        """
        if directory is None:
            directory = GameIO.get_saves_directory()
        
        if not os.path.exists(directory):
            return []
        
        # Get all .xot files with their modification times
        xot_files = [f for f in os.listdir(directory) if f.endswith('.xot')]
        
        # Sort by modification time (newest first)
        xot_files_with_time = []
        for f in xot_files:
            filepath = os.path.join(directory, f)
            mtime = os.path.getmtime(filepath)
            xot_files_with_time.append((f, mtime))
        
        # Sort by time (newest first)
        xot_files_with_time.sort(key=lambda x: x[1], reverse=True)
        
        return [f for f, _ in xot_files_with_time]

