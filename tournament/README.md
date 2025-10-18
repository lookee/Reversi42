# Reversi42 Tournament System

Sistema completo per tornei automatizzati tra AI con analisi statistica avanzata.

## 🚀 Quick Start

### Metodo 1: Selezione Interattiva (RACCOMANDATO) 🌟

```bash
cd tournament
./select_tournament.sh
```

Ti mostrerà un menu con tutti i tornei disponibili, dettagli e tempo stimato!

### Metodo 2: Esegui TUTTI i Tornei 🚀 NEW

```bash
cd tournament
./run_all_tournaments.sh
```

Esegue automaticamente tutti i 12 tornei (1,120 partite totali, ~4 ore).
Perfetto per testing completo o per eseguire in background overnight!

### Metodo 3: Torneo con Configurazione Diretta ✨

```bash
cd tournament
./run_quick_tournament.sh
```

Oppure scegli una configurazione specifica:

```bash
./run_tournament.sh quick_tournament.json
./run_tournament.sh elite_tournament.json
./run_tournament.sh grandmaster_challenge.json
```

### Metodo 4: Torneo Interattivo

```bash
cd tournament
python3 tournament.py
```

Configura interattivamente:
- Numero di giocatori (2-10)
- Tipo di AI per ogni giocatore
- Livelli di difficoltà
- Partite per matchup

### Metodo 5: Quick Tournament Script

```bash
cd tournament
python3 quick_tournament.py
```

Carica automaticamente la configurazione da `ring/quick_tournament.json`.

## 📁 Struttura Directory

```
tournament/
├── README.md                    # Questo file
├── tournament.py                # Sistema principale di torneo
├── quick_tournament.py          # Torneo rapido (usa configurazione)
├── select_tournament.sh         # Selector interattivo ⭐
├── run_all_tournaments.sh       # Esegue TUTTI i tornei ⭐ NEW
├── run_tournament.sh            # Script per eseguire tornei da config
├── run_quick_tournament.sh      # Script per quick tournament
├── TOURNAMENTS_GUIDE.md         # Guida completa ai 12 tornei ⭐
├── CONFIGURATION_SYSTEM.md      # Sistema di configurazione ⭐
├── TOURNAMENT_README.md         # Documentazione tecnica completa
├── TOURNAMENT_USAGE.txt         # Guida rapida all'uso
├── ring/                        # File di configurazione tornei (12 configs!)
│   ├── README.md                # Guida alle configurazioni
│   ├── quick_tournament.json    # ⚡ Showcase completo (9 AI)
│   ├── elite_tournament.json    # 🏆 Solo i migliori (5 top AI)
│   ├── tournament_of_champions.json  # 🏆 Battaglia epica (7 campioni)
│   ├── grandmaster_challenge.json    # 👑 Sfida il Grandmaster
│   ├── beginner_friendly.json   # 🎓 Perfetto per imparare
│   ├── depth_progression.json   # 📊 Confronto profondità
│   ├── bitboard_benchmark.json  # ⚡ Test velocità bitboard
│   ├── opening_book_showdown.json    # 📚 Con vs senza book
│   ├── rapid_fire.json          # ⚡ Ultra veloce (1-2 min)
│   ├── speed_test.json          # 📊 Test performance
│   ├── evaluator_comparison.json     # 📊 Confronto evaluator
│   └── opening_book_test.json   # 📚 Test book effectiveness
└── reports/                     # Report dei tornei (auto-generati)
    ├── README.md
    ├── tournament_report_*.txt  # Report individuali
    └── all_tournaments_summary_*.txt  # Summary batch execution ⭐
```

## 🎯 Cosa Include

### Funzionalità v3.1

- ✅ **12 Tornei Pre-Configurati** - Pronti all'uso in `ring/` ⭐
- ✅ **Script Interattivo** - Menu visuale con `./select_tournament.sh` ⭐ NEW
- ✅ **Sistema di Configurazione JSON** - Tornei riutilizzabili e condivisibili ⭐ NEW
- ✅ **Script Shell** - Esecuzione rapida con `./run_tournament.sh`
- ✅ **Supporto AI Avanzati** - Bitboard, Parallel Oracle, Grandmaster ⭐ NEW
- ✅ Round-robin completo (tutti contro tutti)
- ✅ Bilanciamento colori (stesso numero di partite come Nero e Bianco)
- ✅ Esecuzione veloce senza grafica
- ✅ Timing preciso di ogni mossa
- ✅ Report statistico dettagliato
- ✅ Storico mosse completo (opzionale)
- ✅ Discovery automatico dei player dai metadati
- ✅ Salvataggio/Caricamento configurazioni

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

## 📝 Configurazioni Tornei Disponibili (12 Tornei)

### 🌟 Tornei in Evidenza

