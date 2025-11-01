# GuiWeb JSON-Driven System - Complete Guide

**Versione:** 1.0.0  
**Data:** 2025-10-21  
**Status:** ✅ Pronto per il tuo HTML!

---

## 🎯 Cosa Ho Preparato

### 1. **JSON Schema Completo** 📋

**File:** `docs/JSON_SCHEMA_GUIWEB.md` (400+ righe)

Schema TypeScript-documented che copre **TUTTO**:

- ✅ `meta` - Informazioni partita
- ✅ `players` - Black/White con config AI
- ✅ `game_state` - Stato corrente
- ✅ `status` - Turn, clocks, round
- ✅ `positions` - Board per ogni ply (64-char strings)
- ✅ `moves` - Storia mosse
- ✅ `move_details` - Dettagli completi ogni mossa
- ✅ `valid_by_ply` - Mosse valide per ply
- ✅ `opening_by_ply` - Suggerimenti opening
- ✅ `ai_stats_by_ply` - Statistiche AI complete
- ✅ `tournament` - Info torneo
- ✅ `annotations` - Commenti mosse
- ✅ `ui_settings` - Configurazione UI

### 2. **JSON Mock Completo** 🎮

**File:** `src/webgui/mock_game_complete.json` (200+ righe)

Esempio **reale** con:
- ✅ 6 posizioni (ply 0-5)
- ✅ 5 mosse giocate
- ✅ 3 AI stats complete
- ✅ Opening suggestions per ogni ply
- ✅ Valid moves per ogni ply
- ✅ Annotations complete
- ✅ Player configs (Human vs Apocalyptron)

### 3. **HTML con Editor JSON** 🎨

**File:** `src/webgui/game_with_json_editor.html` (500+ righe)

Features:
- ✅ **Toggle Mode**: Mock vs Live
- ✅ **JSON Editor**: Show/Hide con syntax highlighting (Prism.js)
- ✅ **Format Button**: Auto-formatta JSON
- ✅ **Validate Button**: Verifica validità
- ✅ **Apply Button**: Applica modifiche → GUI aggiorna!
- ✅ **Status Indicator**: Valid/Invalid real-time
- ✅ **JSON Preview**: Syntax-highlighted read-only
- ✅ **Editable Textarea**: Modifica JSON direttamente

---

## 🎨 Come Funziona

### Architettura JSON-Driven

```
┌─────────────────────────────────────────────┐
│  JSON Game Data (Unico Punto di Verità)     │
│  ─────────────────────────────────────      │
│  • positions[ply]  → Board display          │
│  • valid_by_ply[ply] → Valid indicators     │
│  • opening_by_ply[ply] → Hints             │
│  • ai_stats_by_ply[ply] → AI panel         │
│  • players → Header info                    │
│  • status.clock → Clocks                    │
└─────────────────┬───────────────────────────┘
                  │
                  │ Reactive Updates
                  ▼
┌─────────────────────────────────────────────┐
│  JavaScript render()                        │
│  ─────────────────────────────────────      │
│  1. Read gameData                           │
│  2. Update board grid                       │
│  3. Update score panels                     │
│  4. Update AI stats                         │
│  5. Update openings                         │
│  6. Update history                          │
└─────────────────────────────────────────────┘
```

### Flusso Modifica JSON

```
User edits JSON in editor
    ↓
Click "Apply Changes"
    ↓
JavaScript validates JSON
    ↓
If valid:
  ├─ Update gameData
  ├─ Update embedded <script>
  ├─ Call render()
  └─ GUI refreshes!
```

---

## 📊 JSON Structure Mapping

### Board Display

```json
"positions": [
  "...........................WB......BW...........................",
  //                         ^D4=W   ^E4=B
]
```

**Maps to:**
- Index 27 (D4) = White piece
- Index 28 (E4) = Black piece
- Render: 64 cells, pieces at correct positions

### Player Info

```json
"players": {
  "black": {
    "name": "Luca Amore",
    "avatar": "LA",
    "type": "human"
  }
}
```

**Maps to:**
- Header left: "Luca Amore"
- Avatar: "LA"
- Type determines if AI calls needed

### AI Stats

