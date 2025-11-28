# Timeline Training: Scaletta 100, 1000, 10.000 Partite

## 📊 Panoramica

Questa guida mostra cosa aspettarsi durante il training a diverse milestone:
- **100 partite**: Training iniziale
- **1.000 partite**: Training intermedio
- **10.000 partite**: Training avanzato

---

## 🎯 Configurazione Base

Assumendo configurazione standard:
- **MCTS simulations**: 800 per mossa
- **Games per iterazione**: 100
- **Tempo per partita**: ~5-10 minuti
- **Iterazioni**: 1, 10, 100

---

## 📈 Milestone 1: 100 Partite (1 Iterazione)

### Tempo Totale
```
100 partite × 6 minuti = 600 minuti = 10 ore
```

**Breakdown**:
- Primo gioco: ~8 minuti (warmup)
- Giochi successivi: ~5-6 minuti ciascuno
- Training: ~10-20 minuti
- **Totale**: ~10-12 ore

### Cosa Succede

#### Self-Play (100 giochi)
```
Game 1:    ~8 minuti   (warmup MPS, primo gioco)
Game 2-10: ~6 minuti   (stabilizzazione)
Game 11-100: ~5 minuti (velocità normale)

Totale self-play: ~9-10 ore
```

#### Training
```
Replay buffer: ~6,000 posizioni
Batch size: 2048
Batches: ~3 batch
Tempo training: ~10-20 minuti
```

### Risultati Attesi

**Rete Neurale**:
- Policy: Da casuale → inizia a riconoscere pattern base
- Value: Da casuale → inizia a predire risultati
- Miglioramento: ~10-20% rispetto a iniziale

**Performance di Gioco**:
- Livello: Principiante debole
- Confronto: Simile a giocatore casuale migliorato
- Mosse: Alcune mosse sensate, molte casuali

**MCTS**:
- Trova mosse migliori della rete
- Rete impara da MCTS
- Divario rete-MCTS: Grande (rete debole)

### Checkpoint
```
experimental/checkpoints/
├─ latest.pth (22.5MB)
├─ checkpoint_1000.pth (se configurato)
└─ config_1000.yaml (se configurato)
```

---

## 📈 Milestone 2: 1.000 Partite (10 Iterazioni)

### Tempo Totale
```
1.000 partite × 5 minuti = 5.000 minuti = 83 ore = ~3.5 giorni
```

**Breakdown**:
- Self-play: ~80 ore
- Training: ~3 ore
- **Totale**: ~83-85 ore (~3.5 giorni continuativi)

### Cosa Succede

#### Iterazione 1 (100 giochi)
```
Tempo: ~10 ore
Rete: Molto debole
```

#### Iterazione 2-5 (400 giochi)
```
Tempo: ~35 ore
Rete: Migliora gradualmente
- Inizia a riconoscere angoli importanti
- Valuta meglio posizioni semplici
- Policy migliora leggermente
```

#### Iterazione 6-10 (500 giochi)
```
Tempo: ~40 ore
Rete: Miglioramento significativo
- Riconosce pattern base
- Valuta posizioni con più accuratezza
- Policy più coerente
```

### Risultati Attesi

**Rete Neurale**:
- Policy: Riconosce pattern base (angoli, mobilità)
- Value: Predice risultati con ~40-50% accuratezza
- Miglioramento: ~50-70% rispetto a iniziale

**Performance di Gioco**:
- Livello: Principiante-intermedio
- Confronto: Simile a giocatore Minimax depth 3-4
- Mosse: Molte mosse sensate, alcune ancora deboli

**MCTS**:
- Trova mosse migliori della rete
- Rete si avvicina a MCTS
- Divario rete-MCTS: Medio (rete migliorata)

**Confronto con Altri Player**:
```
vs Random:        ~90% vittorie
vs Greedy:        ~70% vittorie
vs Minimax (d=3): ~50% vittorie
vs Minimax (d=5): ~30% vittorie
```

### Checkpoint
```
experimental/checkpoints/
├─ latest.pth
├─ checkpoint_1000.pth
├─ checkpoint_2000.pth
├─ ...
├─ checkpoint_10000.pth
└─ config_10000.yaml
```

---

## 📈 Milestone 3: 10.000 Partite (100 Iterazioni)

### Tempo Totale
```
10.000 partite × 5 minuti = 50.000 minuti = 833 ore = ~35 giorni
```

