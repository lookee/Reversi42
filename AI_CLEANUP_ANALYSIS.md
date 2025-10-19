# Analisi Pulizia Directory AI

## 🔍 Dipendenze Grandmaster

### Catena di Dipendenze
```
AIPlayerGrandmaster
  └─→ GrandmasterEngine
      ├─→ ParallelBitboardMinimaxEngine
      │   └─→ BitboardMinimaxEngine
      │       └─→ GameEngine
      │           └─→ StandardEvaluator
      │               └─→ Evaluator (interface)
      └─→ GrandmasterWeights
  └─→ MinimaxEngine (fallback)
      └─→ GameEngine
  └─→ OpeningBook (via parent AIPlayerBitboardBook)
```

## ✅ File NECESSARI (Mantenere)

### Engines Core
1. **GameEngine.py** - Classe base per tutti gli engine
2. **MinimaxEngine.py** - Engine fallback per Grandmaster e AIPlayerBitboardBook
3. **BitboardMinimaxEngine.py** - Usato da AIPlayerBitboardBook (parent)
4. **ParallelBitboardMinimaxEngine.py** - Parent di GrandmasterEngine
5. **GrandmasterEngine.py** - Il motore Grandmaster principale

### Evaluators
6. **Evaluator.py** - Interfaccia base per tutti gli evaluator
7. **StandardEvaluator.py** - Evaluator di default usato da GameEngine

### Grandmaster
8. **GrandmasterWeights.py** - Sistema pesi parametrici Grandmaster

### Opening Book
9. **OpeningBook.py** - Usato dai player *Book

### Altro
10. **__init__.py** - File di inizializzazione modulo

**TOTALE: 10 file da mantenere**

---

## ❌ File NON NECESSARI (Eliminabili)

### Evaluators Non Usati
1. **SimpleEvaluator.py** 
   - Evaluator semplicissimo (solo piece count)
   - Non più usato da nessun player

2. **AdvancedEvaluator.py**
   - Evaluator avanzato con heuristics
   - Non più usato da nessun player

3. **GreedyEvaluator.py**
   - Evaluator greedy (massimizza capture immediate)
   - Era usato da GreedyPlayer (rimosso)

### Engines Non Usati
4. **HeuristicEngine.py**
   - Engine con valutazione euristica veloce
   - Era usato da HeuristicPlayer (rimosso)

5. **RandomEngine.py**
   - Engine che genera mosse casuali
   - Sostituito da Monkey player che implementa direttamente random

### Altri
6. **Strategy.py**
   - File strategia (probabilmente vecchio design)
   - Non importato da nessuno

**TOTALE: 6 file eliminabili**

---

## 📊 Verifica Dipendenze

### File Eliminabili - Verifica Import

**SimpleEvaluator.py**:
```python
from AI.Evaluator import Evaluator
```
✅ Dipende solo da Evaluator (mantenuto)

**AdvancedEvaluator.py**:
```python
from AI.Evaluator import Evaluator
```
✅ Dipende solo da Evaluator (mantenuto)

**GreedyEvaluator.py**:
```python
from AI.Evaluator import Evaluator
```
✅ Dipende solo da Evaluator (mantenuto)

**HeuristicEngine.py**:
- Da verificare dipendenze interne

**RandomEngine.py**:
- Da verificare dipendenze interne

**Strategy.py**:
- Da verificare contenuto

---

## 📝 Riepilogo

### Mantenere (10 file)
- ✅ GameEngine.py
- ✅ MinimaxEngine.py
- ✅ BitboardMinimaxEngine.py
- ✅ ParallelBitboardMinimaxEngine.py
- ✅ GrandmasterEngine.py
- ✅ Evaluator.py
- ✅ StandardEvaluator.py
- ✅ GrandmasterWeights.py
- ✅ OpeningBook.py
- ✅ __init__.py

### Eliminare (6 file)
- ❌ SimpleEvaluator.py
- ❌ AdvancedEvaluator.py
- ❌ GreedyEvaluator.py
- ❌ HeuristicEngine.py
- ❌ RandomEngine.py
- ❌ Strategy.py

---

## ⚠️ Attenzione

Prima di eliminare, verificare:
1. Nessun import nei test
2. Nessun import in esempi/demo
3. Nessuna dipendenza circolare nascosta

## 🎯 Risultato Atteso

**Prima**: 17 file
**Dopo**: 11 file (10 + __pycache__)

**Riduzione**: ~35% dei file
**Codice mantenuto**: Solo dipendenze dirette di Grandmaster

