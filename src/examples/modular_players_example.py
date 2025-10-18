#!/usr/bin/env python3
"""
Example demonstrating the modular player system.
This shows how easy it is to create new player types and engines.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Players.PlayerFactory import PlayerFactory
from Players.NetworkPlayer import NetworkPlayer
from AI.RandomEngine import RandomEngine
from AI.HeuristicEngine import HeuristicEngine

def demonstrate_player_creation():
    """Demonstrate different ways to create players."""
    
    print("=== Modular Player System Demo ===\n")
    
    # 1. Create standard players
    print("1. Creating standard players:")
    human = PlayerFactory.create_player("Human")
    monkey = PlayerFactory.create_player("Monkey")
    print(f"   - Human: {human.get_name()}")
    print(f"   - Monkey: {monkey.get_name()}")
    
    # 2. Create AI players with different engines
    print("\n2. Creating AI players with different engines:")
    
    minimax_ai = PlayerFactory.create_ai_player("Minimax", difficulty=4)
    random_ai = PlayerFactory.create_ai_player("Random", difficulty=1)
    heuristic_ai = PlayerFactory.create_ai_player("Heuristic", difficulty=1)
    
    print(f"   - Minimax AI: {minimax_ai.get_name()}")
    print(f"   - Random AI: {random_ai.get_name()}")
    print(f"   - Heuristic AI: {heuristic_ai.get_name()}")
    
    # 3. Register and use a new player type
    print("\n3. Registering new player type:")
    PlayerFactory.register_player_type("Network", NetworkPlayer)
    
    network_player = PlayerFactory.create_player("Network", name="RemotePlayer")
    print(f"   - Network Player: {network_player.get_name()}")
    
    # 4. Show available types
    print("\n4. Available player types:")
    available = PlayerFactory.list_available_players()
    for player_type in available.keys():
        print(f"   - {player_type}")
    
    print("\n5. Available AI engines:")
    for engine_type in PlayerFactory.get_available_engines():
        print(f"   - {engine_type}")
    
    # 5. Demonstrate engine statistics
    print("\n6. Engine statistics:")
    print(f"   - Minimax engine: {minimax_ai.engine.get_statistics()}")
    print(f"   - Random engine: {random_ai.engine.get_statistics()}")

def demonstrate_custom_engine():
    """Demonstrate creating a custom engine."""
    
    print("\n=== Custom Engine Example ===\n")
    
    # Create a custom engine that combines random and heuristic
    class HybridEngine(RandomEngine):
        def __init__(self):
            super().__init__()
            self.name = "HybridEngine"
            self.heuristic_engine = HeuristicEngine()
        
        def get_best_move(self, game, depth):
            # Use heuristic 70% of the time, random 30%
            import random
            if random.random() < 0.7:
                return self.heuristic_engine.get_best_move(game, depth)
            else:
                return super().get_best_move(game, depth)
    
    # Register the custom engine
    PlayerFactory.register_engine("Hybrid", HybridEngine)
    
    # Create a player with the custom engine
    hybrid_player = PlayerFactory.create_ai_player("Hybrid", difficulty=1)
    print(f"Created hybrid player: {hybrid_player.get_name()}")
    print(f"Engine statistics: {hybrid_player.engine.get_statistics()}")

if __name__ == "__main__":
    demonstrate_player_creation()
    demonstrate_custom_engine()
    
    print("\n=== Demo Complete ===")
    print("The modular system makes it very easy to:")
    print("- Add new player types")
    print("- Add new AI engines")
    print("- Combine different strategies")
    print("- Extend functionality without modifying existing code")