**Breakdown**:
- Self-play: ~800 ore
- Training: ~33 ore
- **Totale**: ~833-850 ore (~35 giorni continuativi)

### Cosa Succede

#### Iterazioni 1-10 (1.000 giochi)
```
Tempo: ~85 ore
Rete: Miglioramento base
```

#### Iterazioni 11-50 (4.000 giochi)
```
Tempo: ~340 ore
Rete: Miglioramento significativo
- Riconosce pattern complessi
- Valuta posizioni con accuratezza
- Policy molto migliorata
```

#### Iterazioni 51-100 (5.000 giochi)
```
Tempo: ~425 ore
Rete: Miglioramento avanzato
- Riconosce strategie avanzate
- Valuta posizioni con alta accuratezza
- Policy molto accurata
```

### Risultati Attesi

**Rete Neurale**:
- Policy: Riconosce pattern avanzati e strategie
- Value: Predice risultati con ~70-80% accuratezza
- Miglioramento: ~80-90% rispetto a iniziale

**Performance di Gioco**:
- Livello: Intermedio-avanzato
- Confronto: Simile a giocatore Minimax depth 6-7
- Mosse: Quasi tutte mosse forti, poche deboli

**MCTS**:
- Rete e MCTS quasi concordano
- Rete molto accurata
- Divario rete-MCTS: Piccolo (rete forte)

**Confronto con Altri Player**:
```
vs Random:        ~98% vittorie
vs Greedy:        ~90% vittorie
vs Minimax (d=3): ~80% vittorie
vs Minimax (d=5): ~60% vittorie
vs Minimax (d=6): ~45% vittorie
vs Apocalyptron:  ~40% vittorie
```

### Checkpoint
```
experimental/checkpoints/
├─ latest.pth (22.5MB)
├─ checkpoint_1000.pth
├─ checkpoint_2000.pth
├─ ...
├─ checkpoint_100000.pth
└─ config_100000.yaml
```

---

## ⏱️ Timeline Dettagliata

### 100 Partite (1 Iterazione)

```
00:00 - Inizio training
00:01 - Caricamento modello
00:05 - Primo gioco iniziato
00:13 - Primo gioco completato (8 min)
00:19 - 2° gioco completato (6 min)
00:25 - 3° gioco completato (6 min)
...
09:30 - 100° gioco completato
09:40 - Training iniziato
10:00 - Training completato
10:00 - Checkpoint salvato
10:00 - Iterazione 1 completata ✓
```

**Output atteso**:
```
Iteration 1/1000000
Self-play: 100 games completed in 9.5 hours
Training: Completed in 20 minutes
Loss: Policy=2.1, Value=0.8, Total=2.9
```

### 1.000 Partite (10 Iterazioni)

```
Giorno 1:
  00:00 - Iterazione 1 iniziata
  10:00 - Iterazione 1 completata
  10:20 - Iterazione 2 iniziata
  20:20 - Iterazione 2 completata
  ...

Giorno 2:
  Continua iterazioni 3-5
  ...

Giorno 3:
  Continua iterazioni 6-10
  83:00 - 1.000 partite completate ✓
```

**Output atteso**:
```
Iteration 10/1000000
Self-play: 1,000 games completed
Training: 10 epochs completed
Loss: Policy=1.5, Value=0.5, Total=2.0
Improvement: ~50% from initial
```

### 10.000 Partite (100 Iterazioni)

```
Settimana 1:
  Iterazioni 1-20 completate
  ~200 giochi/giorno
  
Settimana 2:
  Iterazioni 21-40 completate
  ~200 giochi/giorno
  
Settimana 3:
  Iterazioni 41-60 completate
  ~200 giochi/giorno
  
Settimana 4:
  Iterazioni 61-80 completate
  ~200 giochi/giorno
  
Settimana 5:
  Iterazioni 81-100 completate
  833:00 - 10.000 partite completate ✓
```

**Output atteso**:
```
Iteration 100/1000000
Self-play: 10,000 games completed
Training: 100 epochs completed
Loss: Policy=0.8, Value=0.3, Total=1.1
Improvement: ~85% from initial
```

---

## 📊 Metriche di Progresso

### Loss Values

| Milestone | Policy Loss | Value Loss | Total Loss |
|-----------|------------|------------|------------|
| **Iniziale** | ~3.5 | ~1.5 | ~5.0 |
| **100 partite** | ~2.1 | ~0.8 | ~2.9 |
| **1.000 partite** | ~1.5 | ~0.5 | ~2.0 |
| **10.000 partite** | ~0.8 | ~0.3 | ~1.1 |

