# AI Insight Dashboard - Data Science Edition

**Implemented:** 2025-11-02  
**Version:** 5.2.0

## 📊 Overview

Il **Dashboard AI Insight** è una visualizzazione avanzata in tempo reale del processo di thinking dell'AI, progettato per Data Scientists e AI enthusiasts. Combina log dettagliati, grafici interattivi e metriche KPI in un'interfaccia elegante e informativa.

---

## 🎯 Features Principali

### 1. **Pulsante AI Insight Animato** 🧠💡

**Posizione**: Barra inferiore, accanto a "Developer-Insight"

**Stati Animati**:
- **Idle**: Normale, grigio
- **AI Thinking**: 
  - 🔄 Icona ruota (360° ogni 2 sec)
  - ✨ Effetto pulsante (glow blu)
  - 💙 Background illuminato
  - Box-shadow animato
- **Completed**: Stop animazioni, torna normale

**Comportamento**:
- NON si apre automaticamente
- Si apre SOLO quando cliccato dall'utente
- Animazione indica che l'AI sta pensando

---

## 📈 Dashboard Structure

### Layout Verticale (Pannello Slide-in Destro):

```
┌─────────────────────────────────────────────────────┐
│ 🧠 AI Insight - Real-time Reasoning                 │
│ [Clear Logs] [Hide/Show Stats] [Close]              │
├─────────────────────────────────────────────────────┤
│ ╔═ STATISTICS (Compatto & Collapsible) ═══════════╗ │
│ ║ 🤖 FORTRESS ETERNAL • 13:07:42 • Move: C5    [▲]║ │
│ ╠═════════════════════════════════════════════════╣ │
│ ║ Row 1: Primary KPIs                             ║ │
│ ║ ┌──────┬──────┬──────┬──────┐                   ║ │
│ ║ │ Move │ Eval │ Time │Depth │                   ║ │
│ ║ │  C5  │ +18  │247ms │ 10   │                   ║ │
│ ║ │      │      │ ~~~~ │      │  (sparkline)      ║ │
│ ║ └──────┴──────┴──────┴──────┘                   ║ │
│ ╠═════════════════════════════════════════════════╣ │
│ ║ Row 2: Node Statistics (3 sparklines)           ║ │
│ ║ ┌─────────┬─────────┬──────────┐                ║ │
│ ║ │ Nodes   │ Pruned  │Efficiency│                ║ │
│ ║ │ 125.3K  │ 87.2K   │  69.6%   │                ║ │
│ ║ │ ~~~~~~  │ ~~~~~~  │    ◯     │  (circular)    ║ │
│ ║ └─────────┴─────────┴──────────┘                ║ │
│ ╠═════════════════════════════════════════════════╣ │
│ ║ Row 3: Optimization Techniques (Heat Map)       ║ │
│ ║ ┌──────┬──────┬──────┬──────┐                   ║ │
│ ║ │ NULL │ FUT  │ LMR  │M-CUT │                   ║ │
│ ║ │12.5K │ 8.3K │ 24K  │ 3.2K │                   ║ │
│ ║ │▬▬▬▬▬▬│▬▬▬▬ │▬▬▬▬▬▬│▬▬    │  (bars)           ║ │
│ ║ └──────┴──────┴──────┴──────┘                   ║ │
│ ╠═════════════════════════════════════════════════╣ │
│ ║ Row 4: Advanced Metrics                         ║ │
│ ║ ┌──────┬──────┬──────┬──────┐                   ║ │
│ ║ │ NPS  │Iters │Aspir.│TT Hit│                   ║ │
│ ║ │ 507K │  10  │ 90%  │ 2.4K │                   ║ │
│ ║ │ ~~~~ │ ▆▇█  │  ◯   │      │  (charts)         ║ │
│ ║ └──────┴──────┴──────┴──────┘                   ║ │
│ ╠═════════════════════════════════════════════════╣ │
│ ║ ⚙️  AI Configuration                             ║ │
│ ║ ┌─────────────────────────────────────────────┐ ║ │
│ ║ │ Impenetrable Stability | Depth 10 | Focus:  │ ║ │
│ ║ │ Defensive Dominance                         │ ║ │
│ ║ └─────────────────────────────────────────────┘ ║ │
│ ║ Active Optimizations:                           ║ │
│ ║ ☑ Null Move Pruning      ☑ Aspiration Windows  ║ │
│ ║ ☑ Futility Pruning       ☑ Iterative Deepening ║ │
│ ║ ☑ Late Move Reduction    ☐ (inactive)          ║ │
│ ║ ☑ Multi-Cut Pruning                            ║ │
│ ╠═════════════════════════════════════════════════╣ │
│ ║ 📊 Iterative Deepening Timeline                 ║ │
│ ║ ├ D1  │ 12.3ms │ 1.2K nodes  │ ✓                ║ │
│ ║ ├ D2  │ 23.1ms │ 3.8K nodes  │ ✓                ║ │
│ ║ ├ D3  │ 45.2ms │ 12.5K nodes │ ✓                ║ │
│ ║ ├ ... (fino a D10)                              ║ │
│ ╚═════════════════════════════════════════════════╝ │
├─────────────────────────────────────────────────────┤
│ ╔═ REASONING LOGS (Real-time) ═══════════════════╗ │
│ ║ [13:07:42.123] 🎯 Starting search...           ║ │
│ ║ [13:07:42.125] ⚡ Depth 1/10...                 ║ │
│ ║ [13:07:42.130] 📍 Move C5 → +15...              ║ │
│ ║ [13:07:42.140] ✓ Depth 1 complete...           ║ │
│ ╚═════════════════════════════════════════════════╝ │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Visualizations Implemented

### **Sparklines** (Mini Trend Charts)
1. **Time Sparkline** (blue #63b3ed)
   - Shows time progression across iterations
   - Identifies slow/fast depths
   
2. **Nodes Sparkline** (green #34d399)
   - Node exploration growth
   - Exponential growth visualization
   
3. **Pruned Sparkline** (purple #a78bfa)
   - Pruning effectiveness per iteration
   - Shows optimization impact
   
4. **NPS Sparkline** (gold #fbbf24)
   - Nodes/second performance
   - Processing speed trends

### **Circular Progress Charts**
1. **Pruning Efficiency** (large, 60px)
   - Green gradient (#10b981 → #34d399)
   - Glow effect
   - % of nodes pruned
   
2. **Aspiration Success** (small, 40px)
   - Blue (#63b3ed)
   - Success rate %
   
3. **TT Hit Rate** (removed - now absolute hits)
   - Replaced with absolute hit count
   - More readable for high values

### **Heat Map Bars** (Optimization Techniques)
- **Normalized bars**: All relative to max optimization
- **Purple gradient** (#6366f1 → #8b5cf6)
- **Glow effects** on hover
- Shows: NULL, FUT, LMR, M-CUT

### **Micro Bar Chart** (Iterations)
- Small bars showing time distribution
- Blue (#63b3ed) bars
- Height proportional to iteration time

### **Timeline** (Iterative Deepening)
- Chronological list of all iterations
- Shows: Depth, Time, Nodes, Aspiration badge
- Hover effect with slide animation
- Color-coded badges: ✓ (green) / ✗ (red)

---

## 🎨 Design Elements

### **Color Palette**
| Color | Hex | Usage |
|-------|-----|-------|
| Primary Blue | #63b3ed | Headers, primary metrics |
| Success Green | #10b981, #34d399 | Efficiency, success states |
| Purple | #6366f1, #8b5cf6, #a78bfa | Optimizations, advanced metrics |
| Gold | #fbbf24 | Highlights, NPS |
| Red | #f87171 | Failures, negative values |

### **Effects**
1. **Shimmer**: Light sweep on hover
2. **Lift**: Card elevation with shadow
3. **Glow**: SVG drop-shadow on charts
4. **Smooth Transitions**: cubic-bezier(0.4, 0, 0.2, 1)
5. **Color Transitions**: Evaluation values (green/red)

### **Typography**
- **Labels**: 9-10px, uppercase, wide letter-spacing
- **Values**: Courier New, monospace, bold
- **Tooltips**: 11-12px, descriptive (English)

---

## 📋 Metrics Reference

### **Primary KPIs**
| Metric | Format | Tooltip |
|--------|--------|---------|
| Move | C5 | Selected move by AI |
| Evaluation | +18 | Position evaluation (±) |
| Search Time | 247ms | Total search duration |
| Depth | 10/10 | Reached / target depth |

### **Node Statistics**
| Metric | Format | Tooltip | Chart |
|--------|--------|---------|-------|
| Nodes Searched | 125.3K | Total explored | Sparkline (green) |
| Nodes Pruned | 87.2K | Skipped via opts | Sparkline (purple) |
| Pruning Efficiency | 69.6% | % pruned | Circular (green) |

### **Optimization Techniques**
| Technique | Tooltip | Chart |
|-----------|---------|-------|
| NULL | Null move cutoffs | Bar (normalized) |
| FUT | Futility cuts | Bar (normalized) |
| LMR | Late move reductions | Bar (normalized) |
| M-CUT | Multi-cut prunes | Bar (normalized) |

All bars normalized to maximum optimization value for comparison.

### **Advanced Metrics**
| Metric | Format | Tooltip | Chart |
|--------|--------|---------|-------|
| NPS | 507K/s | Search speed | Sparkline (gold) |
| Iterations | 10 | Depth completions | Micro bars (blue) |
| Aspiration | 90% | Window success rate | Circular (blue) |
| TT Hits | 2.4K | Cache hits (absolute) | Text + size |

**Note**: TT changed from % to absolute hits for better readability with high values.

---

## ⚙️ AI Configuration Section

### **Player Description**
Shows brief player strategy from metadata:
- Name
- Depth configuration
- Special focus
- Key features

Example:
```
Impenetrable Stability | Depth 10 | Focus: Defensive Dominance
```

### **Active Optimizations Checklist**
Real-time detection of enabled optimizations:

| Optimization | Detection Logic |
|--------------|-----------------|
| ☑ Null Move Pruning | `null_move_cuts > 0` |
| ☑ Futility Pruning | `futility_cuts > 0` |
| ☑ Late Move Reduction | `lmr_reductions > 0` |
| ☑ Multi-Cut Pruning | `multi_cut_prunes > 0` |
| ☑ Aspiration Windows | `aspiration_hits > 0 OR fails > 0` |
| ☑ Iterative Deepening | `iterations > 1` |

**Visual States**:
- ☑ (green #34d399) = Active
- ☐ (gray) = Inactive

---

## 📊 Iterative Deepening Timeline

**Format**:
```
D1  │ 12.3ms │ 1.2K nodes  │ ✓
D2  │ 23.1ms │ 3.8K nodes  │ ✓
D3  │ 45.2ms │ 12.5K nodes │ ✗  (re-search)
...
D10 │ 89.4ms │ 125.3K nodes│ ✓
```

**Columns**:
1. Depth (D1, D2, ...)
2. Iteration time (ms)
3. Cumulative nodes
4. Aspiration success (✓/✗)

**Interactive**:
- Hover: Slide right + background highlight
- Color-coded badges

---

## 🎨 Visual Effects

### **Card Hover Effects**
```css
/* Shimmer effect */
.stat-card-graph::before {
  background: linear-gradient(90deg, transparent, rgba(99,179,237,0.1), transparent);
  transition: left 0.5s ease;
}

