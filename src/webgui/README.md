# Reversi42 WebGUI

WebGUI modulare per Reversi42 con supporto WebSocket real-time, AI analytics e developer tools.

## 📁 Struttura File

```
src/webgui/
├── game_websocket.html          ← HTML principale (569 righe)
│
├── css/
│   └── styles.css               ← Stili CSS (1,074 righe, 17 sezioni)
│
├── js/
│   ├── game.js                  ← Logica principale (1,983 righe)
│   ├── dev-tools.js             ← Developer tools (104 righe)
│   ├── ai-insight.js            ← AI reasoning (85 righe)
│   └── ai-statistics.js         ← AI statistics (458 righe)
│
├── backend_server.py            ← Server WebSocket
├── backend_monitor.py           ← Monitor backend
├── websocket_observer.py        ← AI observer
├── start_server.sh              ← Avvio semplice
├── start_server_robust.sh       ← Avvio con monitor
└── README.md                    ← Questa documentazione
```

## 🎯 File Principali

### `game_websocket.html` (569 righe)
HTML pulito e semantico con:
- Header giocatori
- Scacchiera 8x8
- Pannelli laterali (history, opening tree, notes)
- Modals (players selection)
- Pannelli overlay (Developer-Insight, AI Insight)

### `css/styles.css` (1,074 righe)
CSS organizzato in 17 sezioni:
- CSS Variables & Root Styles
- Base Styles
- UI Components (Buttons, Chips, Avatars)
- Board & Game Elements
- Moves & History
- AI Stats & Analytics
- Opening Tree
- WebSocket Status & Traffic
- Modals & Dialogs
- Code Editor (CodeMirror)
- Animations
- AI Insight Panel
- AI Statistics Dashboard

### `js/game.js` (1,983 righe)
Logica principale organizzata in sezioni:
- Global Variables & Configuration
- Utility Functions (Formatting, DOM helpers)
- WebSocket (Connection, Messaging, Activity)
- Game State (Data loading, Management)
- Board (DOM construction, Events, Rendering)
- Game Controls (AI, Opening hints)
- Move Submission & AI requests
- Initialization
- UI Setup (History, Toolbar, Tooltips)
- Main Render loop
- Game Format (Import/Export: compact & XOT)

### `js/dev-tools.js` (104 righe)
Developer tools panel:
- Live server logs viewer (tail -f style)
- WebSocket traffic monitor
- Auto-refresh functionality
- Syntax highlighting

### `js/ai-insight.js` (85 righe)
AI reasoning panel:
- Live AI search logs
- Move evaluation tracking
- Thinking process visualization
- Auto-scroll to latest

### `js/ai-statistics.js` (458 righe)
AI performance dashboard:
- Comprehensive search statistics
- Pruning efficiency metrics
- Interactive charts (sparklines, bars, circular)
- Iterative deepening timeline
- Optimization indicators

## 🚀 Avvio Rapido

```bash
# Avvia il backend WebSocket
cd /Users/lucaamore/Documents/devel/Reversi42
python3 -m src.webgui.backend_server --port 8000 --player DIVZERO.EXE

# Apri nel browser
open http://localhost:8000
```

## 🎮 Funzionalità

- ✅ **Real-time WebSocket** - Connessione live con backend
- ✅ **AI vs Human** - Gioca contro AI o umano
- ✅ **Opening Book** - Suggerimenti aperture con varianti
- ✅ **Move History** - Cronologia con navigazione
- ✅ **Undo/Redo** - Navigazione posizioni
- ✅ **AI Analytics** - Statistiche dettagliate ricerca
- ✅ **Developer Tools** - Log server e traffico WebSocket
- ✅ **Import/Export** - Formati Compact e XOT
- ✅ **Responsive** - Adattivo a mobile/desktop

## 📊 Statistiche Refactoring

| Metrica | Prima | Dopo | Beneficio |
|---------|-------|------|-----------|
| **File totali** | 1 monolitico | 6 modulari | ✅ Manutenibilità |
| **HTML** | 4,192 righe | 569 righe | **-86% più pulito** |
| **Organizzazione** | Inline | File separati | ✅ Separazione concerns |
| **Riusabilità** | Bassa | Alta | ✅ Componenti riutilizzabili |
| **Debug** | Difficile | Facile | ✅ File specifici |

## 🏗️ Architettura

```
┌─────────────────────────────────────┐
│  game_websocket.html (HTML puro)   │
│  ├── styles.css                     │
│  ├── game.js (core)                 │
│  ├── dev-tools.js                   │
│  ├── ai-insight.js                  │
│  └── ai-statistics.js               │
└─────────────────────────────────────┘
              ▼ WebSocket
┌─────────────────────────────────────┐
│  backend_server.py                  │
│  ├── Game Engine                    │
│  ├── AI Players                     │
│  └── websocket_observer.py          │
└─────────────────────────────────────┘
```

## 🛠️ Sviluppo

### Modificare Stili
Edita `css/styles.css` - le modifiche si applicano immediatamente (ricarica browser)

### Modificare Logica
Edita file JavaScript specifico:
- `js/game.js` - logica gioco e board
- `js/dev-tools.js` - pannello developer
- `js/ai-insight.js` - pannello AI reasoning
- `js/ai-statistics.js` - dashboard statistics

### Debug
1. Apri Developer Tools (Cmd+Option+I)
2. Usa Developer-Insight panel per log server
3. Tutti i console.error sono mantenuti per debug

## 📝 Note

- **Architettura**: Completamente modulare con separazione HTML/CSS/JS
- **Compatibilità**: 100% funzionalità mantenuta
- **Performance**: Ottimizzata (browser cacha i file esterni)
- **Manutenibilità**: Drasticamente migliorata con file separati
- **Organizzazione**: Directory `css/` e `js/` per codice organizzato

## 🔧 Troubleshooting

**WebSocket non si connette:**
```bash
# Verifica backend attivo
lsof -i :8000

# Riavvia backend
./start_server_robust.sh
```

**Modifiche CSS non visibili:**
- Ricarica con cache vuota: Cmd+Shift+R

**Modifiche JS non visibili:**
- Ricarica hard: Cmd+Shift+R
- Verifica console per errori

## 📄 Licenza

Reversi42 - v3.2.0

