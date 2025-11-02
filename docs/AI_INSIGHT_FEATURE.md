# AI Insight Feature

**Feature implementata:** 2025-11-02  
**Versione:** 5.1.0

## 📋 Panoramica

La feature **AI Insight** fornisce una visualizzazione in tempo reale del ragionamento dell'AI durante la ricerca della mossa migliore. Mostra tutti i passaggi, le ottimizzazioni e le statistiche dettagliate del processo di thinking.

## 🎯 Funzionalità

### Pulsante AI Insight
- Nuovo pulsante dedicato con icona lampadina 💡
- Posizionato accanto al pulsante "Developer-Insight" nella barra inferiore
- Click per aprire/chiudere il pannello laterale

### Pannello AI Insight
- **Posizione**: Slide-in dal lato destro della schermata
- **Dimensioni**: 50% larghezza (min 600px, max 900px)
- **Design**: Gradient background blu scuro con effetti glow
- **Funzionalità**:
  - Clear: pulisce tutti i log
  - Close: chiude il pannello
  - Auto-scroll: segue automaticamente i nuovi log

### Tipi di Log Visualizzati

#### 🎯 Search Start (Verde #10b981)
```
[14:23:45.123] 🎯 Starting search (target depth: 9, mode: sequential)
```
Indica l'inizio della ricerca con profondità target e modalità.

#### ⚡ Iteration Start (Blu #63b3ed)
```
[14:23:45.125] ⚡ Depth 1/9 [Aspiration: α=-100, β=100]
```
Inizio di ogni livello di iterative deepening con finestra di aspirazione.

#### 📍 Move Evaluated (Viola #a78bfa)
```
[14:23:45.130] 📍 Move C4 → +12 (nodes: 150, pruned: 45, 30.0%, 5.0ms)
```
Valutazione di ogni mossa migliore con statistiche complete:
- Coordinata mossa
- Valore di valutazione
- Nodi esplorati
- Nodi potati (pruning)
- Percentuale di pruning
- Tempo di ricerca

#### ✓ Iteration Complete (Verde chiaro #34d399)
```
[14:23:45.140] ✓ Depth 1 complete: C4 (+12) - 450 nodes, 120 pruned, 15.0ms ✓
```
Completamento di ogni livello con riepilogo:
- Mossa migliore trovata
- Valutazione finale
- Nodi totali esplorati
- Nodi potati
- Tempo di iterazione
- Indicatore successo/fallimento aspiration window

#### 🏁 Search Complete (Oro #fbbf24, Bold)
```
[14:23:45.450] 🏁 Search complete! Move: C4 (+22) | Depth: 9 | Nodes: 125,340 | Pruned: 87,250 (69.6%) | Time: 325ms
```
Riepilogo finale con tutte le statistiche:
- Mossa selezionata
- Valutazione finale
- Profondità raggiunta
- Nodi totali esplorati
- Nodi totali potati con percentuale
- Tempo totale di ricerca

#### 🔀 Parallel Search (Arancione #f97316)
```
[14:23:45.200] 🔀 Starting parallel search: 4 workers at depth 7
```
Quando l'AI avvia ricerca parallela con worker multipli.

