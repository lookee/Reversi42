#!/usr/bin/env python3
"""
Grandmaster Weights Demo - Custom Playing Styles
=================================================

This demo shows how to create Grandmaster AI players with different
playing styles by customizing evaluation weights.

Examples:
- Default Grandmaster (balanced)
- Aggressive Mobility Punisher (restricts opponent moves)
- Defensive Stability Master (solid, safe play)
- Corner Hunter (obsessed with corners)
- Edge Control Specialist (border domination)
- Endgame Specialist (parity and piece count focus)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Players.AIPlayerGrandmaster import AIPlayerGrandmaster
from AI.GrandmasterWeights import (
    GrandmasterWeights,
    AggressiveMobilityWeights,
    DefensiveStabilityWeights,
    CornerHunterWeights,
    EdgeControlWeights,
    EndgameSpecialistWeights,
    get_preset_weights,
    list_presets
)
from Reversi.Game import Game


def demo_weight_presets():
    """Show all available weight presets"""
    print("\n" + "="*80)
    print("📊 AVAILABLE WEIGHT PRESETS")
    print("="*80)
    
    presets = list_presets()
    
    for preset_name in presets:
        weights = get_preset_weights(preset_name)
        print(f"\n{preset_name.upper().replace('_', ' ')}:")
        print(f"  • Class: {weights.__class__.__name__}")
        print(f"  • Mobility (O/M/E): {weights.mobility_opening}/{weights.mobility_midgame}/{weights.mobility_endgame}")
        print(f"  • Corner weight: {weights.corner_weight}")
        print(f"  • X-square penalty: {weights.x_square_penalty}")
        print(f"  • Stability weight: {weights.stability_weight}")
        print(f"  • Edge weight: {weights.edge_weight}")
    
    print("\n" + "="*80 + "\n")


def demo_custom_weights():
    """Create a completely custom weight configuration"""
    print("\n" + "="*80)
    print("🔧 CREATING CUSTOM WEIGHTS")
    print("="*80)
    
    # Start with default weights
    custom = GrandmasterWeights()
    
    # Modify for specific strategy: "Mobility Destroyer"
    custom.mobility_midgame = 30  # Triple mobility importance
    custom.move_order_mobility_penalty = 30  # Heavily penalize opponent moves
    custom.corner_weight = 100  # Slightly reduce corner obsession
    
    print("\nCustom 'Mobility Destroyer' weights:")
    print(f"  • Mobility midgame: {custom.mobility_midgame} (default: 15)")
    print(f"  • Mobility penalty: {custom.move_order_mobility_penalty} (default: 15)")
    print(f"  • Corner weight: {custom.corner_weight} (default: 150)")
    
    # Create player with custom weights
    player = AIPlayerGrandmaster(deep=5, show_book_options=False, weights=custom)
    
    print(f"\n✅ Created: {player.name} with custom weights")
    print("="*80 + "\n")
    
    return player


def compare_players_single_position():
    """Compare how different weight configurations evaluate the same position"""
    print("\n" + "="*80)
    print("⚖️  COMPARING EVALUATIONS FOR SAME POSITION")
    print("="*80)
    
    # Create a test position (after a few moves)
    game = Game(size=8)
    
    # Convert to bitboard for evaluation
    from Reversi.BitboardGame import BitboardGame
    bitboard = BitboardGame()
    
    # Play some moves
    test_moves = ['F5', 'D6', 'C3', 'D3', 'C4']
    for move_str in test_moves:
        moves = bitboard.get_move_list()
        for move in moves:
            if str(move) == move_str:
                bitboard.move(move)
                break
    
    print(f"\nPosition after moves: {' '.join(test_moves)}")
    print(f"Black: {bitboard.black_cnt}, White: {bitboard.white_cnt}")
    
    # Create different engines
    from AI.GrandmasterEngine import GrandmasterEngine
    
    engines = {
        'Default': GrandmasterEngine(weights=GrandmasterWeights()),
        'Aggressive': GrandmasterEngine(weights=AggressiveMobilityWeights()),
        'Defensive': GrandmasterEngine(weights=DefensiveStabilityWeights()),
        'Corner Hunter': GrandmasterEngine(weights=CornerHunterWeights()),
        'Edge Control': GrandmasterEngine(weights=EdgeControlWeights()),
    }
    
    print("\nEvaluations (from Black's perspective):")
    print("-" * 60)
    
    for name, engine in engines.items():
        eval_score = engine.evaluate_advanced(bitboard)
        print(f"  {name:<20} {eval_score:>6d}")
    
    print("="*80 + "\n")


def demo_match_different_styles():
    """Simulate a match between different playing styles"""
    print("\n" + "="*80)
    print("🥊 DIFFERENT STYLES CAN PLAY AGAINST EACH OTHER")
    print("="*80)
    
    # Create players with different styles
    aggressive = AIPlayerGrandmaster(
        deep=4, 
        show_book_options=False, 
        weights=AggressiveMobilityWeights()
    )
    aggressive.name = "Aggressive"
    
    defensive = AIPlayerGrandmaster(
        deep=4,
        show_book_options=False,
        weights=DefensiveStabilityWeights()
    )
    defensive.name = "Defensive"
    
    print(f"\n✅ Created two players:")
    print(f"   • {aggressive.name} (AggressiveMobilityWeights)")
    print(f"   • {defensive.name} (DefensiveStabilityWeights)")
    print(f"\n💡 These players would evaluate positions differently")
    print(f"   and make different strategic decisions!")
    
    print("\n" + "="*80 + "\n")


def demo_weight_serialization():
    """Show how to save and load custom weights"""
    print("\n" + "="*80)
    print("💾 SAVING AND LOADING CUSTOM WEIGHTS")
    print("="*80)
    
    # Create custom weights
    custom = GrandmasterWeights()
    custom.corner_weight = 200
    custom.mobility_midgame = 25
    custom.x_square_penalty = 100
    
    print("\nOriginal custom weights:")
    print(f"  • Corner: {custom.corner_weight}")
    print(f"  • Mobility midgame: {custom.mobility_midgame}")
    print(f"  • X-square penalty: {custom.x_square_penalty}")
    
    # Serialize to dict
    data = custom.to_dict()
    print(f"\n✅ Serialized to dictionary ({len(data)} parameters)")
    
    # Can save to JSON
    import json
    json_str = json.dumps(data, indent=2)
    print(f"\n📄 JSON format (first 200 chars):")
    print(json_str[:200] + "...")
    
    # Restore from dict
    restored = GrandmasterWeights.from_dict(data)
    print(f"\n✅ Restored from dictionary:")
    print(f"  • Corner: {restored.corner_weight}")
    print(f"  • Mobility midgame: {restored.mobility_midgame}")
    print(f"  • X-square penalty: {restored.x_square_penalty}")
    
    print("\n💡 You can save custom weights to JSON and load them later!")
    print("="*80 + "\n")


def main():
    """Run all demos"""
    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  GRANDMASTER WEIGHTS DEMONSTRATION".center(78) + "█")
    print("█" + "  Create Custom AI Playing Styles".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    # 1. Show all presets
    demo_weight_presets()
    
    # 2. Create custom weights
    custom_player = demo_custom_weights()
    
    # 3. Compare evaluations
    compare_players_single_position()
    
    # 4. Show different styles can compete
    demo_match_different_styles()
    
    # 5. Serialization demo
    demo_weight_serialization()
    
    # Summary
    print("\n" + "="*80)
    print("📝 SUMMARY - HOW TO USE CUSTOM WEIGHTS")
    print("="*80)
    print("""
