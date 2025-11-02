/**
 * Reversi42 - AI Statistics Dashboard
 * 
 * Comprehensive AI performance analytics and visualization
 * Displays detailed search statistics, pruning efficiency, and performance metrics
 * 
 * Features:
 *  - Move evaluation metrics
 *  - Search performance statistics
 *  - Pruning efficiency visualization
 *  - Iterative deepening timeline
 *  - Optimization indicators
 *  - Interactive charts (sparklines, circular progress, bar charts)
 */

// Initialize AI Statistics Dashboard after template is loaded
function initAIStatistics() {
  const statsDashboard = document.getElementById('aiStatsDashboard');
  const statsCollapsibleBody = document.getElementById('statsCollapsibleBody');
  const toggleStatsCollapseBtn = document.getElementById('toggleStatsCollapse');
  const toggleAiStatsBtn = document.getElementById('toggleAiStatsBtn');
  const toggleAiStatsText = document.getElementById('toggleAiStatsText');
  const toggleAiStatsIcon = document.getElementById('toggleAiStatsIcon');

let statsCollapsed = false;
let statsVisible = false;

// Toggle collapse/expand statistics (▲/▼ button in stats header)
if(toggleStatsCollapseBtn){
  toggleStatsCollapseBtn.addEventListener('click', () => {
    statsCollapsed = !statsCollapsed;
    if(statsCollapsibleBody){
      if(statsCollapsed){
        statsCollapsibleBody.classList.add('collapsed');
        toggleStatsCollapseBtn.textContent = '▼';
        toggleStatsCollapseBtn.title = 'Show statistics';
      } else {
        statsCollapsibleBody.classList.remove('collapsed');
        toggleStatsCollapseBtn.textContent = '▲';
        toggleStatsCollapseBtn.title = 'Hide statistics';
      }
    }
  });
}

// Toggle Hide/Show statistics section (button in main header)
if(toggleAiStatsBtn){
  toggleAiStatsBtn.addEventListener('click', () => {
    statsVisible = !statsVisible;
    if(statsDashboard){
      if(statsVisible){
        // Show stats
        statsDashboard.style.display = 'block';
        if(toggleAiStatsText) toggleAiStatsText.textContent = 'Hide Stats';
        if(toggleAiStatsIcon){
          toggleAiStatsIcon.innerHTML = '<svg viewBox="0 0 24 24"><path d="M18 15l-6-6-6 6"/></svg>';
        }
      } else {
        // Hide stats
        statsDashboard.style.display = 'none';
        if(toggleAiStatsText) toggleAiStatsText.textContent = 'Show Stats';
        if(toggleAiStatsIcon){
          toggleAiStatsIcon.innerHTML = '<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>';
        }
      }
    }
  });
}

// Show AI Statistics Dashboard (inside AI Insight panel)
function showAIStatisticsDashboard(stats){
  if(!statsDashboard) return;
  
  console.log('📊 Showing AI Statistics Dashboard:', stats);
  
  // NO auto-apertura! Il pannello si apre SOLO quando l'utente clicca il bottone
  // Ma popola comunque i dati per quando verrà aperto
  
  // Reset collapsed state (show stats expanded when new data arrives)
  statsCollapsed = false;
  if(statsCollapsibleBody){
    statsCollapsibleBody.classList.remove('collapsed');
  }
  if(toggleStatsCollapseBtn){
    toggleStatsCollapseBtn.textContent = '▲';
    toggleStatsCollapseBtn.title = 'Hide statistics';
  }
  
  // Player info
  const playerName = stats.player_name || 'AI Player';
  document.getElementById('statsPlayerName').textContent = playerName;
  document.getElementById('statsPlayerAvatar').textContent = playerName.substring(0, 2).toUpperCase();
  document.getElementById('statsTimestamp').textContent = stats.timestamp;
  
  // Move badge (prominent display in header)
  const moveBadge = document.getElementById('statMoveBadge');
  if(moveBadge){
    moveBadge.textContent = stats.best_move || '--';
    const evalValue = stats.evaluation !== undefined ? stats.evaluation : null;
    if(evalValue !== null){
      moveBadge.style.color = evalValue >= 0 ? '#34d399' : '#ff6b6b';
      moveBadge.title = `Evaluation: ${evalValue >= 0 ? '+' : ''}${evalValue}`;
    }
  }
  
  // Move info (in body)
  const moveElem = document.getElementById('statMove');
  if(moveElem) moveElem.textContent = stats.best_move || '--';
  
  const evalElem = document.getElementById('statEval');
  if(evalElem && stats.evaluation !== undefined){
    const evalText = (stats.evaluation >= 0 ? '+' : '') + stats.evaluation;
    evalElem.textContent = evalText;
    evalElem.style.color = stats.evaluation >= 0 ? '#34d399' : '#ff6b6b';
  }
  
  // Performance metrics
  const timeElem = document.getElementById('statTime');
  if(timeElem) timeElem.textContent = stats.total_time_ms ? stats.total_time_ms.toFixed(0) + 'ms' : '--';
  
  const depthElem = document.getElementById('statDepth');
  if(depthElem) depthElem.textContent = stats.depth_reached ? stats.depth_reached + '' : '--';
  
  const depthTargetElem = document.getElementById('statDepthTarget');
  if(depthTargetElem && stats.target_depth){
    depthTargetElem.textContent = `/ ${stats.target_depth}`;
  }
  
  // Node statistics
  const nodesElem = document.getElementById('statNodesSearched');
  if(nodesElem) nodesElem.textContent = stats.nodes_searched ? 
    (stats.nodes_searched >= 1000 ? (stats.nodes_searched/1000).toFixed(1) + 'K' : stats.nodes_searched) : '--';
  
  const prunedElem = document.getElementById('statNodesPruned');
  if(prunedElem) prunedElem.textContent = stats.nodes_pruned ? 
    (stats.nodes_pruned >= 1000 ? (stats.nodes_pruned/1000).toFixed(1) + 'K' : stats.nodes_pruned) : '--';
  
  const effElem = document.getElementById('statPruningEff');
  if(effElem) effElem.textContent = stats.pruning_efficiency !== undefined ? 
    stats.pruning_efficiency.toFixed(1) + '%' : '--%';
  
  // Pruning efficiency bar (animated)
  const pruningBar = document.getElementById('pruningBar');
  if(pruningBar && stats.pruning_efficiency !== undefined){
    setTimeout(() => {
      pruningBar.style.width = Math.min(100, stats.pruning_efficiency) + '%';
    }, 100);
  }
  
  // Optimizations (compact display)
  const nullElem = document.getElementById('statNullMove');
  if(nullElem) nullElem.textContent = formatCompactNumber(stats.null_move_cuts);
  
  const futElem = document.getElementById('statFutility');
  if(futElem) futElem.textContent = formatCompactNumber(stats.futility_cuts);
  
  const lmrElem = document.getElementById('statLMR');
  if(lmrElem) lmrElem.textContent = formatCompactNumber(stats.lmr_reductions);
  
  const mcElem = document.getElementById('statMultiCut');
  if(mcElem) mcElem.textContent = formatCompactNumber(stats.multi_cut_prunes);
  
  const parallelElem = document.getElementById('statParallel');
  if(parallelElem){
    if(stats.parallel_threads !== undefined && stats.parallel_threads > 0){
      parallelElem.textContent = stats.parallel_threads + ' threads';
    } else if(stats.parallel_tasks !== undefined){
      parallelElem.textContent = formatCompactNumber(stats.parallel_tasks);
    } else {
      parallelElem.textContent = '--';
    }
  }
  
  const bookingElem = document.getElementById('statBooking');
  if(bookingElem){
    if(stats.book_hits !== undefined){
      bookingElem.textContent = formatCompactNumber(stats.book_hits);
    } else if(stats.book_enabled){
      bookingElem.textContent = 'Active';
    } else {
      bookingElem.textContent = '--';
    }
  }
  
  // AI Configuration Description
  const aiDescElem = document.getElementById('aiConfigDescription');
  if(aiDescElem){
    if(stats.player_description){
      aiDescElem.textContent = stats.player_description;
    } else if(stats.player_name){
      aiDescElem.textContent = `${stats.player_name} - Advanced AI engine with multi-threaded alpha-beta search, iterative deepening, and extensive pruning optimizations.`;
    }
    // Se non c'è nessuna descrizione, mantiene il testo di default dall'HTML
  }
  
  // Update optimization checkboxes based on active features
  updateOptCheckbox('optNull', stats.null_move_enabled || stats.null_move_cuts > 0);
  updateOptCheckbox('optFutility', stats.futility_enabled || stats.futility_cuts > 0);
  updateOptCheckbox('optLMR', stats.lmr_enabled || stats.lmr_reductions > 0);
  updateOptCheckbox('optMultiCut', stats.multi_cut_enabled || stats.multi_cut_prunes > 0);
  updateOptCheckbox('optAspiration', stats.aspiration_enabled || stats.aspiration_success_rate > 0);
  updateOptCheckbox('optTT', stats.tt_enabled || stats.tt_hits > 0);
  updateOptCheckbox('optKiller', stats.killer_enabled || false);
  updateOptCheckbox('optHistory', stats.history_enabled || false);
  updateOptCheckbox('optParallel', stats.parallel_enabled || stats.parallel_threads > 0 || stats.parallel_tasks > 0);
  updateOptCheckbox('optBook', stats.book_enabled || stats.book_hits > 0);
  
  // NPS (nodes per second)
  const npsElem = document.getElementById('statNPS');
  if(npsElem) npsElem.textContent = stats.nodes_per_second ? 
    (stats.nodes_per_second / 1000).toFixed(0) + 'K' : '--';
  
  // Iterations
  const iterElem = document.getElementById('statIterations');
  if(iterElem) iterElem.textContent = stats.iterations_completed || '--';
  
  // Aspiration windows
  const aspElem = document.getElementById('statAspirationRate');
  if(aspElem) aspElem.textContent = stats.aspiration_success_rate !== undefined ? 
    stats.aspiration_success_rate.toFixed(0) + '%' : '--%';
  
  // Transposition table - show absolute hits count
  const ttElem = document.getElementById('statTTRate');
  const ttPercentElem = document.getElementById('statTTPercent');
  if(ttElem){
    if(stats.tt_hits !== undefined){
      ttElem.textContent = formatCompactNumber(stats.tt_hits);
    } else {
      ttElem.textContent = '--';
    }
  }
  // Show hit rate as sublabel
  if(ttPercentElem){
    if(stats.tt_hit_rate !== undefined){
      ttPercentElem.textContent = stats.tt_hit_rate.toFixed(0) + '% hit rate';
    } else {
      ttPercentElem.textContent = '-- hit rate';
    }
  }
  
  // ==================== ADVANCED CHARTS ====================
  
  // Circular progress: Pruning Efficiency
  updateCircularProgress('circularPruningFill', stats.pruning_efficiency || 0, 157);
  
  // Circular progress: Aspiration Rate
  updateCircularProgress('circularAspirationFill', stats.aspiration_success_rate || 0, 100);
  
  // Sparklines for depth history
  if(stats.depth_history && stats.depth_history.length > 0){
    drawSparkline('sparklineTime', stats.depth_history.map(d => d.time), '#8b5cf6');
    drawSparkline('sparklineNodes', stats.depth_history.map(d => d.nodes), '#06b6d4');
    drawSparkline('sparklinePruned', stats.depth_history.map(d => d.pruned || 0), '#a78bfa');
    drawSparkline('sparklineNPS', stats.depth_history.map(d => d.nps || 0), '#f59e0b');
    drawSparkline('sparklineTT', stats.depth_history.map(d => d.tt_hits || 0), '#a78bfa');
  }
  
  // Optimization bars (normalized to max value)
  const parallelValue = stats.parallel_threads || stats.parallel_tasks || 0;
  const bookValue = stats.book_hits || 0;
  const optValues = [
    stats.null_move_cuts || 0,
    stats.futility_cuts || 0,
    stats.lmr_reductions || 0,
    stats.multi_cut_prunes || 0,
    bookValue,
    parallelValue
  ];
  const maxOpt = Math.max(...optValues, 1);
  updateOptimizationBar('barNull', (stats.null_move_cuts || 0) / maxOpt * 100);
  updateOptimizationBar('barFut', (stats.futility_cuts || 0) / maxOpt * 100);
  updateOptimizationBar('barLMR', (stats.lmr_reductions || 0) / maxOpt * 100);
  updateOptimizationBar('barMC', (stats.multi_cut_prunes || 0) / maxOpt * 100);
  updateOptimizationBar('barBook', bookValue / maxOpt * 100);
  updateOptimizationBar('barParallel', parallelValue / maxOpt * 100);
  
  // Iteration timeline
  buildIterationTimeline(stats.depth_history || []);
  
  // Iteration micro chart
  if(stats.depth_history && stats.depth_history.length > 1){
    drawMicroBarChart('chartIterations', stats.depth_history.map(d => d.time));
  }
  
  // Show stats section
  statsDashboard.style.display = 'block';
  statsVisible = true;
  
  // Show and update "Hide Stats" button in header
  if(toggleAiStatsBtn){
    toggleAiStatsBtn.style.display = 'inline-flex';
    if(toggleAiStatsText) toggleAiStatsText.textContent = 'Hide Stats';
    if(toggleAiStatsIcon){
      toggleAiStatsIcon.innerHTML = '<svg viewBox="0 0 24 24"><path d="M18 15l-6-6-6 6"/></svg>';
    }
  }
}

// ==================== CHART RENDERING FUNCTIONS ====================

// Update circular progress chart
function updateCircularProgress(elementId, percentage, circumference){
  const circle = document.getElementById(elementId);
  if(!circle) return;
  const offset = circumference - (percentage / 100 * circumference);
  circle.style.strokeDashoffset = offset;
  circle.style.transition = 'stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
}

// Draw sparkline chart
function drawSparkline(svgId, dataPoints, color){
  const svg = document.getElementById(svgId);
  if(!svg || !dataPoints || dataPoints.length === 0) return;
  
  svg.innerHTML = '';
  const width = svg.clientWidth || 100;
  const height = 20;
  const max = Math.max(...dataPoints, 1);
  const min = Math.min(...dataPoints, 0);
  const range = max - min || 1;
  
  // Create path
  const points = dataPoints.map((val, idx) => {
    const x = (idx / (dataPoints.length - 1)) * width;
    const y = height - ((val - min) / range * height);
    return `${x},${y}`;
  }).join(' ');
  
  const polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
  polyline.setAttribute('points', points);
  polyline.setAttribute('fill', 'none');
  polyline.setAttribute('stroke', color);
  polyline.setAttribute('stroke-width', '2');
  polyline.setAttribute('opacity', '0.8');
  
  svg.appendChild(polyline);
}

// Update optimization bar
function updateOptimizationBar(barId, percentage){
  const bar = document.getElementById(barId);
  if(!bar) return;
  setTimeout(() => {
    bar.style.width = Math.min(100, percentage) + '%';
  }, 100);
}

/* ========================================
   CHART RENDERING - Visualization Helpers
   ======================================== */
function drawMicroBarChart(svgId, dataPoints){
  const svg = document.getElementById(svgId);
  if(!svg || !dataPoints || dataPoints.length === 0) return;
  
  svg.innerHTML = '';
  const width = svg.clientWidth || 100;
  const height = 24;
  const barWidth = (width / dataPoints.length) - 1;
  const max = Math.max(...dataPoints, 1);
  
  dataPoints.forEach((val, idx) => {
    const barHeight = (val / max) * height;
    const x = idx * (barWidth + 1);
    const y = height - barHeight;
    
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', y);
    rect.setAttribute('width', barWidth);
    rect.setAttribute('height', barHeight);
    rect.setAttribute('fill', '#63b3ed');
    rect.setAttribute('opacity', '0.7');
    rect.setAttribute('rx', '1');
    
    svg.appendChild(rect);
  });
}

// Build iteration timeline
function buildIterationTimeline(depthHistory){
  const timeline = document.getElementById('iterationTimeline');
  if(!timeline) return;
  
  if(!depthHistory || depthHistory.length === 0){
    timeline.innerHTML = '<div style="text-align:center;color:rgba(255,255,255,0.3);font-size:11px;padding:8px">No iteration data</div>';
    return;
  }
  
  timeline.innerHTML = '';
  depthHistory.forEach((iter, idx) => {
    const item = document.createElement('div');
    item.className = 'iteration-item';
    
    const depthSpan = document.createElement('span');
    depthSpan.className = 'iteration-depth';
    depthSpan.textContent = `D${iter.depth}`;
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'iteration-time';
    timeSpan.textContent = `${iter.time.toFixed(1)}ms`;
    
    const nodesSpan = document.createElement('span');
    nodesSpan.className = 'iteration-nodes';
    nodesSpan.textContent = formatCompactNumber(iter.nodes) + ' nodes';
    
    const badge = document.createElement('span');
    badge.className = iter.aspiration_success ? 'iteration-badge' : 'iteration-badge iteration-badge-fail';
    badge.textContent = iter.aspiration_success ? '✓' : '✗';
    badge.title = iter.aspiration_success 
      ? 'Aspiration Window Success: Search completed within expected score range, no re-search needed' 
      : 'Aspiration Window Failed: Score fell outside expected range, had to re-search with wider window';
    badge.style.cursor = 'help';
    
    item.appendChild(depthSpan);
    item.appendChild(timeSpan);
    item.appendChild(nodesSpan);
    item.appendChild(badge);
    
    timeline.appendChild(item);
  });
}

/* ========================================
   UTILITY FUNCTIONS - Global Helpers
   ======================================== */
function formatCompactNumber(num){
  if(num === undefined || num === null) return '0';
  if(num >= 1000000) return (num/1000000).toFixed(1) + 'M';
  if(num >= 1000) return (num/1000).toFixed(1) + 'K';
  return num.toString();
}

/* ========================================
   DEVELOPER TOOLS - UI Helper Functions
   ======================================== */
function updateOptCheckbox(checkboxId, isActive){
  const checkbox = document.getElementById(checkboxId);
  if(!checkbox) return;
  checkbox.textContent = isActive ? '☑' : '☐';
  checkbox.style.color = isActive ? '#10b981' : 'rgba(255,255,255,0.3)';
}

// Toggle section visibility (for collapsible sections)
function toggleSection(contentId, buttonId){
  const content = document.getElementById(contentId);
  const button = document.getElementById(buttonId);
  if(!content || !button) return;
  
  const isVisible = content.style.display !== 'none';
  content.style.display = isVisible ? 'none' : 'block';
  button.textContent = isVisible ? 'Show' : 'Hide';
  button.classList.toggle('collapsed', isVisible);
}

/* ========================================
   GLOBAL EXPORTS
   ======================================== */
window.showAIStatisticsDashboard = showAIStatisticsDashboard;
window.formatCompactNumber = formatCompactNumber;
window.toggleSection = toggleSection;
}

// Will be called by loadTemplates() in game.js after templates are loaded
