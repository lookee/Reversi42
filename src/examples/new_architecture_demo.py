"""
New Architecture Demo

Demonstrates the new modular Players/AI architecture with:
- Dependency Injection
- Builder Pattern
- Decorator Pattern
- Registry Pattern

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from AI.factory.engine_builder import EngineBuilder
from AI.factory.engine_registry import EngineRegistry
from Players.ai.ai_player import AIPlayer
from Players.factory.player_presets import PlayerPresets
from Players.factory.player_factory_v2 import PlayerFactoryV2


def demo_basic_usage():
    """Demo 1: Basic usage with Builder Pattern"""
    print("\n" + "="*80)
    print("DEMO 1: Basic Builder Pattern")
    print("="*80)
    
    # Create simple AI with fluent API
    engine = (EngineBuilder()
        .use_minimax()
        .with_standard_evaluator()
        .build())
    
    player = AIPlayer(engine=engine, depth=6, name="SimpleAI")
    
    print(f"Created: {player}")
    print(f"Engine: {player.get_engine().get_name()}")


def demo_advanced_configuration():
    """Demo 2: Advanced configuration with Decorators"""
    print("\n" + "="*80)
    print("DEMO 2: Builder + Decorators (Grandmaster Configuration)")
    print("="*80)
    
    # Create grandmaster-level AI
    engine = (EngineBuilder()
        .use_grandmaster()
        .with_advanced_evaluator()
        .with_opening_book()
        .with_transposition_table(size_mb=256)
        .with_endgame_solver(depth_trigger=14)
        .build())
    
    player = AIPlayer(engine=engine, depth=9, name="UltimateGrandmaster")
    
    print(f"Created: {player}")
    print(f"Engine: {player.get_engine().get_name()}")
    print(f"\nFeatures:")
    print("  ✓ Grandmaster base engine")
    print("  ✓ Advanced evaluator")
    print("  ✓ Opening book")
    print("  ✓ Transposition table (256 MB)")
    print("  ✓ Perfect endgame solver")


def demo_presets():
    """Demo 3: Quick creation with Presets"""
    print("\n" + "="*80)
    print("DEMO 3: PlayerPresets (Quick Creation)")
    print("="*80)
    
    # Create pre-configured players
    beginner = PlayerPresets.create_beginner(depth=3)
    intermediate = PlayerPresets.create_intermediate(depth=6)
    grandmaster = PlayerPresets.create_grandmaster(depth=9)
    
    print(f"Beginner: {beginner.get_name()}")
    print(f"Intermediate: {intermediate.get_name()}")
    print(f"Grandmaster: {grandmaster.get_name()}")


def demo_backward_compatibility():
    """Demo 4: Backward compatibility"""
    print("\n" + "="*80)
    print("DEMO 4: Backward Compatibility (PlayerFactoryV2)")
    print("="*80)
    
    # Old API still works!
    player1 = PlayerFactoryV2.create_player('Alpha-Beta AI', deep=6)
    player2 = PlayerFactoryV2.create_player('Grandmaster', deep=9)
    
    print(f"Legacy API Player 1: {player1.get_name()}")
    print(f"Legacy API Player 2: {player2.get_name()}")
    print("\n✓ Old code continues to work with new architecture!")


def demo_registry():
    """Demo 5: Engine Registry"""
    print("\n" + "="*80)
    print("DEMO 5: EngineRegistry (Auto-discovery)")
    print("="*80)
    
    # List all registered engines
    engines = EngineRegistry.list_engines()
    
    print(f"Registered Engines: {len(engines)}\n")
    
    for name, metadata in engines.items():
        print(f"{name:15} | {metadata.display_name:20} | {metadata.strength:10}")


def demo_comparison():
    """Demo 6: Comparison OLD vs NEW"""
    print("\n" + "="*80)
    print("DEMO 6: OLD Architecture vs NEW Architecture")
    print("="*80)
    
    print("\n❌ OLD (6+ duplicate classes):")
    print("  from Players.AIPlayerBitboardBookParallel import AIPlayerBitboardBookParallel")
    print("  player = AIPlayerBitboardBookParallel(depth=8)")
    print("  # Hardcoded engine + features!")
    
    print("\n✅ NEW (ONE class, infinite configurations):")
    print("  engine = (EngineBuilder()")
    print("      .use_bitboard()")
    print("      .with_advanced_evaluator()")
    print("      .with_opening_book('master.book')")
    print("      .with_parallel_search(threads=8)")
    print("      .build())")
    print("  player = AIPlayer(engine=engine, depth=8)")
    print("  # Fully modular and configurable!")
    
    print("\nVantaggi:")
    print("  • UNA classe invece di 6+")
    print("  • Engines intercambiabili")
    print("  • Testabile (mock injection)")
    print("  • Estendibile (new engine = implement interface)")
    print("  • SOLID compliance")


if __name__ == '__main__':
    print("\n" + "🏆" * 40)
    print(" " * 10 + "NUOVA ARCHITETTURA ENTERPRISE - DEMO")
    print("🏆" * 40)
    
    demo_basic_usage()
    demo_advanced_configuration()
    demo_presets()
    demo_backward_compatibility()
    demo_registry()
    demo_comparison()
    
    print("\n" + "="*80)
    print("✨ ARCHITETTURA ENTERPRISE COMPLETAMENTE IMPLEMENTATA! ✨")
    print("="*80)

