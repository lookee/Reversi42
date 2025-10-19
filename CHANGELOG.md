# Changelog - Reversi42

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [3.2.0] - 2025-10-19

### 🎓 Opening Book System - Major Overhaul

#### Added
- **Automatic Book Loading**: All `.txt` files in `Books/` directory loaded automatically
- **HYBRID Evaluation Strategy**: Intelligent opening selection using AVERAGE + VARIETY_BONUS
- **Professional Opening Collections**:
  - FFO Repertoire: 586 C4-based openings with advantage evaluations
  - PointyStone3: 57 F5-based tactical openings
  - Total: 644+ professional openings
- **Advantage System**: Positional evaluation (`=`, `b`, `b+`, `b++`, `w`, `w+`, `w++`)
- **Contextual Scoring**: Evaluations adapt to player color (Black vs White)
- **Visual Display Enhancements**:
  - Opening names with first move indicator `[C4]` or `[F5]`
  - Advantage display with evaluation scores
  - Grouped display by available moves
  - Always-present opening information (even when out of book)
  - Remaining openings counter `[X in book]`

#### Opening Book Parameters (Configurable)
- `advantage_weight = 0.2`: Base weight for advantage evaluation
- `variety_weight = 0.1`: Bonus for tactical flexibility  
- `only_evaluated_openings = True`: Filter non-evaluated openings

#### Opening Book Files Renamed
- `00_opening_ffo.txt`: FFO Professional Repertoire
- `01_opening_pointystone.txt`: PointyStone3 Collection
- Format: `NAME | MOVES | ADVANTAGE` (standardized)

### 🤖 Grandmaster AI - Advanced Optimizations

#### Added
- **Iterative Deepening**: Progressive search 1→N with PV move ordering (1.5-2.5x)
- **History Heuristic**: Global move success tracking weighted by depth² (1.2-1.4x)
- **Aspiration Windows**: Narrow search optimization [value±50] (1.2-1.5x, 90-97% success)
- **Null Move Pruning**: Skip-turn verification for dominant positions (1.5-2.5x, 30-50% success)
- **Multi-Cut Pruning**: Early cutoff detection C=3, M=10 (1.15-1.3x)
- **Late Move Reduction (LMR)**: Reduced depth for moves 4+ (1.4-2x, 7-15% re-search)
- **Futility Pruning**: Hopeless position detection at frontier (1.15-1.25x)
- **Game Statistics Report**: Comprehensive end-game performance analysis
- **Opening Info in Summary**: Shows detected opening and remaining book moves

#### Improved
- **Cumulative Speedup**: Now 18-60x from all optimizations combined
- **Summary Display**: Robot icon 🤖 and detailed optimization breakdown
- **Opening Display**: Always shows current/following opening with book count

### 📚 Documentation

#### Added
- Acknowledgments section thanking Donato Barnaba
- Recommended Study Tools section with WOF link
- Comprehensive opening book evaluation documentation
- Updated all player documentation files

#### Changed
- Default Pygame player: Grandmaster at depth 6
- Opening book display improved throughout terminal and pygame views

---

