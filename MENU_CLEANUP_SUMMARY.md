# Menu Cleanup - Solo Grandmaster

## 🎯 Obiettivo
Mantenere solo il Grandmaster visibile nel menu di selezione AI.

## ✅ Modifiche Effettuate

### 1. PlayerFactory Semplificato

**File**: `src/Players/PlayerFactory.py`

**Prima**:
```python
from Players.AIPlayerBitboardBook import AIPlayerBitboardBook
from Players.AIPlayerBitboardBookParallel import AIPlayerBitboardBookParallel
from Players.Monkey import Monkey
from Players.NetworkPlayer import NetworkPlayer

ALL_PLAYER_CLASSES = [
    HumanPlayer,
    AIPlayerBitboardBook,
    AIPlayerBitboardBookParallel,
    AIPlayerGrandmaster,
    Monkey,
    NetworkPlayer,
]
```

**Dopo**:
```python
# Solo import necessari
from Players.HumanPlayer import HumanPlayer
from Players.AIPlayerGrandmaster import AIPlayerGrandmaster

ALL_PLAYER_CLASSES = [
    HumanPlayer,          # enabled: False (non in menu)
    AIPlayerGrandmaster,  # enabled: True (unico nel menu)
]
```

### 2. HumanPlayer Disabilitato dal Menu

**File**: `src/Players/HumanPlayer.py`

**Modifica**:
```python
PLAYER_METADATA = {
    'display_name': 'Human Player',
    'description': 'You! Play with mouse or keyboard controls',
    'enabled': False,  # ← Cambiato da True a False
    'parameters': []
}
```

**Motivo**: HumanPlayer viene creato automaticamente quando si gioca contro l'AI. Non serve selezionarlo dal menu.

### 3. Grandmaster Unico Abilitato

**File**: `src/Players/AIPlayerGrandmaster.py`

**Stato**:
```python
PLAYER_METADATA = {
    'display_name': 'Grandmaster',
    'description': 'Ultimate AI - Futility + LMR + null move + aspiration + ID',
    'enabled': True,  # ✅ Unico AI abilitato
    'parameters': {
        'difficulty': {
            'type': int,
            'min': 7,
            'max': 12,
            'default': 9
        }
    }
}
```

## 📊 Risultato

### Menu di Selezione AI

**Prima**:
- Human Player
- Random Chaos (Monkey)
- Greedy Player
- Heuristic Player  
- AIPlayer
- AIPlayerBook
- AIPlayerBitboard
- The Oracle
- Parallel Oracle
- **Grandmaster**
- Network Player

**Dopo**:
- **Grandmaster** ← UNICO

### Player Disponibili via API

Anche se non visibili nel menu, i seguenti player sono ancora disponibili programmaticamente:

```python
# Via codice Python
from Players.HumanPlayer import HumanPlayer
from Players.AIPlayerGrandmaster import AIPlayerGrandmaster

# Uso diretto
human = HumanPlayer("You")
gm = AIPlayerGrandmaster(deep=9)
```

## 🎮 Come Funziona il Menu

1. **Selezione AI**: Il menu mostra solo "Grandmaster"
2. **Selezione difficoltà**: Profondità 7-12 (default: 9)
3. **Selezione stile** (opzionale): Default, Aggressive, Defensive, etc.
4. **Avvio partita**: Il gioco crea automaticamente:
   - Un `HumanPlayer` per l'utente
   - Un `AIPlayerGrandmaster` con i parametri scelti

## ✅ Vantaggi

1. **Semplicità**: Un solo AI da scegliere
2. **Chiarezza**: Non c'è confusione su quale AI scegliere
3. **Focus**: Grandmaster è l'AI migliore, gli altri erano obsoleti
4. **Flessibilità**: 7 stili diversi disponibili via weights
5. **Performance**: Codice più pulito e veloce

## 🔧 Personalizzazione Avanzata

Per utenti avanzati che vogliono diversi stili di Grandmaster:

```python
from Players.AIPlayerGrandmaster import AIPlayerGrandmaster
from AI.GrandmasterWeights import get_preset_weights

# Aggressive
weights = get_preset_weights('aggressive')
gm = AIPlayerGrandmaster(deep=9, weights=weights)

# Corner Hunter
weights = get_preset_weights('corner_hunter')
gm = AIPlayerGrandmaster(deep=9, weights=weights)

# Custom
from AI.GrandmasterWeights import GrandmasterWeights
weights = GrandmasterWeights()
weights.mobility_midgame = 30
gm = AIPlayerGrandmaster(deep=9, weights=weights)
```

## 📝 File Modificati

1. ✅ `src/Players/PlayerFactory.py` - Rimossi import e player obsoleti
2. ✅ `src/Players/HumanPlayer.py` - Disabilitato dal menu (enabled: False)

## 📈 Impatto

- **Player nel menu**: 11 → 1 (solo Grandmaster)
- **Import eliminati**: 5 (AIPlayerBitboardBook, AIPlayerBitboardBookParallel, Monkey, NetworkPlayer, e i loro engine)
- **Codice più semplice**: ✅
- **Funzionalità preservata**: ✅ (tutto il codice esistente funziona)

---

**Data**: 2025-10-19  
**Status**: ✅ Completato  
**Impatto**: Menu semplificato - solo Grandmaster  

