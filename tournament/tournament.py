#!/usr/bin/env python3

#------------------------------------------------------------------------
#    Reversi42 Tournament System
#    
#    Advanced tournament simulation with detailed statistical analysis
#    for AI players only (no graphics, high-speed simulation)
#------------------------------------------------------------------------

import sys
import os
# Add parent directory's src to path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(os.path.join(parent_dir, 'src'))

from Reversi.Game import Game, Move
from Players.PlayerFactory import PlayerFactory
import time
from datetime import datetime, timedelta
import statistics
from collections import defaultdict
import json
import argparse

class TournamentGame:
    """Single game statistics"""
    def __init__(self, black_player, white_player):
        self.black_player = black_player
        self.white_player = white_player
        self.moves_count = 0
        self.black_score = 0
        self.white_score = 0
        self.winner = None
        self.duration = 0
        self.move_times = []
        self.game_history = ""
        
class PlayerStats:
    """Statistics for a single player"""
    def __init__(self, name):
        self.name = name
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        
        # As Black
        self.black_games = 0
        self.black_wins = 0
        self.black_losses = 0
        self.black_draws = 0
        self.black_total_score = 0
        
        # As White
        self.white_games = 0
        self.white_wins = 0
        self.white_losses = 0
        self.white_draws = 0
        self.white_total_score = 0
        
        # Performance metrics
        self.total_score = 0
        self.move_times = []
        self.total_moves = 0
        
    def add_game(self, as_black, won, score, opponent_score, move_times):
        """Add game results"""
        self.games_played += 1
        self.total_score += score
        self.move_times.extend(move_times)
        self.total_moves += len(move_times)
        
        if as_black:
            self.black_games += 1
            self.black_total_score += score
            if won:
                self.black_wins += 1
                self.wins += 1
            elif score == opponent_score:
                self.black_draws += 1
                self.draws += 1
            else:
                self.black_losses += 1
                self.losses += 1
        else:
            self.white_games += 1
            self.white_total_score += score
            if won:
                self.white_wins += 1
                self.wins += 1
            elif score == opponent_score:
                self.white_draws += 1
                self.draws += 1
            else:
                self.white_losses += 1
                self.losses += 1