1. USE PRESET:
   from AI.GrandmasterWeights import get_preset_weights
   weights = get_preset_weights('aggressive')
   player = AIPlayerGrandmaster(deep=9, weights=weights)

2. CREATE CUSTOM:
   from AI.GrandmasterWeights import GrandmasterWeights
   weights = GrandmasterWeights()
   weights.mobility_midgame = 25  # Customize!
   player = AIPlayerGrandmaster(deep=9, weights=weights)

3. USE DEFAULT (original behavior):
   player = AIPlayerGrandmaster(deep=9)  # weights=None uses defaults

4. AVAILABLE PRESETS:
   - 'default' - Standard Grandmaster (balanced)
   - 'aggressive' - Restricts opponent mobility
   - 'defensive' - Prioritizes stability and safety
   - 'corner_hunter' - Obsessed with corners
   - 'edge_control' - Border domination specialist
   - 'endgame_specialist' - Parity and piece count focus

5. ALL CUSTOMIZABLE PARAMETERS:
   • mobility_opening, mobility_midgame, mobility_endgame
   • corner_weight, x_square_penalty, stability_weight
   • frontier_weight, edge_weight
   • parity_favorable, parity_unfavorable, piece_count_weight
   • move_order_corner, move_order_edge, move_order_center
   • move_order_mobility_penalty
""")
    print("="*80 + "\n")
    
    print("✅ Demo complete! You can now create custom Grandmaster players.")
    print("   Try running tournaments between different styles!\n")


if __name__ == '__main__':
    main()

