#!/usr/bin/env python3
"""
Comprehensive Test Suite for BitboardBook Integration

This test suite ensures the stability and correctness of the AIPlayerBitboardBook
implementation by testing:
1. Game -> BitboardGame conversion accuracy
2. Move generation consistency between standard and bitboard
3. Opening book integration
4. Late-game positions (move 55+)
5. Edge cases and stress tests
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Reversi.Game import Game, Move
from Reversi.BitboardGame import BitboardGame
from Players.AIPlayerBitboard import AIPlayerBitboard
from Players.AIPlayerBitboardBook import AIPlayerBitboardBook
from Players.AIPlayer import AIPlayer
from AI.OpeningBook import OpeningBook, get_default_opening_book

# Test counters
tests_run = 0
tests_passed = 0
tests_failed = 0

def test_assert(condition, test_name, error_msg=""):
    """Helper to track test results"""
    global tests_run, tests_passed, tests_failed
    tests_run += 1
    
    if condition:
        tests_passed += 1
        print(f"  ✓ {test_name}")
        return True
    else:
        tests_failed += 1
        print(f"  ✗ {test_name}")
        if error_msg:
            print(f"    Error: {error_msg}")
        return False


class TestBitboardConversion:
    """Test Game -> BitboardGame conversion"""
    
    @staticmethod
    def test_initial_position():
        """Test conversion of initial game position"""
        print("\n[TEST] Initial Position Conversion")
        
        # Create standard game
        standard = Game(8)
        
        # Convert to bitboard
        bitboard = AIPlayerBitboard()._convert_to_bitboard(standard)
        
        # Verify piece counts
        test_assert(bitboard.black_cnt == 2, "Initial black count")
        test_assert(bitboard.white_cnt == 2, "Initial white count")
        test_assert(bitboard.turn == 'B', "Initial turn is Black")
        test_assert(bitboard.turn_cnt == standard.turn_cnt, f"Turn count matches ({bitboard.turn_cnt})")
        
        # Verify initial positions (D4=W, E4=B, D5=B, E5=W)
        # In bitboard: D4 = bit 27, E4 = bit 28, D5 = bit 35, E5 = bit 36
        white_d4 = (bitboard.white >> 27) & 1
        black_e4 = (bitboard.black >> 28) & 1
        black_d5 = (bitboard.black >> 35) & 1
        white_e5 = (bitboard.white >> 36) & 1
        
        test_assert(white_d4 == 1, "White at D4")
        test_assert(black_e4 == 1, "Black at E4")
        test_assert(black_d5 == 1, "Black at D5")
        test_assert(white_e5 == 1, "White at E5")
    
    @staticmethod
    def test_conversion_consistency():
        """Test that conversion produces valid game states"""
        print("\n[TEST] Conversion Consistency")
        
        standard = Game(8)
        bitboard = AIPlayerBitboard()._convert_to_bitboard(standard)
        
        # Total pieces should match
        standard_total = standard.black_cnt + standard.white_cnt
        bitboard_total = bitboard.black_cnt + bitboard.white_cnt
        test_assert(standard_total == bitboard_total, 
                   f"Total piece count matches ({standard_total})")
        
        # No overlap between black and white
        overlap = bitboard.black & bitboard.white
        test_assert(overlap == 0, "No overlap between black and white bitboards")
        
        # Virtual matrix should match standard matrix
        matches = 0
        for y in range(1, 9):
            for x in range(1, 9):
                if bitboard.matrix[y][x] == standard.matrix[y][x]:
                    matches += 1
        
        test_assert(matches == 64, f"Virtual matrix matches ({matches}/64 cells)")
    
    @staticmethod
    def test_midgame_conversion():
        """Test conversion after several moves"""
        print("\n[TEST] Mid-game Conversion")
        
        # Play some moves
        standard = Game(8)
        moves_to_play = [
            Move(6, 5),  # F5
            Move(4, 6),  # D6
            Move(3, 5),  # C5
        ]
        
        for move_to_play in moves_to_play:
            available_moves = standard.get_move_list()
            if move_to_play in available_moves:
                standard.move(move_to_play)
        
        # Convert and verify
        bitboard = AIPlayerBitboard()._convert_to_bitboard(standard)
        
        test_assert(bitboard.black_cnt == standard.black_cnt, 
                   f"Black count matches ({bitboard.black_cnt})")
        test_assert(bitboard.white_cnt == standard.white_cnt,
                   f"White count matches ({bitboard.white_cnt})")
        test_assert(bitboard.turn == standard.turn,
                   f"Turn matches ({bitboard.turn})")
        
        # Verify all cells match
        all_match = True
        for y in range(1, 9):
            for x in range(1, 9):
                if bitboard.matrix[y][x] != standard.matrix[y][x]:
                    all_match = False
                    break
        
        test_assert(all_match, "All board positions match")


class TestMoveGeneration:
    """Test that bitboard generates same moves as standard"""
    
    @staticmethod
    def test_initial_moves():
        """Test initial position move generation"""
        print("\n[TEST] Initial Move Generation")
        
        standard = Game(8)
        bitboard = BitboardGame()
        
        std_moves = set(standard.get_move_list())
        bb_moves = set(bitboard.get_move_list())
        
        test_assert(std_moves == bb_moves,
                   f"Initial moves match",
                   f"Standard: {std_moves}, Bitboard: {bb_moves}")
        
        test_assert(len(std_moves) == 4,
                   "Initial position has 4 moves")
    
    @staticmethod
    def test_moves_after_sequence():
        """Test move generation after a sequence of moves"""
        print("\n[TEST] Move Generation After Sequence")
        
        # Play opening sequence
        opening = "F5d6C3"  # Tiger opening
        
        standard = Game(8)
        bitboard = BitboardGame()
        
        # Parse and play moves
        i = 0
        while i < len(opening):
            if opening[i].isalpha() and i + 1 < len(opening):
                move_str = opening[i:i+2]
                col = ord(move_str[0].upper()) - ord('A') + 1
                row = int(move_str[1])
                move = Move(col, row)
                
                # Play on both boards
                std_moves = standard.get_move_list()
                bb_moves = bitboard.get_move_list()
                
                if move in std_moves:
                    standard.move(move)
                if move in bb_moves:
                    bitboard.move(move)
                
                i += 2
            else:
                i += 1
        
        # Compare final move lists
        std_final = set(standard.get_move_list())
        bb_final = set(bitboard.get_move_list())
        
        test_assert(std_final == bb_final,
                   f"Moves match after opening sequence",
                   f"Standard: {std_final}, Bitboard: {bb_final}")
    
    @staticmethod
    def test_move_validation():
        """Test that both engines validate moves the same way"""
        print("\n[TEST] Move Validation Consistency")
        
        standard = Game(8)
        bitboard = BitboardGame()
        
        # Test valid move
        valid_move = Move(6, 5)  # F5
        test_assert(
            standard.valid_move(valid_move) == bitboard.valid_move(valid_move),
            "Valid move recognized by both"
        )
        
        # Test invalid move
        invalid_move = Move(1, 1)  # A1
        test_assert(
            standard.valid_move(invalid_move) == bitboard.valid_move(invalid_move),
            "Invalid move rejected by both"
        )


class TestOpeningBookIntegration:
    """Test opening book integration with bitboard"""
    
    @staticmethod
    def test_book_loading():
        """Test that opening book loads correctly"""
        print("\n[TEST] Opening Book Loading")
        
        book = get_default_opening_book()
        
        test_assert(book is not None, "Opening book loads")
        test_assert(book.lines_loaded > 0, 
                   f"Opening book has lines ({book.lines_loaded} loaded)")
    
    @staticmethod
    def test_book_move_retrieval():
        """Test retrieving moves from opening book"""
        print("\n[TEST] Opening Book Move Retrieval")
        
        book = get_default_opening_book()
        
        # Initial position should have book moves
        initial_moves = book.get_book_moves("")
        test_assert(len(initial_moves) > 0,
                   f"Book has initial moves ({len(initial_moves)} found)")
        
        # After F5, should have book responses
        after_f5 = book.get_book_moves("F5")
        test_assert(len(after_f5) > 0,
                   f"Book has moves after F5 ({len(after_f5)} found)")
    
    @staticmethod
    def test_book_player_initialization():
        """Test that BitboardBook player initializes correctly"""
        print("\n[TEST] BitboardBook Player Initialization")
        
        try:
            player = AIPlayerBitboardBook(deep=6, show_book_options=False)
            test_assert(True, "BitboardBook player initializes")
            test_assert(player.opening_book is not None, "Player has opening book")
            test_assert(player.bitboard_engine is not None, "Player has bitboard engine")
            test_assert(player.standard_engine is not None, "Player has fallback engine")
        except Exception as e:
            test_assert(False, "BitboardBook player initializes", str(e))


class TestLateGamePositions:
    """Test late-game positions where bugs were reported"""
    
    @staticmethod
    def test_move_55_plus():
        """Test positions at move 55 and beyond"""
        print("\n[TEST] Late Game Positions (Move 55+)")
        
        # Create a late-game scenario by fast-forwarding
        standard = Game(8)
        bitboard = BitboardGame()
        
        # Play random moves until move 55+
        move_count = 0
        max_moves = 60
        
        while move_count < max_moves:
            std_moves = standard.get_move_list()
            bb_moves = bitboard.get_move_list()
            
            if len(std_moves) == 0 and len(bb_moves) == 0:
                # Game over
                break
            
            # Pick first available move
            if len(std_moves) > 0:
                standard.move(std_moves[0])
            else:
                standard.turn = 'W' if standard.turn == 'B' else 'B'
            
            if len(bb_moves) > 0:
                bitboard.move(bb_moves[0])
            else:
                bitboard.turn = 'W' if bitboard.turn == 'B' else 'B'
            
            move_count += 1
            
            # Test consistency every 5 moves
            if move_count % 5 == 0 and move_count >= 55:
                std_set = set(std_moves)
                bb_set = set(bb_moves)
                test_assert(
                    std_set == bb_set,
                    f"Moves match at move {move_count}",
                    f"Diff: std={std_set - bb_set}, bb={bb_set - std_set}"
                )
    
    @staticmethod
    def test_near_endgame():
        """Test positions with few pieces left to play"""
        print("\n[TEST] Near Endgame Positions")
        
        # This would require setting up specific endgame positions
        # For now, we'll test that the conversion still works
        standard = Game(8)
        
        # Manually set up a near-endgame position
        # (In practice, you'd load a saved game state)
        standard.turn_cnt = 58
        
        bitboard = AIPlayerBitboard()._convert_to_bitboard(standard)
        
        test_assert(bitboard.turn_cnt == standard.turn_cnt,
                   "Turn count preserved in late game")


class TestEdgeCases:
    """Test edge cases and stress scenarios"""
    
    @staticmethod
    def test_no_moves_available():
        """Test when no moves are available (pass turn)"""
        print("\n[TEST] No Moves Available")
        
        # This requires setting up a specific board state
        # For now, test that the player handles empty move lists
        game = Game(8)
        player = AIPlayerBitboardBook(deep=2, show_book_options=False)
        
        # Get move with no available moves (passing None for control)
        move = player.get_move(game, [], None)
        
        test_assert(move is None, "Returns None when no moves available")
    
    @staticmethod
    def test_out_of_book():
        """Test behavior when out of opening book"""
        print("\n[TEST] Out of Book Behavior")
        
        game = Game(8)
        player = AIPlayerBitboardBook(deep=2, show_book_options=False)
        
        # Play moves to get out of book quickly
        # Use unusual sequence unlikely to be in book
        unusual_moves = [
            Move(6, 5),  # F5
            Move(6, 6),  # F6 (if valid)
        ]
        
        for move_to_play in unusual_moves:
            moves = game.get_move_list()
            if move_to_play in moves:
                game.move(move_to_play)
        
        # Try to get a move (should use engine, not book)
        moves = game.get_move_list()
        if len(moves) > 0:
            try:
                move = player.get_move(game, moves, None)
                test_assert(move is not None, "Player finds move when out of book")
                test_assert(move in moves, "Move is valid")
            except Exception as e:
                test_assert(False, "Player works out of book", str(e))
    
    @staticmethod
    def test_bitboard_vs_standard_engine():
        """Compare bitboard and standard engine results"""
        print("\n[TEST] Bitboard vs Standard Engine")
        
        game = Game(8)
        
        # Create both players
        bb_player = AIPlayerBitboard(deep=3)
        std_player = AIPlayer(deep=3)
        
        moves = game.get_move_list()
        
        try:
            bb_move = bb_player.get_move(game, moves, None)
            std_move = std_player.get_move(game, moves, None)
            
            test_assert(bb_move is not None, "Bitboard finds a move")
            test_assert(std_move is not None, "Standard finds a move")
            test_assert(bb_move in moves, "Bitboard move is valid")
            test_assert(std_move in moves, "Standard move is valid")
            
            # Note: They might not choose the same move, but both should be valid
            print(f"    Bitboard chose: {bb_move}, Standard chose: {std_move}")
            
        except Exception as e:
            test_assert(False, "Both engines work", str(e))
    
    @staticmethod
    def test_history_preservation():
        """Test that game history is preserved through conversion"""
        print("\n[TEST] History Preservation")
        
        game = Game(8)
        
        # Play some moves
        moves_to_play = [Move(6, 5), Move(4, 6)]
        for move_to_play in moves_to_play:
            if move_to_play in game.get_move_list():
                game.move(move_to_play)
        
        # Convert to bitboard
        bitboard = AIPlayerBitboard()._convert_to_bitboard(game)
        
        test_assert(bitboard.history == game.history,
                   "History preserved in conversion",
                   f"Standard: '{game.history}', Bitboard: '{bitboard.history}'")


def run_all_tests():
    """Run all test suites"""
    print("=" * 80)
    print("BITBOARD BOOK COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    # Run all test classes
    test_classes = [
        TestBitboardConversion,
        TestMoveGeneration,
        TestOpeningBookIntegration,
        TestLateGamePositions,
        TestEdgeCases,
    ]
    
    for test_class in test_classes:
        print(f"\n{'=' * 80}")
        print(f"Running {test_class.__name__}")
        print('=' * 80)
        
        # Run all test methods
        for method_name in dir(test_class):
            if method_name.startswith('test_'):
                method = getattr(test_class, method_name)
                try:
                    method()
                except Exception as e:
                    print(f"\n  ✗ {method_name} - EXCEPTION: {e}")
                    import traceback
                    traceback.print_exc()
                    global tests_failed, tests_run
                    tests_failed += 1
                    tests_run += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total tests run: {tests_run}")
    print(f"Passed: {tests_passed} ✓")
    print(f"Failed: {tests_failed} ✗")
    print(f"Success rate: {(tests_passed/tests_run*100) if tests_run > 0 else 0:.1f}%")
    print("=" * 80)
    
    return tests_failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