class Tournament:
    """Tournament manager and statistics"""
    
    def __init__(self, players_config, games_per_matchup, include_move_history=False, 
                 name="Reversi42 Tournament", description=""):
        """
        Initialize tournament
        
        Args:
            players_config: List of tuples (type, name, difficulty, engine, evaluator)
            games_per_matchup: Number of games per matchup (each color)
            include_move_history: If True, include full move history in report
            name: Tournament name
            description: Tournament description
        """
        self.name = name
        self.description = description
        self.players_config = players_config
        self.games_per_matchup = games_per_matchup
        self.include_move_history = include_move_history
        self.games = []
        self.player_stats = {}
        self.start_time = None
        self.end_time = None
    
    @classmethod
    def from_config_file(cls, config_path):
        """
        Create tournament from JSON configuration file
        
        Args:
            config_path: Path to JSON configuration file
            
        Returns:
            Tournament instance
        """
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Parse players configuration
        players_config = []
        for player in config['players']:
            player_tuple = (
                player['type'],
                player['name'],
                player.get('difficulty', 1),
                player.get('engine', 'Minimax'),
                player.get('evaluator', 'Standard')
            )
            players_config.append(player_tuple)
        
        # Create tournament instance
        return cls(
            players_config=players_config,
            games_per_matchup=config.get('games_per_matchup', 1),
            include_move_history=config.get('include_move_history', False),
            name=config.get('name', 'Reversi42 Tournament'),
            description=config.get('description', '')
        )
    
    def to_config_dict(self):
        """
        Convert tournament configuration to dictionary
        
        Returns:
            Dictionary with tournament configuration
        """
        players = []
        for player_tuple in self.players_config:
            player_dict = {
                'type': player_tuple[0],
                'name': player_tuple[1],
                'difficulty': player_tuple[2],
                'engine': player_tuple[3],
                'evaluator': player_tuple[4]
            }
            players.append(player_dict)
        
        return {
            'name': self.name,
            'description': self.description,
            'players': players,
            'games_per_matchup': self.games_per_matchup,
            'include_move_history': self.include_move_history
        }
    
    def save_config(self, filepath):
        """
        Save tournament configuration to JSON file
        
        Args:
            filepath: Path where to save configuration
        """
        config = self.to_config_dict()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to: {filepath}")
        return filepath
        
    def create_player(self, config):
        """Create a player from configuration"""
        player_type, name, difficulty, engine_type, evaluator_type = config
        
        if player_type == "AI":
            player = PlayerFactory.create_ai_player(
                engine_type=engine_type,
                difficulty=difficulty,
                evaluator_type=evaluator_type
            )
            player.name = name
        elif player_type == "AIBook":
            # Create AIPlayerBook with specified difficulty
            from Players.AIPlayerBook import AIPlayerBook
            player = AIPlayerBook(deep=difficulty)
            player.name = name
        elif player_type == "Bitboard":
            # Create AIPlayerBitboard (ultra-fast)
            from Players.AIPlayerBitboard import AIPlayerBitboard
            player = AIPlayerBitboard(deep=difficulty)
            player.name = name
        elif player_type == "BitboardBook":
            # Create AIPlayerBitboardBook (The Oracle)
            from Players.AIPlayerBitboardBook import AIPlayerBitboardBook
            player = AIPlayerBitboardBook(deep=difficulty, show_book_options=False)
            player.name = name
        elif player_type == "ParallelOracle":
            # Create AIPlayerBitboardBookParallel (Parallel Oracle)
            from Players.AIPlayerBitboardBookParallel import AIPlayerBitboardBookParallel
            player = AIPlayerBitboardBookParallel(deep=difficulty, show_book_options=False)
            player.name = name
        elif player_type == "Grandmaster":
            # Create AIPlayerGrandmaster (Ultimate AI)
            from Players.AIPlayerGrandmaster import AIPlayerGrandmaster
            player = AIPlayerGrandmaster(deep=difficulty, show_book_options=False)
            player.name = name
        else:
            player = PlayerFactory.create_player(player_type)
            player.name = name
        
        # Initialize stats
        if name not in self.player_stats:
            self.player_stats[name] = PlayerStats(name)
        
        return player
    
    def play_game(self, black_config, white_config, game_number, total_games):
        """Play a single game and collect statistics"""
        
        # Create players
        black_player = self.create_player(black_config)
        white_player = self.create_player(white_config)
        
        # Create game
        g = Game(8)
        game_stat = TournamentGame(black_player.name, white_player.name)
        
        # Track progress
        print(f"  Game {game_number}/{total_games}: {black_player.name} (B) vs {white_player.name} (W)... ", end='', flush=True)
        
        game_start = time.perf_counter()
        move_times_by_player = {black_player.name: [], white_player.name: []}
        
        # Game loop
        while not g.is_finish():
            turn = g.get_turn()
            player = black_player if turn == 'B' else white_player
            
            moves = g.get_move_list()
            
            if len(moves) > 0:
                # Get move with timing
                move_start = time.perf_counter()
                move = player.get_move(g, moves, None)
                move_time = time.perf_counter() - move_start
                
                if move is None:
                    break
                
                # Record move time
                move_times_by_player[player.name].append(move_time)
                game_stat.move_times.append(move_time)
                
                # Make move
                g.move(move)
                game_stat.moves_count += 1
                
                # Update history
                if turn == 'B':
                    game_stat.game_history += str(move).upper()
                else:
                    game_stat.game_history += str(move).lower()
            else:
                g.pass_turn()
                next_moves = g.get_move_list()
                if len(next_moves) == 0:
                    break
        
        game_stat.duration = time.perf_counter() - game_start
        
        # Get final scores
        game_stat.black_score = g.black_cnt
        game_stat.white_score = g.white_cnt
        
        # Determine winner
        if g.black_cnt > g.white_cnt:
            game_stat.winner = black_player.name
            print(f"Winner: {black_player.name} ({g.black_cnt}-{g.white_cnt})")
        elif g.white_cnt > g.black_cnt:
            game_stat.winner = white_player.name
            print(f"Winner: {white_player.name} ({g.white_cnt}-{g.black_cnt})")
        else:
            game_stat.winner = "Draw"
            print(f"Draw ({g.black_cnt}-{g.white_cnt})")
        
        # Update player stats
        self.player_stats[black_player.name].add_game(
            as_black=True,
            won=(game_stat.winner == black_player.name),
            score=game_stat.black_score,
            opponent_score=game_stat.white_score,
            move_times=move_times_by_player[black_player.name]
        )
        
        self.player_stats[white_player.name].add_game(
            as_black=False,
            won=(game_stat.winner == white_player.name),
            score=game_stat.white_score,
            opponent_score=game_stat.black_score,
            move_times=move_times_by_player[white_player.name]
        )
        
        self.games.append(game_stat)
        
        return game_stat
    
    def run(self):
        """Run the tournament"""
        self.start_time = datetime.now()
        print("\n" + "="*80)
        print(f"{self.name.upper()}")
        print("="*80)
        if self.description:
            print(f"Description: {self.description}")
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Players: {len(self.players_config)}")
        print(f"Games per matchup: {self.games_per_matchup}")
        
        # Calculate total games
        n_players = len(self.players_config)
        matchups = n_players * (n_players - 1)  # Each pair, both colors
        total_games = matchups * self.games_per_matchup
        
        print(f"Total games: {total_games}")
        print()
        
        game_number = 0
        
        # Play all matchups
        for i, black_config in enumerate(self.players_config):
            for j, white_config in enumerate(self.players_config):
                if i == j:
                    continue  # Don't play against self
                
                print(f"\nMatchup: {black_config[1]} vs {white_config[1]}")
                
                # Play multiple games
                for game_num in range(self.games_per_matchup):
                    game_number += 1
                    self.play_game(black_config, white_config, game_number, total_games)
        
        self.end_time = datetime.now()
        print("\n" + "="*80)
        print("TOURNAMENT COMPLETED")
        print("="*80)
        print(f"End time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {self.end_time - self.start_time}")
        print()
    
    def generate_report(self):
        """Generate comprehensive statistical report"""
        
        report = []
        report.append("\n" + "="*80)
        report.append("REVERSI42 TOURNAMENT - COMPREHENSIVE STATISTICAL REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Tournament Duration: {self.end_time - self.start_time}")
        report.append("")
        
        # Tournament Overview
        report.append("─" * 80)
        report.append("1. TOURNAMENT OVERVIEW")
        report.append("─" * 80)
        report.append(f"Total Players: {len(self.players_config)}")
        report.append(f"Total Games Played: {len(self.games)}")
        report.append(f"Games per Matchup: {self.games_per_matchup}")
        report.append(f"Average Game Duration: {statistics.mean([g.duration for g in self.games]):.3f}s")
        report.append(f"Total Tournament Time: {sum(g.duration for g in self.games):.2f}s")
        report.append(f"Average Moves per Game: {statistics.mean([g.moves_count for g in self.games]):.1f}")
        report.append("")
        
        # Overall Rankings
        report.append("─" * 80)
        report.append("2. OVERALL RANKINGS")
        report.append("─" * 80)
        
        # Sort by win rate
        sorted_players = sorted(
            self.player_stats.values(),
            key=lambda p: (p.wins / p.games_played if p.games_played > 0 else 0),
            reverse=True
        )
        
        report.append(f"{'Rank':<6}{'Player':<25}{'W':>5} {'L':>5} {'D':>5} {'Win%':>7} {'Avg Score':>10}")
        report.append("─" * 80)
        
        for rank, player in enumerate(sorted_players, 1):
            win_rate = (player.wins / player.games_played * 100) if player.games_played > 0 else 0
            avg_score = player.total_score / player.games_played if player.games_played > 0 else 0
            report.append(f"{rank:<6}{player.name:<25}{player.wins:>5} {player.losses:>5} {player.draws:>5} {win_rate:>6.1f}% {avg_score:>10.2f}")
        
        report.append("")
        
        # Detailed Player Statistics
        report.append("─" * 80)
        report.append("3. DETAILED PLAYER ANALYSIS")
        report.append("─" * 80)
        report.append("")
        
        for player in sorted_players:
            report.append("+" + "=" * 78 + "+")
            report.append(f"| PLAYER: {player.name:<69}|")
            report.append("+" + "=" * 78 + "+")
            report.append("")
            
            # Overall Performance
            report.append("  OVERALL PERFORMANCE:")
            report.append(f"    Games Played: {player.games_played}")
            report.append(f"    Wins: {player.wins} ({player.wins/player.games_played*100:.1f}%)")
            report.append(f"    Losses: {player.losses} ({player.losses/player.games_played*100:.1f}%)")
            report.append(f"    Draws: {player.draws} ({player.draws/player.games_played*100:.1f}%)")
            report.append(f"    Average Score: {player.total_score/player.games_played:.2f}")
            report.append("")
            
            # Performance as Black
            report.append("  PERFORMANCE AS BLACK:")
            if player.black_games > 0:
                report.append(f"    Games: {player.black_games}")
                report.append(f"    Wins: {player.black_wins} ({player.black_wins/player.black_games*100:.1f}%)")
                report.append(f"    Losses: {player.black_losses} ({player.black_losses/player.black_games*100:.1f}%)")
                report.append(f"    Draws: {player.black_draws} ({player.black_draws/player.black_games*100:.1f}%)")
                report.append(f"    Average Score: {player.black_total_score/player.black_games:.2f}")
            else:
                report.append("    No games played as Black")
            report.append("")
            
            # Performance as White
            report.append("  PERFORMANCE AS WHITE:")
            if player.white_games > 0:
                report.append(f"    Games: {player.white_games}")
                report.append(f"    Wins: {player.white_wins} ({player.white_wins/player.white_games*100:.1f}%)")
                report.append(f"    Losses: {player.white_losses} ({player.white_losses/player.white_games*100:.1f}%)")
                report.append(f"    Draws: {player.white_draws} ({player.white_draws/player.white_games*100:.1f}%)")
                report.append(f"    Average Score: {player.white_total_score/player.white_games:.2f}")
            else:
                report.append("    No games played as White")
            report.append("")
            
            # Timing Analysis
            report.append("  TIMING ANALYSIS:")
            if player.move_times:
                report.append(f"    Total Moves: {player.total_moves}")
                report.append(f"    Average Move Time: {statistics.mean(player.move_times)*1000:.2f}ms")
                report.append(f"    Median Move Time: {statistics.median(player.move_times)*1000:.2f}ms")
                report.append(f"    Fastest Move: {min(player.move_times)*1000:.2f}ms")
                report.append(f"    Slowest Move: {max(player.move_times)*1000:.2f}ms")
                report.append(f"    Std Dev: {statistics.stdev(player.move_times)*1000:.2f}ms")
                report.append(f"    Total Thinking Time: {sum(player.move_times):.2f}s")
            report.append("")
            
            # Color Advantage Analysis
            if player.black_games > 0 and player.white_games > 0:
                black_wr = player.black_wins / player.black_games * 100
                white_wr = player.white_wins / player.white_games * 100
                color_diff = black_wr - white_wr
                
                report.append("  COLOR ADVANTAGE ANALYSIS:")
                report.append(f"    Black Win Rate: {black_wr:.1f}%")
                report.append(f"    White Win Rate: {white_wr:.1f}%")
                if abs(color_diff) < 5:
                    report.append(f"    Analysis: Balanced performance (±{abs(color_diff):.1f}%)")
                elif color_diff > 0:
                    report.append(f"    Analysis: Stronger as Black (+{color_diff:.1f}%)")
                else:
                    report.append(f"    Analysis: Stronger as White (+{abs(color_diff):.1f}%)")
            report.append("")
        
        # Head-to-Head Analysis
        report.append("─" * 80)
        report.append("4. HEAD-TO-HEAD MATCHUP MATRIX")
        report.append("─" * 80)
        report.append("")
        
        # Build H2H matrix
        h2h = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0}))
        
        for game in self.games:
            if game.winner == game.black_player:
                h2h[game.black_player][game.white_player]['wins'] += 1
                h2h[game.white_player][game.black_player]['losses'] += 1
            elif game.winner == game.white_player:
                h2h[game.white_player][game.black_player]['wins'] += 1
                h2h[game.black_player][game.white_player]['losses'] += 1
            else:
                h2h[game.black_player][game.white_player]['draws'] += 1
                h2h[game.white_player][game.black_player]['draws'] += 1
        
        # Print matrix
        player_names = [p.name for p in sorted_players]
        
        # Header
        header = f"{'Player':<20}"
        for name in player_names:
            header += f" {name[:8]:>8}"
        report.append(header)
        report.append("─" * (20 + 9 * len(player_names)))
        
        # Rows
        for p1_name in player_names:
            row = f"{p1_name:<20}"
            for p2_name in player_names:
                if p1_name == p2_name:
                    row += f" {'─':>8}"
                else:
                    stats = h2h[p1_name][p2_name]
                    score_str = f"{stats['wins']}-{stats['losses']}-{stats['draws']}"
                    row += f" {score_str:>8}"
            report.append(row)
        
        report.append("")
        report.append("  Note: Format is W-L-D (Wins-Losses-Draws)")
        report.append("")
        
        # Game Duration Analysis
        report.append("─" * 80)
        report.append("5. GAME DURATION ANALYSIS")
        report.append("─" * 80)
        
        durations = [g.duration for g in self.games]
        report.append(f"  Average Game Duration: {statistics.mean(durations):.3f}s")
        report.append(f"  Median Game Duration: {statistics.median(durations):.3f}s")
        report.append(f"  Fastest Game: {min(durations):.3f}s")
        report.append(f"  Slowest Game: {max(durations):.3f}s")
        report.append(f"  Std Dev: {statistics.stdev(durations):.3f}s")
        report.append(f"  Total Playing Time: {sum(durations):.2f}s ({sum(durations)/60:.2f} minutes)")
        report.append("")
        
        # Move Count Analysis
        report.append("─" * 80)
        report.append("6. MOVE COUNT ANALYSIS")
        report.append("─" * 80)
        
        move_counts = [g.moves_count for g in self.games]
        report.append(f"  Average Moves per Game: {statistics.mean(move_counts):.1f}")
        report.append(f"  Median Moves per Game: {statistics.median(move_counts):.0f}")
        report.append(f"  Minimum Moves: {min(move_counts)}")
        report.append(f"  Maximum Moves: {max(move_counts)}")
        report.append(f"  Total Moves Played: {sum(move_counts)}")
        report.append("")
        
        # Expert Analysis & Recommendations
        report.append("─" * 80)
        report.append("7. EXPERT ANALYSIS & RECOMMENDATIONS")
        report.append("─" * 80)
        report.append("")
        
        # Determine strongest player
        strongest = sorted_players[0]
        report.append(f"  ★ TOURNAMENT CHAMPION: {strongest.name}")
        report.append(f"    Win Rate: {strongest.wins/strongest.games_played*100:.1f}%")
        report.append(f"    Avg Score: {strongest.total_score/strongest.games_played:.2f}")
        report.append("")
        
        # Color analysis across all games
        black_wins = sum(1 for g in self.games if g.winner == g.black_player)
        white_wins = sum(1 for g in self.games if g.winner == g.white_player)
        draws = sum(1 for g in self.games if g.winner == "Draw")
        
        report.append("  COLOR ADVANTAGE IN TOURNAMENT:")
        report.append(f"    Black Wins: {black_wins} ({black_wins/len(self.games)*100:.1f}%)")
        report.append(f"    White Wins: {white_wins} ({white_wins/len(self.games)*100:.1f}%)")
        report.append(f"    Draws: {draws} ({draws/len(self.games)*100:.1f}%)")
        
        if black_wins > white_wins * 1.1:
            report.append("    Analysis: Significant Black advantage in this tournament")
        elif white_wins > black_wins * 1.1:
            report.append("    Analysis: Significant White advantage in this tournament")
        else:
            report.append("    Analysis: Well-balanced color distribution")
        report.append("")
        
        # Performance insights
        report.append("  KEY INSIGHTS:")
        
        # Most consistent player
        consistency_scores = []
        for player in sorted_players:
            if player.games_played > 2:
                win_rate = player.wins / player.games_played
                consistency = 1.0 - abs(0.5 - win_rate)  # Distance from 50%
                consistency_scores.append((player.name, consistency, win_rate))
        
        if consistency_scores:
            most_consistent = max(consistency_scores, key=lambda x: x[2] if x[2] > 0.5 else 0)
            report.append(f"    • Most Dominant: {most_consistent[0]} (win rate: {most_consistent[2]*100:.1f}%)")
        
        # Fastest thinker
        fastest_player = min(sorted_players, key=lambda p: statistics.mean(p.move_times) if p.move_times else float('inf'))
        report.append(f"    • Fastest Thinker: {fastest_player.name} (avg: {statistics.mean(fastest_player.move_times)*1000:.2f}ms/move)")
        
        # Most aggressive (highest avg score)
        most_aggressive = max(sorted_players, key=lambda p: p.total_score/p.games_played if p.games_played > 0 else 0)
        report.append(f"    • Most Aggressive: {most_aggressive.name} (avg score: {most_aggressive.total_score/most_aggressive.games_played:.2f})")
        
        report.append("")
        
        # Optional: Move History Section
        if self.include_move_history:
            report.append("─" * 80)
            report.append("8. COMPLETE MOVE HISTORY")
            report.append("─" * 80)
            report.append("")
            report.append("  Full game notation for all tournament games:")
            report.append("  (Uppercase = Black moves, Lowercase = White moves)")
            report.append("")
            
            for i, game in enumerate(self.games, 1):
                report.append(f"  Game {i}: {game.black_player} (B) vs {game.white_player} (W)")
                report.append(f"    Winner: {game.winner}")
                report.append(f"    Score: {game.black_score}-{game.white_score}")
                report.append(f"    Moves ({game.moves_count}): {game.game_history}")
                report.append(f"    Duration: {game.duration:.3f}s")
                report.append("")
            
            report.append(f"  Total games recorded: {len(self.games)}")
            report.append("")
        
        report.append("─" * 80)
        report.append("END OF REPORT")
        report.append("─" * 80)
        report.append("")
        
        return "\n".join(report)
    
    def save_report(self, filename=None):
        """Save report to file in reports/ directory"""
        # Get script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(script_dir, 'reports')
        
        # Ensure reports directory exists
        os.makedirs(reports_dir, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tournament_report_{timestamp}.txt"
        
        # Full path in reports directory
        filepath = os.path.join(reports_dir, filename)
        
        report = self.generate_report()
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        print(f"\nReport saved to: {filepath}")
        return filepath


def main():
    """Main tournament setup using player metadata or config file"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Reversi42 Tournament System')
    parser.add_argument('--config', '-c', type=str, 
                       help='Path to tournament configuration file (JSON)')
    parser.add_argument('--save-config', type=str,
                       help='Save current configuration to specified file')
    args = parser.parse_args()
    
    # If config file provided, load and run tournament
    if args.config:
        print("\n" + "="*80)
        print("REVERSI42 TOURNAMENT SYSTEM - LOADING FROM CONFIG")
        print("="*80)
        print(f"Configuration file: {args.config}")
        print()
        
        try:
            tournament = Tournament.from_config_file(args.config)
            
            print(f"Tournament: {tournament.name}")
            if tournament.description:
                print(f"Description: {tournament.description}")
            print(f"Players: {len(tournament.players_config)}")
            print(f"Games per matchup: {tournament.games_per_matchup}")
            print()
            
            print("Configured players:")
            for config in tournament.players_config:
                print(f"  - {config[1]}")
            print()
            
            input("Press ENTER to start tournament...")
            
            # Run tournament
            tournament.run()
            
            # Generate and display report
            report = tournament.generate_report()
            print(report)
            
            # Save report
            filename = tournament.save_report()
            
            print("\nTournament completed successfully!")
            print(f"Detailed report saved to: {filename}")
            if tournament.include_move_history:
                print("Note: Report includes complete move history for all games")
            
            return
            
        except FileNotFoundError:
            print(f"ERROR: Configuration file not found: {args.config}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in configuration file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Failed to load configuration: {e}")
            sys.exit(1)
    
    # Otherwise, interactive configuration
    print("\n" + "="*80)
    print("REVERSI42 TOURNAMENT SYSTEM")
    print("="*80)
    print()
    
    # Get available players from metadata (excluding Human)
    all_metadata = PlayerFactory.get_all_player_metadata()
    
    # Filter to only AI players (no Human)
    ai_players_meta = {
        name: meta for name, meta in all_metadata.items()
        if meta['enabled'] and name != 'Human'
    }
    
    # For AI players with evaluators, create variants
    tournament_options = []
    option_configs = []
    
    # Add Minimax variants
    for evaluator in ['Standard', 'Advanced', 'Greedy']:
        tournament_options.append(f"Minimax ({evaluator} evaluator)")
        option_configs.append(('AI_variant', evaluator))
    
    # Add other players from metadata
    for name, meta in ai_players_meta.items():
        if name != 'AI':  # AI is handled above with variants
            tournament_options.append(f"{name}: {meta['description']}")
            option_configs.append((name, None))
    
    # Get tournament configuration
    print("Configure your tournament:")
    print()
    
    # Display available players
    print("Available AI types:")
    for i, option in enumerate(tournament_options, 1):
        print(f"  {i}. {option}")
    print()
    
    # Get number of participants
    while True:
        try:
            n_players = int(input("Number of AI players (2-10): "))
            if 2 <= n_players <= 10:
                break
            print("Please enter a number between 2 and 10")
        except ValueError:
            print("Please enter a valid number")
    
    # Configure each player
    players_config = []
    
    print("\nConfigure each player:")
    for i in range(n_players):
        print(f"\nPlayer {i+1}:")
        
        while True:
            try:
                ai_type = int(input(f"  AI type (1-{len(tournament_options)}): "))
                if 1 <= ai_type <= len(tournament_options):
                    break
                print(f"  Please enter a number between 1 and {len(tournament_options)}")
            except ValueError:
                print("  Please enter a valid number")
        
        player_type, extra = option_configs[ai_type - 1]
        
        if player_type == 'AI_variant':
            # Minimax with specific evaluator
            evaluator = extra
            while True:
                try:
                    difficulty = int(input("  Difficulty level (1-10): "))
                    if 1 <= difficulty <= 10:
                        break
                    print("  Please enter a number between 1 and 10")
                except ValueError:
                    print("  Please enter a valid number")
            
            name = f"Minimax-{evaluator}-{difficulty}"
            player_config = ("AI", name, difficulty, "Minimax", evaluator)
        
        elif player_type == 'AI with Opening Book':
            # AIPlayerBook with difficulty
            while True:
                try:
                    difficulty = int(input("  Difficulty level (1-10): "))
                    if 1 <= difficulty <= 10:
                        break
                    print("  Please enter a number between 1 and 10")
                except ValueError:
                    print("  Please enter a valid number")
            
            name = f"AIPlayerBook-{difficulty}"
            player_config = ("AIBook", name, difficulty, "Minimax", "Standard")
        
        else:
            # Other player types (Heuristic, Greedy, Monkey)
            name = f"{player_type.replace(' ', '')}"
            player_config = (player_type, name, 1, player_type, "Standard")
        
        players_config.append(player_config)
        print(f"  Added: {name}")
    
    # Get games per matchup
    print()
    while True:
        try:
            games_per_matchup = int(input("Games per matchup (1-20): "))
            if 1 <= games_per_matchup <= 20:
                break
            print("Please enter a number between 1 and 20")
        except ValueError:
            print("Please enter a valid number")
    
    # Ask about move history
    print()
    while True:
        include_history = input("Include complete move history in report? (y/n): ").strip().lower()
        if include_history in ['y', 'n', 'yes', 'no']:
            include_move_history = include_history in ['y', 'yes']
            break
        print("Please enter 'y' or 'n'")
    
    # Calculate total games
    n = len(players_config)
    total_games = n * (n - 1) * games_per_matchup
    
    print()
    print("Tournament Configuration:")
    print(f"  Players: {n}")
    print(f"  Matchups: {n * (n - 1)}")
    print(f"  Games per matchup: {games_per_matchup}")
    print(f"  Total games: {total_games}")
    print(f"  Include move history: {'Yes' if include_move_history else 'No'}")
    print()
    
    input("Press ENTER to start tournament...")
    
    # Get tournament name and description
    print()
    tournament_name = input("Tournament name (press ENTER for default): ").strip()
    if not tournament_name:
        tournament_name = "Reversi42 Tournament"
    
    tournament_desc = input("Tournament description (optional): ").strip()
    
    # Run tournament
    tournament = Tournament(players_config, games_per_matchup, include_move_history,
                          name=tournament_name, description=tournament_desc)
    
    # Optionally save configuration
    if args.save_config:
        tournament.save_config(args.save_config)
    
    tournament.run()
    
    # Generate and display report
    report = tournament.generate_report()
    print(report)
    
    # Save report
    filename = tournament.save_report()
    
    print("\nTournament completed successfully!")
    print(f"Detailed report saved to: {filename}")
    if include_move_history:
        print("Note: Report includes complete move history for all games")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTournament interrupted by user.")
        sys.exit(0)