### Performance vs Altri Player

| Milestone | vs Random | vs Greedy | vs Minimax d=5 |
|-----------|-----------|-----------|----------------|
| **100 partite** | ~60% | ~40% | ~20% |
| **1.000 partite** | ~90% | ~70% | ~30% |
| **10.000 partite** | ~98% | ~90% | ~60% |

### Valutazione Posizione Iniziale

| Milestone | Value Estimate | Accuratezza |
|-----------|----------------|-------------|
| **Iniziale** | ~0.0 (casuale) | 0% |
| **100 partite** | ~+0.02 | ~20% |
| **1.000 partite** | ~+0.05 | ~50% |
| **10.000 partite** | ~+0.08 | ~80% |

---

## 🚀 Accelerazione Training

### Opzione 1: Config Veloce

```yaml
mcts:
  simulations: 400  # Invece di 800 (2x più veloce)

self_play:
  games_per_iteration: 50  # Invece di 100 (2x più veloce)
```

**Tempi**:
- 100 partite: ~5 ore (invece di 10)
- 1.000 partite: ~42 ore (invece di 83)
- 10.000 partite: ~417 ore (invece di 833)

### Opzione 2: Training Parallelo

Eseguire più giochi in parallelo (richiede modifiche al codice):
- 4 processi paralleli = 4x più veloce
- 100 partite: ~2.5 ore
- 1.000 partite: ~21 ore
- 10.000 partite: ~208 ore

### Opzione 3: Ridurre Simulazioni Progressivamente

```yaml
# Inizio: molte simulazioni
mcts:
  simulations: 800

# Dopo 1.000 partite: riduci
mcts:
  simulations: 400

# Dopo 10.000 partite: riduci ancora
mcts:
  simulations: 200
```

---

## 📋 Checklist per Ogni Milestone

### ✅ 100 Partite

- [ ] Training completato senza errori
- [ ] Checkpoint salvato correttamente
- [ ] Loss diminuisce
- [ ] Modello può giocare partite

**Test**:
```bash
python experimental/rl_player/evaluate.py
python experimental/rl_player/play_against.py
```

### ✅ 1.000 Partite

- [ ] 10 iterazioni completate
- [ ] Loss diminuita significativamente
- [ ] Performance migliorata vs altri player
- [ ] Modello gioca mosse sensate

**Test**:
```bash
# Confronta con altri player
python experimental/rl_player/compare_players.py
```

### ✅ 10.000 Partite

- [ ] 100 iterazioni completate
- [ ] Loss molto bassa
- [ ] Performance competitiva
- [ ] Modello molto forte

**Test**:
```bash
# Torneo completo
python tournament/tournament.py --config tournament_config_with_rl.json
```

---

## 🎯 Raccomandazioni

### Per Test Rapidi
- **100 partite**: Sufficiente per vedere se funziona
- Tempo: ~10 ore
- Config: Veloce (400 simulazioni, 50 giochi)

### Per Training Serio
- **1.000 partite**: Buon punto di partenza
- Tempo: ~3.5 giorni
- Config: Standard (800 simulazioni, 100 giochi)

### Per Training Avanzato
- **10.000 partite**: Modello molto forte
- Tempo: ~35 giorni
- Config: Standard o avanzato

### Per Training Professionale
- **100.000+ partite**: Livello professionale
- Tempo: ~1 anno
- Config: Avanzato (1600 simulazioni, 200 giochi)

---

## 📈 Grafico Progresso Atteso

```
Performance
    ↑
100%│                    ╱─────────── (10k partite)
    │                 ╱
 80%│              ╱
    │           ╱
 60%│        ╱
    │     ╱
 40%│  ╱
    │╱
 20%│
    │
  0%└─────────────────────────────────→ Partite
     0    100   1k    5k    10k
```

---

## 🎓 Conclusione

**Scaletta Training**:

1. **100 partite** (~10 ore)
   - Verifica che funzioni
   - Modello debole ma funzionante

2. **1.000 partite** (~3.5 giorni)
   - Modello migliorato
   - Performance competitive base

3. **10.000 partite** (~35 giorni)
   - Modello molto forte
   - Performance competitiva avanzata

**Raccomandazione**: Inizia con 100 partite per testare, poi continua fino a 1.000-10.000 per risultati migliori!

