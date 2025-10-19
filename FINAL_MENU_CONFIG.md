# Configurazione Finale Menu

## 🎮 Player Disponibili nel Menu

### 1. **Human Player** ✅
- **Display Name**: "Human Player"
- **Enabled**: `True`
- **Descrizione**: "You! Play with mouse or keyboard controls"
- **Uso**: Giocare manualmente con mouse/tastiera

### 2. **Grandmaster** ✅  
- **Display Name**: "Grandmaster"
- **Enabled**: `True`
- **Descrizione**: "Ultimate AI - Futility + LMR + null move + aspiration + ID"
- **Parametri**: Difficoltà 7-12 (default: 9)
- **Uso**: L'AI più forte disponibile

## 🎯 Modalità di Gioco

### Opzione 1: Umano (Nero) vs Grandmaster (Bianco)
```
Black: Human Player
White: Grandmaster (depth 9)
```
→ L'utente gioca come Nero contro l'AI

### Opzione 2: Grandmaster (Nero) vs Umano (Bianco)
```
Black: Grandmaster (depth 9)
White: Human Player
```
→ L'AI gioca come Nero, utente come Bianco

### Opzione 3: Grandmaster vs Grandmaster
```
Black: Grandmaster (depth 9, aggressive)
White: Grandmaster (depth 9, defensive)
```
→ Osservare partita AI vs AI con stili diversi

### Opzione 4: Umano vs Umano
```
Black: Human Player
White: Human Player
```
→ Due giocatori umani (hot-seat)

## 📊 Riepilogo PlayerFactory

**File**: `src/Players/PlayerFactory.py`

```python
ALL_PLAYER_CLASSES = [
    HumanPlayer,          # enabled: True  ✅
    AIPlayerGrandmaster,  # enabled: True  ✅
]
```

**Player visibili nel menu**: 2
- Human Player
- Grandmaster

## 🎨 Stili Grandmaster Disponibili

Anche se non nel menu principale, è possibile usare diversi stili via codice:

1. **default** - Bilanciato
2. **aggressive** - Restringe mobilità avversaria  
3. **defensive** - Priorità stabilità
4. **corner_hunter** - Ossessionato angoli
5. **edge_control** - Dominio bordi
6. **endgame_specialist** - Focus endgame
7. **custom** - Configurazione personalizzata

## ✅ Vantaggi Configurazione

1. ✅ **Scelta semplice**: Solo 2 player nel menu
2. ✅ **Gioco umano**: Possibilità di giocare come Nero
3. ✅ **AI migliore**: Solo Grandmaster (il più forte)
4. ✅ **Flessibilità**: Configurazione posizioni (Nero/Bianco)
5. ✅ **Codice pulito**: Nessun player obsoleto

## 🔧 Configurazione Avanzata (via API)

Per utenti Python che vogliono personalizzare:

```python
from Players.HumanPlayer import HumanPlayer
from Players.AIPlayerGrandmaster import AIPlayerGrandmaster
from AI.GrandmasterWeights import get_preset_weights

# Umano vs Grandmaster Aggressive
human = HumanPlayer("You")
weights = get_preset_weights('aggressive')
gm = AIPlayerGrandmaster(deep=9, weights=weights)

# Gioca partita
# black = human, white = gm
```

---

**Status**: ✅ Configurazione finale completata  
**Menu**: Human Player + Grandmaster  
**Data**: 2025-10-19