#### 1. Quick Tournament - Best AI Showcase ⚡
**File**: `quick_tournament.json`
- **Giocatori**: 9 (Random → Grandmaster)
- **Partite Totali**: 144
- **Tempo**: ~10-15 minuti
- **Scopo**: Panoramica completa di tutte le categorie AI
- **Include**: Random Chaos, Greedy Goblin, Heuristic Scout, AlphaBeta-6, Opening Scholar-6, Bitboard Blitz-8, The Oracle-8, Parallel Oracle-8, Grandmaster-9

#### 2. Tournament of Champions 🏆
**File**: `tournament_of_champions.json`
- **Giocatori**: 7 (un campione per categoria)
- **Partite Totali**: 294
- **Tempo**: ~45-60 minuti
- **Scopo**: Battaglia epica tra i migliori rappresentanti
- **Include**: Heuristic Champion, Minimax Champion-7, Opening Book Champion-7, Speed Champion-10, Hybrid Champion-9, Parallel Champion-9, Ultimate Champion-10

#### 3. Grandmaster Challenge 👑
**File**: `grandmaster_challenge.json`
- **Giocatori**: 6 (top AI vs Grandmaster-11)
- **Partite Totali**: 150
- **Tempo**: ~30-45 minuti
- **Scopo**: Sfida estrema - qualcuno può battere il Grandmaster?
- **Include**: AlphaBeta Expert-8, Scholar Master-8, Blitz Champion-10, Oracle Supreme-10, Parallel Elite-10, Grandmaster-11

#### 4. Elite Tournament 🏆
**File**: `elite_tournament.json`
- **Giocatori**: 5 (solo i più forti)
- **Partite Totali**: 100
- **Tempo**: ~20-30 minuti
- **Scopo**: Competizione ad alto livello
- **Include**: Opening Scholar-7, Bitboard Blitz-9, The Oracle-9, Parallel Oracle-9, Grandmaster-10

### 📊 Tornei di Analisi

#### 5. Depth Progression
**File**: `depth_progression.json`
- **Giocatori**: 4 (stesso AI, profondità diverse)
- **Partite Totali**: 36
- **Tempo**: ~15-20 minuti
- **Scopo**: Capire l'impatto della profondità di ricerca
- **Include**: Standard AI a depth 3, 5, 7, 9

#### 6. Evaluator Comparison
**File**: `evaluator_comparison.json`
- **Giocatori**: 4 (stessa profondità, evaluator diversi)
- **Partite Totali**: 36
- **Tempo**: ~8-12 minuti
- **Scopo**: Confrontare le funzioni di valutazione
- **Include**: Standard, Advanced, Simple, Greedy Evaluator (tutti depth 6)

#### 7. Opening Book Showdown 📚
**File**: `opening_book_showdown.json`
- **Giocatori**: 4 (con/senza book)
- **Partite Totali**: 60
- **Tempo**: ~12-18 minuti
- **Scopo**: Misurare l'impatto dell'opening book
- **Include**: AI senza book vs AI con book a depth 5 e 7

#### 8. Opening Book Test
**File**: `opening_book_test.json`
- **Giocatori**: 4 (varianti con opening book)
- **Partite Totali**: 60
- **Tempo**: ~10-15 minuti
- **Scopo**: Test efficacia opening book

### ⚡ Tornei di Velocità

#### 9. Bitboard Benchmark
**File**: `bitboard_benchmark.json`
- **Giocatori**: 6 (tutte varianti bitboard)
- **Partite Totali**: 60
- **Tempo**: ~8-12 minuti
- **Scopo**: Showcase delle performance bitboard
- **Include**: Bitboard-8/10, Oracle-8/10, Parallel-9, Grandmaster-10

#### 10. Rapid Fire Championship ⚡
**File**: `rapid_fire.json`
- **Giocatori**: 3 (solo risposta istantanea)
- **Partite Totali**: 60
- **Tempo**: ~1-2 minuti
- **Scopo**: Risultati ultra-rapidi
- **Include**: Random, Greedy, Heuristic (10 games per matchup)

#### 11. Speed Test
**File**: `speed_test.json`
- **Giocatori**: 4 (giocatori veloci)
- **Partite Totali**: 60
- **Tempo**: ~2-3 minuti
- **Scopo**: Baseline performance
- **Include**: Heuristic, Greedy, Monkey, AI-3

### 🎓 Tornei per Imparare

#### 12. Beginner Friendly
**File**: `beginner_friendly.json`
- **Giocatori**: 5 (progressione facile)
- **Partite Totali**: 60
- **Tempo**: ~3-5 minuti
- **Scopo**: Perfetto per imparare le basi
- **Include**: Random, Greedy, Heuristic, AlphaBeta-3, AlphaBeta-4

