# Reversi42 Tournament System

Sistema completo per tornei automatizzati tra AI con analisi statistica avanzata.

## Quick Start

### Torneo Interattivo

```bash
cd tournament
python3 tournament.py
```

Configura interattivamente:
- Numero di giocatori (2-10)
- Tipo di AI per ogni giocatore
- Livelli di difficoltà
- Partite per matchup

### Torneo Rapido Pre-configurato

```bash
cd tournament
python3 quick_tournament.py
```

Esegue un torneo veloce con 4 giocatori pre-configurati.

## Struttura Directory

```
tournament/
├── README.md              # Questo file
├── tournament.py          # Sistema principale di torneo
├── quick_tournament.py    # Esempio torneo rapido
├── TOURNAMENT_README.md   # Documentazione completa
├── TOURNAMENT_USAGE.txt   # Guida rapida all'uso
└── reports/               # Report dei tornei (generati automaticamente)
    ├── README.md
    └── tournament_report_*.txt
```

## Cosa Include

### Funzionalità

- ✅ Round-robin completo (tutti contro tutti)
- ✅ Bilanciamento colori (stesso numero di partite come Nero e Bianco)
- ✅ Esecuzione veloce senza grafica
- ✅ Timing preciso di ogni mossa
- ✅ Report statistico dettagliato
- ✅ Storico mosse completo (opzionale)
- ✅ Discovery automatico dei player dai metadati

### AI Disponibili

I tipi di AI disponibili vengono rilevati automaticamente dai metadati dei player:

1. **Minimax** (Standard/Advanced/Greedy evaluator)
   - Difficoltà: 1-10
   - Ricerca alpha-beta completa

2. **Heuristic**
   - Euristiche semplici, veloce

3. **Greedy**
   - Massimizza catture immediate

4. **Monkey**
   - Mosse casuali (controllo)

Il sistema rileva automaticamente tutti i player abilitati e li mostra nel menu interattivo.

### Report Generato

Il sistema genera automaticamente un report dettagliato con:

1. **Panoramica Torneo**
   - Statistiche generali
   - Durata totale

2. **Classifica Generale**
   - Ordinata per win rate
   - Record W-L-D

3. **Analisi Dettagliata per Giocatore**
   - Performance come Nero/Bianco
   - Tempi di ragionamento
   - Vantaggio colore

4. **Matrice Head-to-Head**
   - Confronti diretti

5. **Analisi Durata Partite**

6. **Analisi Conteggio Mosse**

7. **Analisi da Esperto**
   - Campione del torneo
   - Giocatore più veloce
   - Giocatore più aggressivo
   - Insights strategici

8. **Storico Mosse Completo** (opzionale)
   - Notazione completa di tutte le partite
   - Uppercase = mosse Nero, lowercase = mosse Bianco
   - Utile per analisi post-torneo e replay

## Esempio Output

```
================================================================================
REVERSI42 TOURNAMENT - COMPREHENSIVE STATISTICAL REPORT
================================================================================

─────────────────────────────────────────────────────────────────────────────
OVERALL RANKINGS
─────────────────────────────────────────────────────────────────────────────
Rank  Player                      W     L     D    Win%   Avg Score
─────────────────────────────────────────────────────────────────────────────
1     Minimax-Adv-6              15     3     0    83.3%      36.22
2     Minimax-Std-6              12     6     0    66.7%      34.11
...

TIMING ANALYSIS:
  Average Move Time: 145.23ms
  Median Move Time: 132.45ms
  Total Thinking Time: 47.63s
```

## File di Output

I report vengono salvati automaticamente nella directory `reports/`:
```
reports/tournament_report_YYYYMMDD_HHMMSS.txt
```

Tutti i report vengono organizzati in questa directory per una facile gestione.

## Esempi di Configurazione

### Torneo Competitivo
```python
players_config = [
    ("AI", "Minimax-Std-6", 6, "Minimax", "Standard"),
    ("AI", "Minimax-Adv-6", 6, "Minimax", "Advanced"),
    ("AI", "Minimax-Std-8", 8, "Minimax", "Standard"),
]
games_per_matchup = 5  # 30 partite totali
```

### Confronto Strategie
```python
players_config = [
    ("AI", "Standard-Eval", 6, "Minimax", "Standard"),
    ("AI", "Advanced-Eval", 6, "Minimax", "Advanced"),
    ("AI", "Greedy-Eval", 6, "Minimax", "Greedy"),
]
games_per_matchup = 10  # 60 partite totali
```

## Documentazione Completa

Per maggiori dettagli:
- **TOURNAMENT_README.md** - Documentazione tecnica completa
- **TOURNAMENT_USAGE.txt** - Guida rapida all'uso

## Note

- Solo AI (no giocatori umani)
- Dimensione scacchiera: 8x8
- Nessuna grafica per massima velocità
- Statistiche memorizzate in RAM durante l'esecuzione

---

Buon torneo! 🏆