```json
"ai_stats_by_ply": [
  null,  // ply 0 (no AI)
  {      // ply 1 (AI move)
    "depth": 8,
    "nodes": 6825,
    "selected_move": "E3"
  }
]
```

**Maps to:**
- AI panel shows stats for current ply
- If null → "Nessun dato AI"
- If object → Format and display

---

## 🔄 Mode Toggle Implementation

### Mock Mode (Default)

```javascript
if (dataMode === 'mock') {
  // Use embedded JSON
  gameData = loadFromEmbeddedScript();
  
  // All interactions stay in JavaScript
  // No Python calls
}
```

### Live Mode (Future)

```javascript
if (dataMode === 'live') {
  // Connect to Python API
  const move = await window.pywebview.api.get_ai_move(
    gameData.positions[ply],
    gameData.status.turn_by_ply[ply],
    gameData.players.white.config
  );
  
  // Apply AI move
  applyMove(move.x, move.y);
}
```

---

## 🎨 Quando Mi Passi il Tuo HTML

Farò queste modifiche minime:

### 1. Aggiungerò Mode Toggle

```html
<div class="chip">
  <label>
    <input type="radio" name="mode" value="mock" checked>
    📋 Mock Data
  </label>
</div>
<div class="chip">
  <label>
    <input type="radio" name="mode" value="live">
    🔌 Live (Python AI)
  </label>
</div>
```

### 2. Aggiungerò JSON Editor Section

```html
<article class="card">
  <div class="json-controls">
    <button id="toggleEditor">👁️ Show JSON Editor</button>
    <button id="format">✨ Format</button>
    <button id="validate">✓ Validate</button>
    <button id="apply">🔄 Apply</button>
  </div>
  
  <!-- Syntax highlighted preview -->
  <pre><code class="language-json" id="jsonPreview"></code></pre>
  
  <!-- Editable textarea -->
  <textarea id="jsonEditor" style="display:none"></textarea>
</article>
```

### 3. Aggiungerò Load da File

```javascript
function loadJsonFromFile() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    const json = JSON.parse(await file.text());
    updateGameData(json);
    render(); // Auto-refresh!
  };
  input.click();
}
```

---

## 💡 Vantaggi di Questo Approccio

### 1. **Data-Driven** ✅
- JSON unico punto di verità
- Facile debug (inspect JSON)
- Facile test (mock JSON files)
- Facile export/import

### 2. **Reactive** ✅
- Modifica JSON → GUI aggiorna
- No manual sync
- Consistent state

### 3. **Testabile** ✅
- Test con JSON fixtures
- No need di backend per UI testing
- Mock data instant

### 4. **Portable** ✅
- JSON può venire da Python
- JSON può venire da file
- JSON può venire da network
- Same format, different sources!

---

## 🚀 Prossimi Passi

### Quando mi passi il tuo HTML:

1. **Analizzo** la struttura esistente
2. **Aggiungo** editor JSON in fondo
3. **Integro** syntax highlighting (Prism.js)
4. **Collego** apply button → render()
5. **Testo** che funzioni
6. **Documento** API Python necessaria

### Poi implemento Python Bridge:

```python
class AIBridge:
    def get_ai_move(self, board_state, turn, player_config):
        # Adapter per Apocalyptron, DivZero, etc.
        # Return: {"move": {"x": 3, "y": 4}, "stats": {...}}
        pass
```

---

## 📋 File Creati

1. ✅ `docs/JSON_SCHEMA_GUIWEB.md` - Schema completo (400 righe)
2. ✅ `docs/architecture/GUIWEB_V2_ARCHITECTURE.md` - Architettura thick client (980 righe)
3. ✅ `src/webgui/mock_game_complete.json` - JSON mock completo (200 righe)
4. ✅ `src/webgui/game_with_json_editor.html` - HTML con editor (500 righe)

**Totale:** 2,080 righe di documentazione e codice!

---

## ✨ Pronto per il Tuo HTML!

Mandami il tuo HTML/JS completo e io:

1. **Integro** editor JSON elegante
2. **Aggiungo** mode toggle (mock/live)  
3. **Collego** tutto reattivamente
4. **Testo** che modificando JSON la GUI aggiorni
5. **Implemento** Python AI bridge minimo

**Sono pronto!** 🚀✨