### Creare Configurazione Personalizzata

#### Metodo 1: File JSON Manuale

Crea `ring/my_tournament.json`:

```json
{
  "name": "My Tournament",
  "description": "Custom tournament configuration",
  "games_per_matchup": 3,
  "include_move_history": true,
  "players": [
    {
      "type": "AI",
      "name": "Standard-6",
      "difficulty": 6,
      "engine": "Minimax",
      "evaluator": "Standard"
    },
    {
      "type": "AIBook",
      "name": "BookMaster-6",
      "difficulty": 6,
      "engine": "Minimax",
      "evaluator": "Standard"
    }
  ]
}
```

Esegui:
```bash
./run_tournament.sh my_tournament.json
```

#### Metodo 2: Salvataggio Interattivo

```bash
python3 tournament.py --save-config ring/my_tournament.json
```

Configura interattivamente, poi salva per riutilizzo futuro.

#### Metodo 3: Programmazione Python

```python
from tournament import Tournament

tournament = Tournament(
    players_config=[
        ("AI", "Player1", 6, "Minimax", "Standard"),
        ("AI", "Player2", 8, "Minimax", "Advanced"),
    ],
    games_per_matchup=5,
    include_move_history=True,
    name="My Tournament",
    description="Custom tournament"
)

# Salva configurazione
tournament.save_config('ring/my_tournament.json')

# Oppure esegui subito
tournament.run()
```

### Esempi di Configurazione Legacy (Python)

#### Torneo Competitivo
```python
players_config = [
    ("AI", "Minimax-Std-6", 6, "Minimax", "Standard"),
    ("AI", "Minimax-Adv-6", 6, "Minimax", "Advanced"),
    ("AI", "Minimax-Std-8", 8, "Minimax", "Standard"),
]
games_per_matchup = 5  # 30 partite totali
```

#### Confronto Strategie
```python
players_config = [
    ("AI", "Standard-Eval", 6, "Minimax", "Standard"),
    ("AI", "Advanced-Eval", 6, "Minimax", "Advanced"),
    ("AI", "Greedy-Eval", 6, "Minimax", "Greedy"),
]
games_per_matchup = 10  # 60 partite totali
```

## 📊 Tabella Riepilogativa Tornei

| # | Nome | Players | Partite | Storia | Tempo | Categoria | Difficoltà |
|---|------|---------|---------|--------|-------|-----------|------------|
| 1 | Quick Tournament | 9 | 144 | ✓ | 10-15 min | ⚡ Showcase | Mista |
| 2 | Tournament of Champions | 7 | 294 | ✓ | 45-60 min | 🏆 Epic | Alta |
| 3 | Grandmaster Challenge | 6 | 150 | ✓ | 30-45 min | 👑 Ultimate | Estrema |
| 4 | Elite Tournament | 5 | 100 | ✓ | 20-30 min | 🏆 Competitive | Alta |
| 5 | Depth Progression | 4 | 36 | ✓ | 15-20 min | 📊 Analysis | Media |
| 6 | Evaluator Comparison | 4 | 36 | ✓ | 8-12 min | 📊 Analysis | Media |
| 7 | Opening Book Showdown | 4 | 60 | ✓ | 12-18 min | 📚 Analysis | Media |
| 8 | Opening Book Test | 4 | 60 | ✓ | 10-15 min | 📚 Learning | Media |
| 9 | Bitboard Benchmark | 6 | 60 | ✗ | 8-12 min | ⚡ Speed | Alta |
| 10 | Rapid Fire | 3 | 60 | ✗ | 1-2 min | ⚡ Speed | Bassa |
| 11 | Speed Test | 4 | 60 | ✗ | 2-3 min | 📊 Speed | Bassa |
| 12 | Beginner Friendly | 5 | 60 | ✗ | 3-5 min | 🎓 Learning | Bassa |

**Totale: 1,120 partite attraverso tutti i tornei configurati!**

## 🎯 Guida alla Selezione del Torneo

### Per Scopo

| Se vuoi... | Torneo Raccomandato | Tempo |
|------------|---------------------|-------|
| **Panoramica generale** | Quick Tournament | 10-15 min |
| **Imparare le basi** | Beginner Friendly | 3-5 min |
| **Test veloce** | Rapid Fire | 1-2 min |
| **Analisi profonda** | Tournament of Champions | 45-60 min |
| **Sfida massima** | Grandmaster Challenge | 30-45 min |
| **Velocità showcase** | Bitboard Benchmark | 8-12 min |
| **Studio opening** | Opening Book Showdown | 12-18 min |
| **Analisi depth** | Depth Progression | 15-20 min |

### Per Tempo Disponibile

