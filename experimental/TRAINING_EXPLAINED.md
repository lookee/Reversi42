# Spiegazione Dettagliata del Training RL

## 🎮 Cosa Succede Durante il Primo Gioco

### Fase 1: Inizializzazione (Istantaneo)

```
1. Carica modello neurale (22.5M parametri)
2. Inizializza MCTS con 800 simulazioni
3. Crea nuovo gioco Reversi (posizione iniziale)
4. Player corrente: Black (B)
```

**Tempo**: < 1 secondo

---

### Fase 2: Prima Mossa (Black) - Il Processo Più Lento

#### Step 2.1: Encoding dello Stato
```
Stato attuale del board:
  - Channel 0: Black pieces (2 pezzi iniziali)
  - Channel 1: White pieces (2 pezzi iniziali)
  - Channel 2: Legal moves mask (4 mosse possibili)
  - Channel 3: Mobility count (per ogni posizione)
  - Channel 4: Corner positions
  - Channel 5: Edge positions
  - Channel 6: Turn indicator (1.0 per Black)
  - Channel 7: Opening book moves (se in book)
```

**Output**: Tensor [1, 8, 8, 8] → [batch, channels, height, width]

**Tempo**: ~1ms

#### Step 2.2: Forward Pass della Rete Neurale
```
Input: [1, 8, 8, 8] tensor
  ↓
Convolutional Block (2 → 256 channels)
  ↓
19 Residual Blocks (ogni blocco: Conv → BN → ReLU → Conv → BN → Skip → ReLU)
  ↓
Policy Head: [1, 65] → probabilità per ogni mossa (64 posizioni + pass)
Value Head: [1, 1] → valore posizione [-1, +1]
```

**Output**:
- Policy logits: [65] valori (prima di softmax)
- Value: singolo valore (es. 0.02 = posizione leggermente favorevole a Black)

**Tempo**: ~5-10ms su M1 MPS

#### Step 2.3: MCTS Search (800 Simulazioni)

Per ogni simulazione (800 volte):

```
Simulazione 1:
  1. Selection: Traversa l'albero usando UCB1
     - Parte dalla root
     - Sceglie child con score UCB1 più alto
     - Continua fino a leaf node
     
  2. Expansion: Se il leaf non è terminale
     - Forward pass rete neurale sul leaf
     - Crea children per ogni mossa legale
     - Assegna prior probabilities dalla rete
     
  3. Evaluation: Valuta la posizione
     - Se terminale: usa risultato reale (vittoria/sconfitta/pareggio)
     - Se non terminale: usa value dalla rete neurale
     
  4. Backpropagation: Aggiorna statistiche
     - Incrementa visit_count del nodo
     - Aggiunge value a value_sum
     - Propaga valore (con segno invertito) al parent
     - Continua fino alla root

Simulazione 2-800: Ripete lo stesso processo
```

**Dettaglio UCB1 Score**:
```
UCB1(node) = exploitation + exploration

exploitation = value_sum / visit_count  (valore medio del nodo)
exploration = c_puct * prior_prob * sqrt(parent_visits) / (node_visits + 1)

c_puct = 1.0 (costante di esplorazione)
```

**Dopo 800 simulazioni**:
- Root node ha visitato tutti i 4 children possibili
- Ogni child ha un numero di visite proporzionale alla sua forza
- Esempio: Child A (mossa migliore): 350 visite, Child B: 200 visite, etc.

**Tempo totale MCTS**: ~4-8 secondi per mossa
- 800 simulazioni × ~5-10ms = 4-8 secondi

#### Step 2.4: Selezione Mossa

```
1. Calcola distribuzione visite:
   - Child A: 350 visite / 800 totali = 0.4375
   - Child B: 200 visite / 800 totali = 0.25
   - Child C: 150 visite / 800 totali = 0.1875
   - Child D: 100 visite / 800 totali = 0.125

2. Applica temperatura (τ=1.0 per exploration):
   - Distribuzione rimane invariata (temperatura 1.0)

3. Sample dalla distribuzione:
   - Probabilità di scegliere A: 43.75%
   - Probabilità di scegliere B: 25%
   - etc.

4. Seleziona mossa (es. Child A)
```

**Tempo**: < 1ms

#### Step 2.5: Salvataggio Dati Training

```
Salva tuple (state, policy_target, value_target):
  - state: Tensor [8, 8, 8] dello stato corrente
  - policy_target: Distribuzione visite MCTS [65] (normalizzata)
  - value_target: None (verrà assegnato alla fine del gioco)
```

