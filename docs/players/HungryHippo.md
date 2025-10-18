# Hungry Hippo 🦛

**Difficulty**: Beginner | **Style**: Greedy | **Strength**: Weak

## Overview

Hungry Hippo is a greedy AI that looks 3 moves ahead while trying to maximize captures. It's smarter than Random Chaos but still focuses on short-term gains rather than long-term strategy.

Perfect practice opponent for players learning tactical thinking!

## Key Characteristics

- **Icon**: 🦛
- **Engine**: Greedy (3-ply lookahead)
- **Speed**: Very Fast
- **Play Style**: Greedy, capture-focused
- **Best For**: Beginner players learning tactics

## How It Works

Hungry Hippo uses a simple greedy algorithm:

```
For each valid move:
  1. Simulate the move
  2. Count immediate captures
  3. Look 3 moves ahead
  4. Evaluate position
  5. Choose move with most captures
```

### Depth Settings

- **Default**: 3 moves ahead
- **Range**: 1-5
  - Depth 1: Pure greedy (instant captures only)
  - Depth 3: Tactical (default)
  - Depth 5: More strategic but slower

## Strengths

- ⚡ **Very fast**: Even at depth 3
- 🎯 **Some tactics**: Better than random
- 📊 **Consistent**: Same strategy every time
- 🦛 **Aggressive**: Forces action

## Weaknesses

- 👁️ **Short-sighted**: Doesn't see long-term traps
- 🏰 **Corner blind**: Doesn't value corners enough
- 📈 **Capture obsessed**: Quantity over quality
- 🎭 **Predictable**: Easy to trap

## Use Cases

### Learning Tactical Play
```
Perfect for:
- Understanding capture mechanics
- Learning short-term tactics
- Practicing corner control
- Building strategic thinking
```

### Benchmarking
```
Use for:
- Testing new strategies
- Quick tournament games
- AI comparison baseline
```

## Performance

| Metric | Rating |
|--------|--------|
| Strength | ★★☆☆☆ |
| Speed | ★★★★★ |
| Strategic Depth | ★★☆☆☆ |
| Learning Value | ★★★★☆ |

## Tactical Advice

**How to beat Hungry Hippo**:
1. **Sacrifice pieces**: Give away captures to set traps
2. **Control corners**: Hippo doesn't value them enough
3. **Limit mobility**: Force bad moves
4. **Think 4+ moves ahead**: Stay one step ahead

**What you'll learn**:
- Short-term vs long-term thinking
- When to sacrifice pieces
- Corner and edge control
- Mobility management

## Depth Comparison

| Depth | Strength | Speed | Best For |
|-------|----------|-------|----------|
| 1 | Very Weak | Instant | Pure greedy testing |
| 2 | Weak | Instant | Slight improvement |
| 3 | Weak+ | Very Fast | **Default - balanced** |
| 4 | Medium-Weak | Fast | Tougher practice |
| 5 | Medium-Weak | Medium | Maximum greedy power |

## Quote

> "I see food, I eat! Corners? Edges? No time! MUST. CAPTURE. NOW! 🦛"

## Configuration

```json
{
  "type": "Hungry Hippo",
  "depth": 3
}
```

### Custom Depth
```json
{
  "type": "Hungry Hippo",
  "depth": 5,
  "description": "Extra hungry mode!"
}
```

## Strategy Guide

### Early Game
Hungry Hippo will grab any captures it sees. Use this to:
- Set up corner traps
- Control the center
- Force bad positions

### Mid Game
It starts thinking ahead but still values captures too much:
- Sacrifice 2-3 pieces to gain corners
- Limit its mobility
- Create future opportunities

### Late Game
Weakest phase:
- Corner control wins
- Mobility advantage dominates
- Stay calm and play solid

---

**Next Step**: Mastered Hungry Hippo? Try **Berserker** for aggressive combat! ⚔️