| Tempo | Tornei Consigliati |
|-------|-------------------|
| **< 5 minuti** | Rapid Fire, Speed Test, Beginner Friendly |
| **5-15 minuti** | Quick Tournament, Bitboard Benchmark, Evaluator Comparison |
| **15-30 minuti** | Elite Tournament, Depth Progression, Opening Book tests |
| **30-60 minuti** | Grandmaster Challenge, Tournament of Champions |

### Per Livello Giocatore

| Livello | Torneo di Partenza |
|---------|-------------------|
| **Principiante** | Beginner Friendly → Quick Tournament |
| **Intermedio** | Quick Tournament → Elite Tournament |
| **Avanzato** | Elite Tournament → Grandmaster Challenge |
| **Esperto** | Tournament of Champions (analisi completa) |

## 📚 Documentazione Completa

### Guide Principali
- **[TOURNAMENTS_GUIDE.md](TOURNAMENTS_GUIDE.md)** - Guida completa ai 12 tornei ⭐ NEW
- **[ring/README.md](ring/README.md)** - Guida configurazioni JSON dettagliata ⭐ NEW
- **[CONFIGURATION_SYSTEM.md](CONFIGURATION_SYSTEM.md)** - Riferimento tecnico sistema config ⭐ NEW

### Documentazione Legacy
- **TOURNAMENT_README.md** - Documentazione tecnica completa
- **TOURNAMENT_USAGE.txt** - Guida rapida all'uso

## 🔧 Opzioni Linea di Comando

### Caricamento Configurazione
```bash
python3 tournament.py --config ring/my_tournament.json
```

### Salvataggio Configurazione
```bash
python3 tournament.py --save-config ring/new_tournament.json
```

Segui il processo interattivo, la configurazione verrà salvata al termine.

### Help
```bash
python3 tournament.py --help
```

## 💡 Suggerimenti

### Per Iniziare
1. Usa `./select_tournament.sh` per vedere tutti i tornei
2. Prova **Rapid Fire** per un test veloce (1-2 min)
3. Poi **Quick Tournament** per panoramica completa (10-15 min)

### Per Testing Completo 🚀
```bash
# Esegue TUTTI i 12 tornei automaticamente
./run_all_tournaments.sh
```
- 1,120 partite totali
- ~4 ore di esecuzione
- Report individuali + summary batch
- Perfetto per eseguire overnight o in background
- Genera analisi completa di tutto il sistema

### Per Testing Specifico
1. **Speed Test** - baseline velocità
2. **Evaluator Comparison** - confronto strategie
3. **Depth Progression** - impatto profondità

### Per Competizione
1. **Elite Tournament** - top tier battle
2. **Grandmaster Challenge** - sfida suprema
3. **Tournament of Champions** - analisi completa

### Per Ricerca
1. Abilita **move history** per analisi dettagliata
2. Usa configurazioni con molte partite per significatività statistica
3. Studia i report in `reports/` per insights
4. Usa **run_all_tournaments.sh** per dataset completo

## 📦 File di Output

Ogni torneo genera:
- **Report testuale**: `reports/tournament_report_YYYYMMDD_HHMMSS.txt`
- **Statistiche complete**: Rankings, H2H matrix, timing analysis
- **Move history** (se abilitato): Notazione completa partite

## 🚀 Esempi Pratici

### Esempio 1: Quick Start
```bash
cd tournament
./select_tournament.sh
# Scegli [1] per Quick Tournament
```

### Esempio 2: Sfida il Grandmaster
```bash
./run_tournament.sh grandmaster_challenge.json
```

### Esempio 3: Test Rapido
```bash
./run_tournament.sh rapid_fire.json
```

### Esempio 4: Esecuzione Batch Completa 🚀
```bash
# Esegui tutti i 12 tornei (1,120 partite, ~4 ore)
./run_all_tournaments.sh

# Per esecuzione in background:
nohup ./run_all_tournaments.sh > batch_execution.log 2>&1 &

# Per esecuzione con screen:
screen -S tournaments
./run_all_tournaments.sh
# Ctrl+A+D per detach
```

### Esempio 5: Creare Torneo Personalizzato
```bash
# Copia una configurazione esistente
cp ring/quick_tournament.json ring/my_custom.json

# Modifica con il tuo editor preferito
nano ring/my_custom.json

# Esegui
./run_tournament.sh my_custom.json
```

## Note Tecniche

- Solo AI (no giocatori umani)
- Dimensione scacchiera: 8x8
- Nessuna grafica per massima velocità
- Statistiche memorizzate in RAM durante l'esecuzione
- Compatibile Python 3.6+
- Supporta tutti i player types da Monkey a Grandmaster

---

**Buon torneo!** 🏆

*Reversi42 Tournament System v3.1.0 - 12 Pre-Configured Tournaments*

