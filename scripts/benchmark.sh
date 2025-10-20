#!/bin/bash
# Run performance benchmarks for Reversi42
# Usage: ./scripts/benchmark.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}⚡ Performance Benchmarks${NC}"
echo "======================================"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set headless mode for benchmarks
export REVERSI42_VIEW=headless

# 1. Bitboard operations benchmark
echo -e "\n${BLUE}→ Bitboard Operations${NC}"
python3 << 'PYTHON'
import time
from src.Reversi.BitboardGame import BitboardGame

game = BitboardGame()
iterations = 10000

# Move generation benchmark
start = time.perf_counter()
for _ in range(iterations):
    moves = game.get_valid_moves(1)
elapsed = (time.perf_counter() - start) / iterations * 1e9
print(f"  Move generation: {elapsed:.1f} ns/op")

# Make move benchmark  
start = time.perf_counter()
for _ in range(iterations):
    new_game = game.make_move(19)
elapsed = (time.perf_counter() - start) / iterations * 1e9
print(f"  Make move: {elapsed:.1f} ns/op")

# Score calculation
start = time.perf_counter()
for _ in range(iterations):
    score = game.get_score()
elapsed = (time.perf_counter() - start) / iterations * 1e9
print(f"  Get score: {elapsed:.1f} ns/op")
PYTHON

# 2. AI Performance benchmark
echo -e "\n${BLUE}→ AI Performance${NC}"
python3 << 'PYTHON'
import time
from src.Reversi.BitboardGame import BitboardGame
from src.Players.PlayerApocalyptron import PlayerApocalyptron

game = BitboardGame()

for depth in [6, 9]:
    player = PlayerApocalyptron(depth=depth)
    moves = game.get_valid_moves(1)
    
    start = time.perf_counter()
    move = player.get_move(game, moves, None)
    elapsed = time.perf_counter() - start
    
    print(f"  Depth {depth}: {elapsed:.3f} seconds")
    
    if depth == 6 and elapsed > 0.5:
        print(f"    ⚠️  Slower than expected (target: <0.5s)")
    elif depth == 9 and elapsed > 2.0:
        print(f"    ⚠️  Slower than expected (target: <2.0s)")
    else:
        print(f"    ✅ Within performance targets")
PYTHON

# 3. Memory usage
echo -e "\n${BLUE}→ Memory Usage${NC}"
python3 << 'PYTHON'
import sys
from src.Reversi.BitboardGame import BitboardGame
from src.Players.PlayerApocalyptron import PlayerApocalyptron

game = BitboardGame()
game_size = sys.getsizeof(game)
print(f"  BitboardGame: {game_size} bytes")

if game_size < 1024:
    print(f"    ✅ Optimal size (<1KB)")
else:
    print(f"    ⚠️  Larger than expected")

player = PlayerApocalyptron(depth=9)
player_size = sys.getsizeof(player)
print(f"  PlayerApocalyptron: {player_size} bytes")
PYTHON

# 4. Full game benchmark
echo -e "\n${BLUE}→ Full Game Completion${NC}"
python3 << 'PYTHON'
import time
from src.Reversi.BitboardGame import BitboardGame
from src.Players.PlayerApocalyptron import PlayerApocalyptron

game = BitboardGame()
black = PlayerApocalyptron(depth=6)
white = PlayerApocalyptron(depth=6)

start = time.perf_counter()
move_count = 0

while not game.is_game_over() and move_count < 60:
    moves = game.get_valid_moves(game.current_player)
    
    if not moves:
        game = game.pass_turn()
        continue
    
    player = black if game.current_player == 1 else white
    move = player.get_move(game, moves, None)
    game = game.make_move(move)
    move_count += 1

elapsed = time.perf_counter() - start
black_score, white_score = game.get_score()

print(f"  Game completed in {elapsed:.2f} seconds")
print(f"  Moves: {move_count}")
print(f"  Final score: Black {black_score} - White {white_score}")
print(f"  Time per move: {elapsed/move_count:.3f} seconds")

if elapsed < 60:
    print(f"    ✅ Excellent performance (<60s)")
else:
    print(f"    ⚠️  Slower than target")
PYTHON

echo -e "\n======================================"
echo -e "${GREEN}✅ Benchmark suite completed${NC}"