/* On hover: light sweeps across */
.stat-card-graph:hover::before {
  left: 100%;
}
```

### **Circular Progress Animation**
```javascript
// Smooth arc drawing with easing
circle.style.transition = 'stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
```

### **Color Coding**
- **Evaluation Values**: 
  - Positive (≥0): Green #34d399
  - Negative (<0): Red #ff6b6b
- **Aspiration Badges**:
  - Success ✓: Green background
  - Failure ✗: Red background

---

## 🔧 Technical Implementation

### **Backend** (`websocket_observer.py`)

#### Data Tracking
```python
self.depth_history = []  # Track all iterations
self.move_evaluations = []  # Track move evals

# Per iteration:
{
  "depth": 1,
  "time": 12.3,
  "nodes": 1250,
  "pruned": 340,
  "nps": 101626,
  "value": +15,
  "aspiration_success": True
}
```

#### Statistics Extraction
```python
# Extract from nested objects
null_move_stats = statistics.get("null_move", {})
null_move_cuts = null_move_stats.get("cutoffs", 0)

# Same for: futility, lmr, multi_cut
```

### **Frontend** (`game_websocket.html`)

#### Sparkline Rendering
```javascript
function drawSparkline(svgId, dataPoints, color){
  // Normalize to SVG viewport
  // Draw polyline with smooth curves
  // Color-coded by metric type
}
```

#### Circular Progress
```javascript
function updateCircularProgress(elementId, percentage, circumference){
  const offset = circumference - (percentage / 100 * circumference);
  circle.style.strokeDashoffset = offset;
}
```

#### Optimization Bars (Normalized)
```javascript
const maxOpt = Math.max(...allOptimizations);
barWidth = (value / maxOpt) * 100 + '%';
```

---

## 📱 User Interactions

### **Toggle Controls**

1. **▲ / ▼** (In statistics header)
   - Collapses/expands detailed statistics
   - Keeps header visible (player + move)
   - Smooth height transition

2. **Hide Stats / Show Stats** (Main header)
   - Hides/shows entire statistics section
   - Icon changes (up/down arrow)
   - Text updates dynamically

3. **Clear Logs**
   - Clears reasoning logs
   - Keeps statistics

4. **Close**
   - Closes entire AI Insight panel
   - Stops any updates

### **Auto-Behaviors**

- **Statistics populate automatically** after AI move
- **Panel stays closed** unless user opens
- **Sparklines auto-update** with new data
- **Circular charts animate** on data change
- **Timeline appends** new iterations

---

## 🎯 Use Cases

### **For Developers**
- Debug search algorithms
- Verify optimization effectiveness
- Analyze performance bottlenecks
- Compare different AI configurations

### **For Data Scientists**
- Analyze search patterns
- Statistical trend analysis
- Performance benchmarking
- Algorithm efficiency studies

### **For AI Enthusiasts**
- Understand AI decision-making
- Learn optimization techniques
- Visualize search complexity
- Compare player strategies

### **For Educators**
- Teaching minimax algorithms
- Demonstrating alpha-beta pruning
- Visualizing iterative deepening
- Showing aspiration windows

---

## 📊 Sample Data Interpretation

### **High Pruning Efficiency (>70%)**
```
Nodes: 150K | Pruned: 105K | Efficiency: 70%
```
✅ Excellent optimization  
✅ Alpha-beta pruning working well  
✅ Move ordering effective

### **Low Aspiration Success (<50%)**
```
Aspiration: 45% | 5 hits / 6 fails
```
⚠️ Unstable position evaluations  
⚠️ Consider wider windows  
⚠️ Or disable aspiration

### **High NPS (>500K)**
```
NPS: 847K/s
```
✅ Fast evaluation function  
✅ Efficient implementation  
✅ Good cache locality

### **Optimization Distribution**
```
NULL: 25K | FUT: 18K | LMR: 42K | M-CUT: 8K
```
📈 LMR most effective (42K reductions)  
📈 Null move strong (25K cuts)  
📉 Multi-cut less used (8K)

---

## 🚀 Quick Start

### 1. Start Server
```bash
./reversi42
# or
python3 -m src.webgui.server.backend_server
```

### 2. Open Browser
```
http://localhost:8000
```

### 3. Play a Move
- AI starts thinking
- 🔄 AI Insight button **pulses and rotates**

### 4. Open Panel (Optional)
- Click "AI Insight" button
- See real-time logs + statistics

### 5. Explore Data
- Hover over metrics for tooltips
- Observe sparklines and charts
- Check optimization checkboxes
- Read iteration timeline

---

## 🎨 Customization

### **Colors** (in CSS)
```css
/* Primary metrics */
--color-primary: #63b3ed;
--color-success: #34d399;
--color-warning: #fbbf24;
--color-error: #f87171;
--color-accent: #a78bfa;
```

### **Chart Sizes**
```css
.stat-sparkline { height: 18px; }      /* Sparklines */
.circular-progress { width: 60px; }    /* Large circular */
.circular-progress-sm { width: 40px; } /* Small circular */
.stat-micro-chart { height: 24px; }    /* Micro bars */
```

---

## 🐛 Troubleshooting

### **Grafici non appaiono**
- Verifica che `depth_history` non sia vuoto
- Controlla console browser (F12)
- Verifica che iterative deepening sia attivo

### **Valori sempre zero**
- Player potrebbe non usare quell'ottimizzazione
- Verifica configurazione player (checkbox section)
- Controlla log backend: `/tmp/backend_detailed.log`

### **Sparklines piatte**
- Normale se tutti i valori uguali
- Significa performance consistente
- Non è un errore

### **TT Hits molto bassi**
- Normale in opening (poche posizioni ripetute)
- Aumenta in endgame
- Dipende da game phase

---

## 📈 Performance

### **Overhead**
- **Backend**: ~2-3% CPU overhead
- **Frontend**: Trascurabile (<1%)
- **Network**: ~2-5KB per mossa
- **Rendering**: <10ms per dashboard update

### **Optimization**
- Sparklines: Canvas-free (SVG only)
- Updates: Batched in single frame
- Animations: GPU-accelerated CSS
- No external libraries (vanilla JS)

---

## 🔮 Future Enhancements

Possible extensions:
- [ ] 3D visualization of search tree
- [ ] Live comparison between 2 AIs
- [ ] Export charts as PNG/SVG
- [ ] Historical trend analysis (multi-game)
- [ ] ML-based anomaly detection
- [ ] Predictive performance metrics
- [ ] Custom chart configurations

---

## 📝 Changelog

### v5.2.0 (2025-11-02)
- ✨ Full dashboard with 7 chart types
- ✨ Sparklines for Time, Nodes, Pruned, NPS
- ✨ Circular progress charts (3x)
- ✨ Optimization heat map bars
- ✨ Iteration timeline with badges
- ✨ AI configuration section
- ✨ Active optimizations checklist
- ✨ Player description display
- ✨ TT changed from % to absolute hits
- ✨ Advanced hover effects & animations
- ✨ Tooltips in English
- ✨ Compact header design

---

**Author**: Luca Amore  
**License**: GPL-3.0-or-later  
**Built for**: Data Scientists, AI Researchers, Reversi Enthusiasts