**Tempo**: < 1ms

#### Step 2.6: Applica Mossa

```
1. Applica mossa al board
2. Aggiorna turno (B → W)
3. Incrementa move_count
```

**Tempo**: < 1ms

**Tempo totale prima mossa**: ~4-8 secondi

---

### Fase 3: Mosse Successive (2-60)

Ogni mossa ripete il processo della Fase 2:
- Encoding stato: ~1ms
- Forward pass rete: ~5-10ms
- MCTS (800 simulazioni): ~4-8 secondi
- Selezione mossa: < 1ms
- Salvataggio dati: < 1ms
- Applica mossa: < 1ms

**Tempo per mossa**: ~4-8 secondi
**Tempo totale gioco**: ~60 mosse × 5 secondi = **~5 minuti**

---

### Fase 4: Fine Gioco e Assegnazione Valori

Quando il gioco finisce:

```
1. Conta pezzi finali:
   - Black: 35 pezzi
   - White: 29 pezzi
   - Black vince!

2. Assegna valori finali:
   - Per ogni posizione giocata da Black: value = +1.0 (vittoria)
   - Per ogni posizione giocata da White: value = -1.0 (sconfitta)

3. Aggiorna training data:
   - (state_1, policy_1, None) → (state_1, policy_1, +1.0)
   - (state_2, policy_2, None) → (state_2, policy_2, -1.0)
   - ...
```

**Tempo**: < 1 secondo

**Risultato**: Lista di ~60 tuple (state, policy, value)

---

## 🧠 Come Funziona l'Addestramento della Rete

### Dopo il Primo Gioco (e i successivi 99)

#### Fase 1: Accumulo nel Replay Buffer

```
Dopo 100 giochi:
  - ~6,000 posizioni nel replay buffer
  - Ogni posizione ha:
    - Stato del board (input)
    - Policy target (distribuzione MCTS)
    - Value target (risultato finale del gioco)
```

#### Fase 2: Training Step (quando buffer >= 10,000 posizioni)

Per ogni batch (2048 posizioni):

```
1. Sample batch dal replay buffer:
   - states: [2048, 8, 8, 8]
   - policy_targets: [2048, 65]
   - value_targets: [2048]

2. Forward pass rete neurale:
   - Input: states [2048, 8, 8, 8]
   - Output: 
     * policy_logits: [2048, 65]
     * value_pred: [2048, 1]

3. Calcola Loss:
   
   Policy Loss (CrossEntropy):
   - Confronta policy_logits con policy_targets
   - La rete impara a predire la distribuzione MCTS
   - Formula: -Σ(target * log(softmax(pred)))
   
   Value Loss (MSE):
   - Confronta value_pred con value_targets
   - La rete impara a predire il risultato finale
   - Formula: (pred - target)²
   
   Total Loss = Policy Loss + Value Loss

4. Backward pass:
   - Calcola gradienti per tutti i parametri
   - Gradient clipping (max_norm=1.0) per stabilità

5. Update weights:
   - AdamW optimizer aggiorna i pesi
   - Learning rate: 0.001
   - Weight decay: 1e-4 (regularizzazione)
```

**Tempo per batch**: ~100-200ms su M1 MPS
**Numero batch per epoch**: ~5 batch (10,000 posizioni / 2048 batch_size)

#### Fase 3: Iterazione

```
Iterazione 1:
  1. Self-play: 100 giochi → ~6,000 posizioni
  2. Training: 5 batch → aggiorna rete
  3. Salva checkpoint (se iteration % 1000 == 0)

Iterazione 2:
  1. Self-play: 100 giochi (rete migliorata!)
  2. Training: 5 batch
  3. ...

Iterazione N:
  - La rete migliora gradualmente
  - Le mosse diventano più forti
  - Il gioco diventa più competitivo
```

---

## 📊 Flusso Completo Dettagliato

### Timeline Primo Gioco (5 minuti)

```
00:00 - Inizio
00:01 - Caricamento modello, inizializzazione
00:01 - Mossa 1 (Black): MCTS 800 simulazioni → 4-8 secondi
00:09 - Mossa 2 (White): MCTS 800 simulazioni → 4-8 secondi
00:17 - Mossa 3 (Black): MCTS 800 simulazioni → 4-8 secondi
...
04:30 - Mossa 60: Fine gioco
04:31 - Assegnazione valori finali
04:32 - Salvataggio dati training
```

### Timeline Training Completo

