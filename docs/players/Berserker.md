# Berserker ⚔️

**Difficulty**: Intermediate | **Style**: Aggressive | **Strength**: Medium-Strong

## Overview

Berserker is a relentless aggressor that attacks without mercy! It maximizes captures with brutal efficiency, looking 5 moves ahead to plan overwhelming assaults. Berserker embodies pure aggressive gameplay!

## Key Characteristics

- **Icon**: ⚔️
- **Engine**: Greedy (5-ply lookahead)
- **Speed**: Very Fast
- **Play Style**: Aggressive, high-pressure
- **Specialty**: Overwhelming captures, brutal attacks
- **Best For**: Learning to handle aggressive opponents

## How It Works

Berserker uses enhanced greedy search with aggression bias:

```
For each valid move:
  1. Simulate move chain (5 moves deep)
  2. Evaluate captures + mobility
  3. Bonus points for aggressive positions
  4. Prioritize high-capture moves
  5. ATTACK!
```

### Aggression Features

- **High mobility preference**: Keeps options open for attacks
- **Capture maximization**: More pieces = more power
- **Pressure tactics**: Forces opponent into defensive positions
- **No mercy**: Takes every capture opportunity

## Strengths

- ⚔️ **Relentless pressure**: Never lets up
- ⚡ **Very fast**: Quick devastating attacks
- 🎯 **Tactical depth**: 5-ply lookahead
- 💪 **Aggressive**: Dominates passive players
- 🔥 **Intimidating**: Psychological advantage

## Weaknesses

- 🏰 **Corner neglect**: Too focused on captures
- 🎭 **Predictable**: Always aggressive
- 🛡️ **Weak defense**: Vulnerable to patient play
- 📉 **Endgame issues**: Quantity ≠ quality

## Use Cases

### Learning Defensive Play
```
Perfect for:
- Practicing defensive strategies
- Learning to handle pressure
- Sacrificial tactics
- Counter-attack timing
```

### Tournament Play
```
Use for:
- Quick aggressive games
- Testing defensive strategies
- Aggressive playstyle benchmarking
```

## Performance

| Metric | Rating |
|--------|--------|
| Strength | ★★★☆☆ |
| Speed | ★★★★★ |
| Strategic Depth | ★★★☆☆ |
| Aggression | ★★★★★ |
| Adaptability | ★★☆☆☆ |

## Tactical Advice

**How to beat Berserker**:
1. **Stay calm**: Don't panic under pressure
2. **Play defensively**: Let it overextend
3. **Secure corners**: Force it into bad positions
4. **Sacrifice wisely**: Trade pieces for position
5. **Patient endgame**: Quality beats quantity

**What you'll learn**:
- Defensive positioning
- Handling aggressive opponents
- Sacrificial tactics
- Staying calm under pressure
- Counter-attack timing

## Depth Comparison

| Depth | Strength | Speed | Aggression | Best For |
|-------|----------|-------|------------|----------|
| 2 | Weak | Instant | Low | Very gentle |
| 4 | Medium-Weak | Very Fast | Medium | Practice |
| 5 | Medium-Strong | Very Fast | **High** | **Default** |
| 6 | Strong | Fast | Very High | Challenging |
| 8 | Very Strong | Medium | Extreme | Brutal mode |

## Battle Strategy

### vs Defensive Players
Berserker excels against:
- Passive opponents
- Slow, methodical players
- Those who fear pressure

**Why**: Constant pressure creates mistakes

### vs Aggressive Players
Berserker struggles against:
- Other aggressive AIs
- Counter-attackers
- Tactical sacrificers

**Why**: Mutual aggression creates chaos

### vs Balanced Players
50/50 matchup:
- Depends on corner control
- Mobility battles
- Who adapts better

## Quote

> "ATTACK! Capture everything! No mercy! No retreat! Only VICTORY or VALHALLA! ⚔️🔥"

## Configuration

### Default (Recommended)
```json
{
  "type": "Berserker",
  "depth": 5
}
```

### Gentle Berserker
```json
{
  "type": "Berserker",
  "depth": 3,
  "description": "Still aggressive but weaker"
}
```

### BRUTAL Mode
```json
{
  "type": "Berserker",
  "depth": 8,
  "description": "⚠️ MAXIMUM AGGRESSION! ⚠️"
}
```

## Tournament Performance

Berserker typically:
- **Dominates**: Random Chaos, Hungry Hippo
- **Competitive with**: The Trickster, mid-depth Zen Master
- **Struggles against**: The Shadow, Ancient Sage, Quantum Mind
- **Destroyed by**: Apocalypse

## Advanced Tactics

**As Berserker**:
1. Maintain high mobility
2. Force opponent into corners (then attack edges)
3. Keep capturing every turn
4. Never let pressure drop

**Against Berserker**:
1. Secure corners ASAP
2. Sacrifice pieces strategically
3. Build solid defensive position
4. Wait for overextension
5. Counter-attack in endgame

---

**Next Step**: Ready for balance? Try **Zen Master** for harmony! 🧘 Or face **The Shadow** for defensive mastery! 🌑