#### 🔄 Phase Transition (Rosa #ec4899)
```
[14:23:46.500] 🔄 Phase 1 → Phase 2: Depth 7/9, Best: C4 (+18), Time: 1.2s
```
Transizione tra fasi di ricerca (quando l'AI cambia strategia).

## 🔧 Implementazione Tecnica

### Backend (Python)

#### 1. WebSocketSearchObserver (`src/webgui/websocket_observer.py`)
- Estende `SearchObserver` dell'engine Apocalyptron
- Metodo `_send_ai_log()`: invia log formattati al frontend
- Log inviati per ogni evento del search:
  - `on_search_start()`
  - `on_iteration_start()`
  - `on_move_evaluated()`
  - `on_iteration_complete()`
  - `on_search_complete()`
  - `on_parallel_phase_start()`
  - `on_phase1_complete()`

#### 2. Backend Server (`src/webgui/backend_server.py`)
- Importa `WebSocketSearchObserver`
- Modifica `get_ai_move()` per accettare WebSocket
- Crea observer con loop asyncio corrente
- Passa observer a `ai.get_move()`

**Modifiche chiave:**
```python
# Create observer for AI insights
observer = WebSocketSearchObserver(websocket, session_id)
observer.loop = asyncio.get_running_loop()

# Pass to AI
ai_move = ai.get_move(game, move_list, observer)
```

### Frontend (JavaScript/HTML)

#### 1. Pannello UI (`src/webgui/game_websocket.html`)
```html
<!-- Pannello AI Insight -->
<div id="aiInsightWrapper">
  <div class="ai-insight-header">...</div>
  <div id="aiLogsContainer">
    <div id="aiLogsContent">...</div>
  </div>
</div>
```

#### 2. Styling CSS
- Pannello fixed position con z-index alto
- Colori specifici per ogni tipo di log
- Hover effects per leggibilità
- Auto-scroll container

#### 3. Logica JavaScript
```javascript
// Handler WebSocket message
case 'ai_log':
  appendAILog(message.data);
  break;

// Append log entry
function appendAILog(logData) {
  const { timestamp, log_type, message } = logData;
  // Create and append colored log entry
  // Auto-scroll to bottom
}
```

## 📊 Formato Messaggio WebSocket

### Server → Client
```json
{
  "type": "ai_log",
  "data": {
    "timestamp": "14:23:45.123",
    "log_type": "search_start",
    "message": "🎯 Starting search (target depth: 9, mode: sequential)",
    "details": {
      "depth": 9,
      "player": "DIVZERO.EXE",
      "mode": "sequential"
    }
  }
}
```

### Tipi di log_type
- `search_start`
- `iteration_start`
- `move_evaluated`
- `iteration_complete`
- `search_complete`
- `parallel_start`
- `phase_transition`

## 🎨 Design Pattern

### Colori per Tipo
Ogni tipo di log ha colore e background specifici per rapida identificazione:

| Tipo | Colore Border | Background | Uso |
|------|---------------|------------|-----|
| search_start | #10b981 (verde) | rgba(16,185,129,.05) | Inizio ricerca |
| iteration_start | #63b3ed (blu) | rgba(99,179,237,.05) | Inizio profondità |
| move_evaluated | #a78bfa (viola) | rgba(167,139,250,.04) | Valutazione mossa |
| iteration_complete | #34d399 (verde chiaro) | rgba(52,211,153,.05) | Fine profondità |
| search_complete | #fbbf24 (oro) | rgba(251,191,36,.08) | Fine ricerca |
| parallel_start | #f97316 (arancione) | rgba(249,115,22,.05) | Ricerca parallela |
| phase_transition | #ec4899 (rosa) | rgba(236,72,153,.05) | Cambio fase |

### Hover Effect
```css
.ai-log-entry:hover {
  background: rgba(99,179,237,.08);
}
```

## 🚀 Utilizzo

### 1. Avvia il server WebGUI
```bash
./reversi42
# oppure
python3 -m src.webgui.backend_server
```

### 2. Apri il browser
```
http://localhost:8000
```

### 3. Clicca sul pulsante "AI Insight"
Il pulsante con icona lampadina 💡 nella barra inferiore.

### 4. Osserva il ragionamento
- L'AI inizia a pensare
- I log compaiono in tempo reale
- Ogni passaggio è colorato e formattato
- Auto-scroll ai nuovi log

### 5. Analizza i dati
Puoi vedere:
- Profondità di ricerca raggiunta
- Mosse valutate
- Efficienza del pruning
- Tempo di ricerca per livello
- Mossa finale selezionata

## 🔍 Casi d'Uso

### Per Sviluppatori
- Debug dell'algoritmo di ricerca
- Verifica efficienza pruning
- Analisi performance per profondità
- Ottimizzazione aspiration windows

### Per Giocatori Avanzati
- Comprensione strategia AI
- Apprendimento valutazione posizioni
- Analisi profondità di ricerca
- Studio del processo decisionale

### Per Ricerca/Educazione
- Dimostrazione algoritmi minimax
- Visualizzazione alpha-beta pruning
- Studio iterative deepening
- Analisi aspiration windows

## 🐛 Troubleshooting

### Log non appaiono
1. Verifica che il server sia avviato
2. Controlla la console browser (F12)
3. Verifica connessione WebSocket (icona verde)
4. Riavvia il server se necessario

### Log si fermano
1. Verifica che l'AI stia effettivamente pensando
2. Controlla che non sia Human vs Human
3. Verifica log del server: `/tmp/backend_detailed.log`

### Performance lente
- Normale per AI complesse
- I log vengono inviati in tempo reale
- Observer ha overhead minimo (~1-2%)

## 📈 Metriche Performance

### Overhead Observer
- **CPU**: ~1-2% overhead
- **Latenza**: <1ms per messaggio
- **Bandwidth**: ~100-500 bytes per log

### Frequenza Invio
- `search_start`: 1 volta per mossa
- `iteration_start`: 1 volta per profondità
- `move_evaluated`: Solo best moves
- `iteration_complete`: 1 volta per profondità
- `search_complete`: 1 volta per mossa

**Totale**: ~20-100 messaggi per mossa (dipende dalla profondità)

## 🔮 Sviluppi Futuri

Possibili estensioni:
- [ ] Filtri per tipo di log
- [ ] Export log in file
- [ ] Grafici interattivi (profondità vs tempo)
- [ ] Highlight mosse nella board durante thinking
- [ ] Playback log step-by-step
- [ ] Confronto tra AI diverse
- [ ] Analisi statistica aggregata

## 📝 Changelog

### v5.1.0 (2025-11-02)
- ✨ Implementazione iniziale AI Insight
- ✨ Pulsante dedicato UI
- ✨ Pannello laterale con auto-scroll
- ✨ 7 tipi di log colorati
- ✨ WebSocketSearchObserver completo
- ✨ Integrazione backend/frontend

---

**Autore:** Luca Amore  
**Licenza:** GPL-3.0-or-later