```
Iterazione 1:
  00:00 - Inizio
  05:00 - Gioco 1 completato (6,000 posizioni)
  10:00 - Gioco 2 completato (+6,000 posizioni)
  ...
  08:20 - Gioco 100 completato (600,000 posizioni totali)
  
  08:21 - Buffer size: 600,000 (> 10,000 min)
  08:21 - Training epoch:
          - Batch 1: Loss = 2.5
          - Batch 2: Loss = 2.3
          - Batch 3: Loss = 2.1
          - ...
          - Batch 293: Loss = 1.8
  08:30 - Training completato
  08:30 - Iterazione 1 completata

Iterazione 2:
  08:30 - Self-play con rete aggiornata
  ... (rete migliorata → mosse migliori → giochi più interessanti)
```

---

## 🎯 Cosa Impara la Rete

### Policy Head (65 output)

**Impara a predire**:
- Quale mossa è migliore in ogni posizione
- Basandosi sulla distribuzione MCTS (che considera molte simulazioni)

**Esempio**:
```
Posizione iniziale:
  - Rete iniziale: probabilità uniformi (1/4 = 25% per ogni mossa)
  - Dopo training: 
    * F5: 45% (mossa migliore secondo MCTS)
    * C4: 30%
    * D3: 15%
    * E6: 10%
```

### Value Head (1 output)

**Impara a predire**:
- Chi vincerà il gioco dalla posizione corrente
- Valore in [-1, +1]:
  - +1.0 = vittoria certa per il giocatore corrente
  - 0.0 = posizione equilibrata
  - -1.0 = sconfitta certa

**Esempio**:
```
Posizione iniziale:
  - Rete iniziale: value ≈ 0.0 (posizione equilibrata)
  - Dopo training: value ≈ 0.02 (leggermente favorevole a chi muove)

Posizione finale (Black vince 35-29):
  - Rete dovrebbe predire: value ≈ +0.1 per Black
```

---

## 🔄 Ciclo di Miglioramento

```
1. Rete iniziale (random):
   - Policy: distribuzione casuale
   - Value: valori casuali
   - Gioca mosse deboli

2. Self-play con rete iniziale:
   - MCTS trova mosse migliori della rete
   - Genera dati di training (stato → policy_MCTS, value_reale)

3. Training:
   - Rete impara a predire policy_MCTS e value_reale
   - Diventa più forte

4. Self-play con rete migliorata:
   - Rete predice meglio
   - MCTS trova mosse ancora migliori
   - Genera dati migliori

5. Training:
   - Rete impara da dati migliori
   - Diventa ancora più forte

6. Ripeti → Convergenza verso gioco perfetto
```

---

## ⚡ Perché è Lento

### Bottleneck Principale: MCTS

```
Per ogni mossa:
  - 800 simulazioni MCTS
  - Ogni simulazione: 1-2 forward pass rete
  - Totale: ~800-1600 forward pass per mossa
  
Per gioco:
  - ~60 mosse
  - Totale: ~48,000-96,000 forward pass
  
Tempo:
  - Forward pass: ~5-10ms su M1 MPS
  - Totale: ~4-8 minuti per gioco
```

### Ottimizzazioni Possibili

1. **Ridurre simulazioni MCTS**: 800 → 400 (2x più veloce)
2. **Batch MCTS**: Processare più stati insieme
3. **Early stopping**: Fermare MCTS se mossa chiara
4. **Parallelizzazione**: Più giochi in parallelo

---

## 📈 Progresso Atteso

### Primi 10 Giochi
- Rete molto debole
- MCTS domina completamente
- Giochi casuali/irregolari

### Dopo 100 Giochi
- Rete inizia a imparare pattern base
- Policy migliora leggermente
- Giochi più strutturati

### Dopo 1,000 Giochi
- Rete riconosce posizioni importanti
- Value prediction migliora
- Giochi più competitivi

### Dopo 10,000+ Giochi
- Rete molto forte
- Policy e value ben calibrati
- Giochi di alta qualità

---

## 🎓 Conclusione

Il primo gioco è lento perché:
1. **800 simulazioni MCTS per mossa** = molti forward pass
2. **Warmup MPS** = primo utilizzo GPU più lento
3. **Caricamento modelli** = overhead iniziale

Ma è **normale e necessario**:
- MCTS genera dati di alta qualità per training
- La rete impara da questi dati
- I giochi successivi saranno più veloci

**Raccomandazione**: Lascia correre il primo gioco (5-10 minuti), poi vedrai progresso più rapido!

