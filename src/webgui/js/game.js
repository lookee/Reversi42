/**
 * Reversi42 - Main Game Logic
 * 
 * Core game engine and UI management for Reversi42 WebGUI
 * Handles WebSocket communication, board rendering, move validation,
 * AI integration, and all game state management.
 * 
 * Features:
 *  - WebSocket real-time communication with backend
 *  - Dynamic board rendering with animations
 *  - AI move handling and statistics
 *  - Opening book integration
 *  - Move history management (compact & XOT formats)
 *  - Player management (Human/AI)
 *  - Undo/Redo functionality
 *  - Dynamic template loading
 * 
 * Dependencies:
 *  - Tailwind CSS (CDN)
 *  - CodeMirror (optional, for JSON editing)
 *  - HTML templates (templates/ directory)
 */
'use strict';

/* ========================================
   TEMPLATE LOADER - Load HTML Components
   ======================================== */
async function loadTemplates() {
  const templates = [
    { url: 'templates/players-modal.html', container: 'playersModalContainer' },
    { url: 'templates/ai-insight-panel.html', container: 'aiInsightContainer' },
    { url: 'templates/dev-tools-panel.html', container: 'devToolsContainer' }
  ];
  
  for (const template of templates) {
    try {
      const response = await fetch(template.url);
      const html = await response.text();
      const container = document.getElementById(template.container);
      if (container) {
        container.innerHTML = html;
      }
    } catch (error) {
      console.error(`Failed to load template ${template.url}:`, error);
    }
  }
  
  // Initialize template-dependent scripts after loading
  if (typeof initDevTools === 'function') {
    initDevTools();
  }
  if (typeof initAIInsight === 'function') {
    initAIInsight();
  }
  if (typeof initAIStatistics === 'function') {
    initAIStatistics();
  }
}

/* ========================================
   GLOBAL VARIABLES & CONFIGURATION
   ======================================== */
let data = null;
let ply = 0;
let wsConnection = null;
let gameOverInfo = null; // { winner, black_count, white_count }
let pendingSelectedAI = null; // confirm selected AI after init
let aiAutoPaused = false; // AI auto-play paused
let showOpeningHints = true; // Show opening book hints on board

/* Initial Setup Screen */
let initialSetupComplete = false;
let initialBlackPlayer = 'Human Player'; // Default Black (must match YAML name exactly)
let initialWhitePlayer = 'LIGHTNING STRIKE'; // Default White (must match YAML name exactly - all caps!)
let initialSelectingFor = null; // 'black' or 'white'

/* Version Information */
let gameVersion = '6.1.2'; // Fallback version

/* Player Cache - for avatar lookups */
let playersCache = null;

/* AI Quick Stats - Throttled Updates */
let lastQuickStatsUpdate = 0;
const QUICK_STATS_THROTTLE_MS = 1000; // Update max every 1 second for readability
let pendingQuickStats = null;
let statsUpdateTimer = null;
let statsCurrentlyVisible = false; // Track if stats panel is visible

/* WebSocket configuration */
const WS_URL = 'ws://localhost:8000/ws';
const SESSION_ID = 'default';

/* ========================================
   UTILITY FUNCTIONS - Formatting & Helpers
   ======================================== */
function pretty(obj){ try{ return JSON.stringify(obj, null, 2); }catch(_){ return String(obj); } }
function highlightJson(json){
  const esc = (s)=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  return esc(json)
    .replace(/(&quot;.*?&quot;)(:\s*)/g, '<span class="json-key">$1</span>$2')
    .replace(/&quot;([^\"]|\\\")*&quot;/g, '<span class="json-string">$&</span>')
    .replace(/\b(true|false)\b/g, '<span class="json-boolean">$1</span>')
    .replace(/\b(null)\b/g, '<span class="json-null">$1</span>')
    .replace(/(-?\b\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?\b)/g, '<span class="json-number">$1</span>');
}
function summarizeMessage(direction, payload){
  let p = payload;
  if(typeof p === 'string'){
    try{ p = JSON.parse(p); }catch(_){ /* ignore */ }
  }
  if(p && typeof p === 'object'){
    const t = p.type || p?.data?.type;
    if(t === 'board_update'){
      const last = p?.data?.moves && p.data.moves.length ? p.data.moves[p.data.moves.length-1] : '-';
      const turn = p?.data?.status?.turn_by_ply?.[0] || '-';
      const valid = (p?.data?.valid_by_ply?.[0] || []).length;
      const book = (p?.data?.opening_by_ply || []).length;
      return `turn ${turn} · last ${last} · valid ${valid} · book ${book}`;
    }
    if(t === 'ai_move'){
      const mv = p?.data?.move || '-';
      return `move ${mv}`;
    }
    if(t === 'ai_thinking'){
      return 'thinking…';
    }
    if(t === 'human_move'){
      return `move ${p.move}`;
    }
    if(t === 'init'){
      return `ai=${p.ai_player || ''}`;
    }
    if(t === 'reset_game'){
      return 'reset';
    }
  }
  return `${direction}`;
}
async function copyTextStrict(text){
  try{
    if(navigator.clipboard && navigator.clipboard.writeText){
      await navigator.clipboard.writeText(text);
      return true;
    }
  }catch(_){/* fallthrough */}
  try{
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position='fixed'; ta.style.left='-9999px'; ta.style.top='-9999px';
    document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
    return true;
  }catch(_){ return false; }
}

/* ========================================
   WEBSOCKET - Activity Indicators
   ======================================== */
let wsHighlightTimeout = null;
function highlightWSActivity(){
  const devBtn = document.getElementById('toggleJsonEditor');
  if(!devBtn) return;
  
  // Add the ws-active class
  devBtn.classList.add('ws-active');
  
  // Clear any existing timeout
  if(wsHighlightTimeout){
    clearTimeout(wsHighlightTimeout);
  }
  
  // Remove the class after animation completes (800ms)
  wsHighlightTimeout = setTimeout(() => {
    devBtn.classList.remove('ws-active');
  }, 800);
}

function appendWsMessage(direction, payload){
  const box = document.getElementById('wsTrafficContent');
  if(!box) return;
  const time = new Date().toISOString();
  const item = document.createElement('div'); item.className = 'ws-item';
  const head = document.createElement('div'); head.className = 'ws-head';
  const timeSpan = document.createElement('span'); timeSpan.className = 'ws-time'; timeSpan.textContent = time;

  // Direction badge
  const dirSpan = document.createElement('span');
  dirSpan.className = 'ws-badge ws-dir';
  dirSpan.textContent = direction;
  if(/^\s*→/.test(direction)) dirSpan.classList.add('send');
  if(/^\s*←/.test(direction)) dirSpan.classList.add('recv');

  // Determine command/type and create colored badge
  let payloadObj = payload;
  if(typeof payloadObj === 'string'){
    try{ payloadObj = JSON.parse(payloadObj); }catch(_){ /* noop */ }
  }
  const typeVal = payloadObj && typeof payloadObj === 'object' ? (payloadObj.type || payloadObj?.data?.type || '—') : '—';
  const typeSpan = document.createElement('span');
  typeSpan.className = 'ws-badge ws-type';
  typeSpan.textContent = String(typeVal);
  if(typeVal && typeof typeVal === 'string'){
    typeSpan.classList.add(`type-${typeVal}`);
  }

  const sumSpan = document.createElement('span'); sumSpan.className = 'ws-sum'; sumSpan.textContent = summarizeMessage(direction, payload);
  const copyBtn = document.createElement('button'); copyBtn.className = 'btn text-xs'; copyBtn.textContent = 'Copy JSON'; copyBtn.setAttribute('data-tip','Copy JSON'); copyBtn.title = 'Copy JSON';
  copyBtn.addEventListener('click', async (e)=>{ e.stopPropagation(); const ok = await copyTextStrict(pretty(payload)); showToast(ok? 'Copied JSON' : 'Copy failed'); });
  head.appendChild(timeSpan); head.appendChild(dirSpan); head.appendChild(typeSpan); head.appendChild(sumSpan); head.appendChild(copyBtn);
  const body = document.createElement('pre'); body.className = 'ws-body ws-json'; body.innerHTML = highlightJson(pretty(payload));
  head.addEventListener('click', ()=>{ body.style.display = (body.style.display==='none'||!body.style.display) ? 'block' : 'none'; });
  item.appendChild(head); item.appendChild(body); box.appendChild(item);
  const container = document.getElementById('wsTrafficContainer'); if(container){ container.scrollTop = container.scrollHeight; }
  
  // Highlight the Developer-Insight button
  highlightWSActivity();
}
function wsSend(obj){
  try{
    wsConnection && wsConnection.send(JSON.stringify(obj));
    appendWsMessage('→ send', obj);
    flashWebSocketActivity(); // Flash on send
  }catch(e){ console.error('wsSend error', e); }
}

function flashWebSocketActivity(){
  const wsIndicator = document.getElementById('wsStatusIndicator');
  if(wsIndicator && wsIndicator.classList.contains('connected')){
    wsIndicator.classList.add('ws-active');
    setTimeout(() => {
      wsIndicator.classList.remove('ws-active');
    }, 400);
  }
}

/* ========================================
   GAME STATE - Data Loading & Management
   ======================================== */

function updatePlayerAvatar(elementId, playerData) {
  /**
   * Update player avatar - use image if available, otherwise lookup from cache
   * @param {string} elementId - ID of avatar element
   * @param {object} playerData - Player data with avatar_url, icon, avatar, name
   */
  const avatarEl = qs(elementId);
  if (!avatarEl) {
    console.error(`❌ Avatar element not found: ${elementId}`);
    return;
  }
  
  console.log(`🎨 updatePlayerAvatar(${elementId}):`, {
    name: playerData?.name,
    avatar_url: playerData?.avatar_url,
    icon: playerData?.icon,
    avatar: playerData?.avatar
  });
  
  // Clear existing content
  avatarEl.innerHTML = '';
  
  // If avatar_url is missing but we have a player name, lookup from cache
  if (!playerData?.avatar_url && playerData?.name && playersCache) {
    console.log(`   ⚠️  No avatar_url provided - looking up in cache for: ${playerData.name}`);
    const cachedPlayer = getPlayerFromCache(playerData.name);
    
    if (cachedPlayer) {
      console.log(`   ✅ Found in cache:`, cachedPlayer.name, cachedPlayer.avatar_url);
      // Update playerData with cached info
      playerData = {
        ...playerData,
        avatar_url: cachedPlayer.avatar_url,
        icon: cachedPlayer.icon || playerData.icon,
        description: cachedPlayer.description
      };
    } else {
      console.warn(`   ⚠️  Player ${playerData.name} not found in cache`);
      console.warn(`   Cache contains:`, playersCache?.map(p => p.name));
    }
  }
  
  // Priority: avatar_url (image) > icon (emoji) > avatar (initials)
  if (playerData?.avatar_url) {
    // Use image
    console.log(`   🖼️  Loading image: ${playerData.avatar_url}`);
    const img = document.createElement('img');
    img.src = playerData.avatar_url;
    img.alt = playerData.name || 'Player';
    img.style.width = '100%';
    img.style.height = '100%';
    img.style.objectFit = 'cover';
    img.style.borderRadius = '50%';
    // Fallback to icon if image fails to load
    img.onerror = () => {
      console.error(`   ❌ Image failed to load: ${playerData.avatar_url}`);
      avatarEl.innerHTML = '';
      avatarEl.textContent = playerData.icon || playerData.avatar || initials(playerData.name);
    };
    img.onload = () => {
      console.log(`   ✅ Image loaded successfully: ${playerData.avatar_url}`);
    };
    avatarEl.appendChild(img);
  } else if (playerData?.icon) {
    // Use icon emoji
    console.log(`   😀 Using icon: ${playerData.icon}`);
    avatarEl.textContent = playerData.icon;
  } else {
    // Use initials
    const ini = playerData?.avatar || initials(playerData?.name);
    console.log(`   🔤 Using initials: ${ini}`);
    avatarEl.textContent = ini;
  }
}

function loadGameData(gameData){
  data = gameData;

  // Update header
  qs('p1Name').textContent   = data.players?.black?.name || '—';
  qs('p2Name').textContent   = data.players?.white?.name || '—';
  
  console.log('👥 loadGameData - Players assigned from backend:');
  console.log('   ⚫ Black (plays first, left side):', data.players?.black?.name);
  console.log('   ⚪ White (plays second, right side):', data.players?.white?.name);
  console.log('   Current turn:', data.status?.turn_by_ply?.[0] || 'B');
  console.log('   Full player data:', {
    black: {
      name: data.players?.black?.name,
      avatar_url: data.players?.black?.avatar_url,
      icon: data.players?.black?.icon,
      avatar: data.players?.black?.avatar
    },
    white: {
      name: data.players?.white?.name,
      avatar_url: data.players?.white?.avatar_url,
      icon: data.players?.white?.icon,
      avatar: data.players?.white?.avatar
    }
  });
  
  // Update avatars - use image if available, otherwise icon/initials
  updatePlayerAvatar('p1Avatar', data.players?.black);
  updatePlayerAvatar('p2Avatar', data.players?.white);
  
  // Show/hide AI config button for White player (if AI)
  const whitePlayerType = data.players?.white?.player_type;
  const whiteAIName = data.players?.white?.ai_name;
  const viewWhiteConfigBtn = document.getElementById('viewWhiteConfigBtn');
  
  // TEMPORARY: Force show button for testing
  // Set AI name from white player name (fallback)
  if (viewWhiteConfigBtn) {
    const whiteName = data.players?.white?.name;
    if (whiteName && whiteName !== 'Human' && whiteName !== 'Human Player') {
      viewWhiteConfigBtn.style.display = 'inline-flex';
      currentAIPlayerName = whiteName.toUpperCase(); // "Lightning Strike" → "LIGHTNING STRIKE"
      console.log(`✅ AI Config button enabled for: ${currentAIPlayerName}`);
    } else {
      console.log('Player data:', {
        whitePlayerType,
        whiteAIName,
        whiteName,
        hasButton: !!viewWhiteConfigBtn,
        fullPlayerData: data.players?.white
      });
    }
  }
  
  // Update player icons based on type
  updatePlayerIcons();
  
  // Update maxPly for calculations
  const maxPly = (data.positions?.length || 1) - 1;

  // Update moves list if exists
  const movesOl = document.getElementById('movesOl');
  if(movesOl && !movesOl.classList.contains('hidden')){
    movesOl.innerHTML = '';
    (data.moves||[]).forEach((m,i)=>{
      const li = document.createElement('li'); li.textContent = m; li.dataset.ply = i+1;
                  li.addEventListener('click', ()=>{ if(data){ ply = i+1; render(); } });
      movesOl.appendChild(li);
    });
  }

  // Re-render with new data (keep current ply; clamp within new bounds)
  const newMaxPly = (data.positions?.length || 1) - 1;
  if(ply > newMaxPly) ply = newMaxPly;
  render();
  
  // Update AI Stats title based on current turn
  const aiStatsTitle = qs('aiQuickStatsTitle');
  if(aiStatsTitle) {
    // Determine which player is AI
    const blackName = data.players?.black?.name;
    const whiteName = data.players?.white?.name;
    const isBlackAI = blackName && blackName !== 'Human' && blackName !== 'Human Player';
    const isWhiteAI = whiteName && whiteName !== 'Human' && whiteName !== 'Human Player';
    
    // Get current turn
    const currentTurn = (data.status && data.status.turn_by_ply && data.status.turn_by_ply.length > 0) 
      ? data.status.turn_by_ply[0] : 'B';
    
    // Set title to AI player name
    if (isBlackAI && !isWhiteAI) {
      aiStatsTitle.textContent = `⚫ ${blackName}`;
      showAIQuickStatsPanel(); // Show panel for AI
    } else if (isWhiteAI && !isBlackAI) {
      aiStatsTitle.textContent = `⚪ ${whiteName}`;
      showAIQuickStatsPanel(); // Show panel for AI
    } else if (isBlackAI && isWhiteAI) {
      // Both AI - show stats for the AI that's currently moving
      if(currentTurn === 'B') {
        aiStatsTitle.textContent = `⚫ ${blackName}`;
      } else {
        aiStatsTitle.textContent = `⚪ ${whiteName}`;
      }
      showAIQuickStatsPanel(); // Show panel for AI
    } else {
      // No AI players
      aiStatsTitle.textContent = 'AI Statistics';
      hideAIQuickStats();
    }
  }
  
  // Rebuild history
  if(window.buildHistory){
    window.buildHistory();
  }
}

/* ========================================
   BOARD - DOM Construction & Events
   ======================================== */
function buildBoard(){
  const elBoard = document.getElementById('board');
  const coords = ['A1','B1','C1','D1','E1','F1','G1','H1','A2','B2','C2','D2','E2','F2','G2','H2',
                  'A3','B3','C3','D3','E3','F3','G3','H3','A4','B4','C4','D4','E4','F4','G4','H4',
                  'A5','B5','C5','D5','E5','F5','G5','H5','A6','B6','C6','D6','E6','F6','G6','H6',
                  'A7','B7','C7','D7','E7','F7','G7','H7','A8','B8','C8','D8','E8','F8','G8','H8'];
  
  for (let i=0;i<64;i++){
    const cell = document.createElement('div'); 
    cell.className = 'cell';
    cell.dataset.coord = coords[i]; // Store coordinate
    cell.onclick = () => {
      console.log('Cell clicked:', cell.dataset.coord, 'wsReady:', wsConnection?.readyState === WebSocket.OPEN, 'data:', !!data);
      
      // Check current turn from data
      let currentTurn = (data && data.status && Array.isArray(data.status.turn_by_ply))
        ? (data.status.turn_by_ply[ply] || (ply%2===0 ? 'B' : 'W'))
        : (ply%2===0 ? 'B' : 'W');
      
      // Check if current side is Human (not AI)
      const isBlackHuman = !data?.players?.black?.name || data.players.black.name === 'Human' || data.players.black.name === 'Human Player';
      const isWhiteHuman = !data?.players?.white?.name || data.players.white.name === 'Human' || data.players.white.name === 'Human Player';
      const isCurrentSideHuman = (currentTurn === 'B' && isBlackHuman) || (currentTurn === 'W' && isWhiteHuman);
      
      const canMove = (isCurrentSideHuman && wsConnection && wsConnection.readyState === WebSocket.OPEN);
      console.log('Current turn:', currentTurn, 'isCurrentSideHuman:', isCurrentSideHuman, 'canMove:', canMove);
      
      if(canMove){
        submitMove(cell.dataset.coord);
      } else {
        console.log('Move rejected - not human player turn or WebSocket closed');
      }
    };
    const inner = document.createElement('div'); 
    inner.className = 'cell-content';
    cell.appendChild(inner); 
    elBoard.appendChild(cell);
  }
}

// WebSocket Status Indicator Functions
function updateWSStatus(status, text) {
  const indicator = document.getElementById('wsStatusIndicator');
  if (!indicator) {
    console.error('WebSocket status indicator not found!');
    return;
  }
  
  const textEl = indicator.querySelector('.ws-status-text');
  if (!textEl) {
    console.error('WebSocket status text element not found!');
    return;
  }
  
  // Remove all status classes
  indicator.classList.remove('connected', 'connecting', 'disconnected');
  
  // Add appropriate class and update text
  indicator.classList.add(status);
  textEl.textContent = text;
  
  console.log('WebSocket status updated:', status, text);
}

// WebSocket functions
function initWebSocket(){
  updateWSStatus('connecting', 'Connecting...');
  wsConnection = new WebSocket(WS_URL);
  
  wsConnection.onopen = async () => {
    console.log('WebSocket connected successfully');
    updateWSStatus('connected', 'Connected');
    
    // Don't auto-init - wait for initial setup screen
    console.log('⏸️  WebSocket ready - waiting for player selection from initial screen');
  };
  
  wsConnection.onmessage = (event) => {
    try{ appendWsMessage('← recv', JSON.parse(event.data)); }catch(_){ appendWsMessage('← recv', event.data); }
    const message = JSON.parse(event.data);
    flashWebSocketActivity(); // Flash on receive
    handleServerMessage(message);
  };
  
  wsConnection.onclose = (event) => {
    console.log('WebSocket disconnected. Code:', event.code, 'Reason:', event.reason, 'Clean:', event.wasClean);
    console.log('Attempting reconnect in 3 seconds...');
    updateWSStatus('disconnected', 'Reconnecting...');
    setTimeout(initWebSocket, 3000);
  };
  
  wsConnection.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
    console.error('WebSocket readyState:', wsConnection.readyState);
    console.error('WebSocket URL:', WS_URL);
    console.error('Stack trace:', new Error().stack);
    updateWSStatus('disconnected', 'Connection Error');
  };
  
  // Log connection attempt
  console.log('Attempting to connect to:', WS_URL);
}

function handleServerMessage(message){
  // Process AI statistics from any message type that contains them
  if(message.data && (message.data.nodes_searched || message.data.nodes || message.data.depth_reached)){
    scheduleStatsUpdate(message.data, message.type === 'ai_statistics_summary');
  }
  
  try {
  switch(message.type){
    case 'board_update':
      // Update board from server
      data = message.data;
      // Clear any previous game-over banner on fresh state
      gameOverInfo = null;
      console.log('🔄 Board update received - gameOverInfo reset to null');
      // Reset AI pause if it's a fresh game (ply < 3)
      if(data.status && data.status.ply !== undefined && data.status.ply < 3){
        aiAutoPaused = false;
        console.log('Fresh game detected (ply < 3) - AI auto-play enabled');
      }
      console.log('Board data:', data);
      console.log('Positions:', data.positions);
      console.log('Ply:', ply, 'Positions[0]:', data.positions?.[0]);
      
      // Update player names everywhere
      if(data.players?.white?.name){
        const p2Name = qs('p2Name');
        if(p2Name) p2Name.textContent = data.players.white.name;
        // Update avatar with image support
        updatePlayerAvatar('p2Avatar', data.players.white);
        if(pendingSelectedAI && data.players.white.name === pendingSelectedAI){
          showToast(`AI set to ${pendingSelectedAI}`);
          pendingSelectedAI = null;
        }
      }
      
      loadGameData(data);
      // Render opening tree if provided
      try{
        if(data && data.opening_tree){
          renderOpeningTree(data.opening_tree);
        } else {
          renderOpeningTree(null);
        }
      }catch(e){ console.warn('Opening tree render error', e); }
      
      // Check if AI should move (only if not paused)
      if(!aiAutoPaused){
        checkAndRequestAIMove();
      }
      
      break;
      
    case 'ai_move':
      const aiMoveSide = data?.status?.turn_by_ply?.[0] || 'W';
      const aiPlayerName = aiMoveSide === 'B' ? data.players?.black?.name : data.players?.white?.name;
      console.log(`${aiPlayerName} played:`, message.data.move);
      
      // Reset stats visibility flag (search is complete)
      statsCurrentlyVisible = false;
      
      // Deactivate AI Insight button animation
      const aiInsightBtnMove = document.getElementById('toggleAiInsight');
      if(aiInsightBtnMove){
        aiInsightBtnMove.classList.remove('ai-thinking');
      }
      
      // Remove thinking icon from BOTH sides to prevent stale icons
      removeThinkingIconFromPlayerName('B');
      removeThinkingIconFromPlayerName('W');
      // Show AI move animation
      if(message.data.move){
        const moveCoord = message.data.move;
        const moveIdx = coordToIdx(moveCoord);
        const cell = document.getElementById('board')?.children[moveIdx];
        if(cell){
          cell.classList.add('ai-move-highlight');
          setTimeout(() => cell.classList.remove('ai-move-highlight'), 2000);
        }
      }
      // Update notes with AI analysis if available (include AI name from side)
      if(message.data.evaluation !== undefined || message.data.depth || message.data.move){
        const aiMovedSide = aiMoveSide; // Already calculated above
        const aiMovedName = aiPlayerName; // Already calculated above
        updateAIAnalysis({...message.data, title: aiMovedName, side: aiMovedSide});
      }
      console.log('AI move completed, waiting for board_update');
      break;
      
    case 'ai_thinking':
      // Show "Searching..." state ONLY on first message (no stats yet AND panel not visible)
      const hasStats = message.data && ((message.data.nodes_searched || message.data.nodes || 0) > 0);
      if(!hasStats && !statsCurrentlyVisible){
        showAISearchingState();
      }
      
      // Activate AI Insight button animation
      const aiInsightBtn = document.getElementById('toggleAiInsight');
      if(aiInsightBtn){
        aiInsightBtn.classList.add('ai-thinking');
      }
      
      // Add thinking icon to AI player name (determine side from current turn)
      const thinkingSide = data?.status?.turn_by_ply?.[0] || 'W';
      
      // ONLY add thinking icon if that side is actually AI (not Human)
      const thinkingBlackName = data?.players?.black?.name;
      const thinkingWhiteName = data?.players?.white?.name;
      const isThinkingSideAI = (thinkingSide === 'B' && thinkingBlackName && thinkingBlackName !== 'Human' && thinkingBlackName !== 'Human Player')
                            || (thinkingSide === 'W' && thinkingWhiteName && thinkingWhiteName !== 'Human' && thinkingWhiteName !== 'Human Player');
      
      console.log('🤔 ai_thinking received - Side:', thinkingSide, 'isAI:', isThinkingSideAI, 'BlackName:', thinkingBlackName, 'WhiteName:', thinkingWhiteName);
      
      if(isThinkingSideAI){
        addThinkingIconToPlayerName(thinkingSide);
      } else {
        console.warn('⚠️  ai_thinking received for HUMAN player - ignoring!');
      }
      
      if(pendingSelectedAI && data && data.players){
        const currentAIName = thinkingSide === 'B' ? data.players.black?.name : data.players.white?.name;
        if(currentAIName === pendingSelectedAI){
          showToast(`AI set to ${pendingSelectedAI}`);
          pendingSelectedAI = null;
        }
      }
      // Update notes with "thinking" state if we have AI data
      const thinkingAIName = thinkingSide === 'B' ? data.players?.black?.name : data.players?.white?.name;
      if(message.data){
        updateAIAnalysis({...message.data, title: thinkingAIName});
        // Stats already updated by universal handler
      } else {
        // If no data yet, show thinking status
        const aiAnalysis = {
          title: thinkingAIName || 'AI',
          status: 'Thinking...',
          selected_move: 'Analyzing...',
          evaluation: 'Calculating...',
          depth: 'Searching...',
          nodes_searched: 'Calculating...',
          nodes_pruned: 'Calculating...',
          pruning_ratio: 'Calculating...',
          avg_search_time: 'Calculating...',
          total_searches: 'Calculating...'
        };
        data.notes = aiAnalysis;
        updateAIAnalysis(aiAnalysis);
      }
      break;
      
    case 'game_over':
      console.log('Game over!', message.data);
      // Stop AI auto-play
      aiAutoPaused = true;
      // Persist winner info for header rendering
      gameOverInfo = {
        winner: message.data.winner || 'Game Over',
        black_count: message.data.black_count || 0,
        white_count: message.data.white_count || 0
      };
      // Update header immediately
      render();
      // Update Play/Pause button to show it's stopped
      const btn = qs('aiPlayPauseBtn');
      const icon = document.getElementById('aiPlayPauseIcon');
      if(btn && icon){
        icon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"/>';
        btn.title = 'Play AI';
        btn.setAttribute('data-tip', 'Play AI');
        btn.style.background = 'rgba(245,158,11,.12)';
        btn.style.borderColor = 'rgba(245,158,11,.35)';
      }
      // Show game over message (non-blocking)
      setTimeout(() => {
        const winner = gameOverInfo.winner;
        const blackCount = gameOverInfo.black_count;
        const whiteCount = gameOverInfo.white_count;
        console.log(`🎮 GAME OVER - Winner: ${winner} (Black: ${blackCount}, White: ${whiteCount})`);
        
        // Show a non-blocking notification instead of alert
        if (confirm(`🎮 GAME OVER\n\nWinner: ${winner}\n\nBlack: ${blackCount} pieces\nWhite: ${whiteCount} pieces\n\nStart a new game?`)) {
          // User clicked OK - Reset state IMMEDIATELY before starting new game
          console.log('🔄 User confirmed new game - resetting state immediately');
          gameOverInfo = null;
          aiAutoPaused = false;
          // Now start new game
          document.getElementById('newGameBtn')?.click();
        }
      }, 100);
      break;
    
    case 'ai_log':
      // Handle AI reasoning logs
      console.log('📝 [AI_LOG] Received:', message.data.log_type, '-', message.data.message);
      if(message.data){
        if(typeof appendAILog === 'function'){
          appendAILog(message.data);
        } else {
          console.error('❌ appendAILog function not available! Template may not be loaded.');
        }
        // Stats already updated by universal handler
      }
      break;
    
    case 'ai_statistics_summary':
      // Handle comprehensive AI statistics for data science dashboard
      console.log('📊 ai_statistics_summary received:', message.data);
      if(message.data){
        showAIStatisticsDashboard(message.data);
        
        // Stats already updated by universal handler (as final)
        
        // Also update the Notes box with comprehensive statistics
        updateAIAnalysis({
          ...message.data,
          title: message.data.player_name,
          move: message.data.best_move,
          evaluation: message.data.evaluation,
          depth: message.data.depth_reached,
          nodes_searched: message.data.nodes_searched,
          nodes_pruned: message.data.nodes_pruned,
          pruning_ratio: message.data.pruning_efficiency / 100, // Convert % to ratio
          avg_search_time: `${message.data.total_time_ms}ms`,
          total_searches: message.data.iterations_completed || 0,
          nodes_per_second: message.data.nodes_per_second, // Add N/s
          transposition_hits: message.data.tt_hits,
          killer_moves: message.data.pv_move_hits,
          history_entries: message.data.history_entries,
          null_move_cutoffs: message.data.null_move_cuts,
          futility_pruned: message.data.futility_cuts,
          lmr_reductions: message.data.lmr_reductions,
          multi_cut_pruned: message.data.multi_cut_prunes,
          last_search_time_ms: message.data.total_time_ms
        });
      }
      
      // Deactivate AI Insight button animation (search complete)
      const aiInsightBtnStats = document.getElementById('toggleAiInsight');
      if(aiInsightBtnStats){
        aiInsightBtnStats.classList.remove('ai-thinking');
      }
      break;
      
    case 'error':
      console.error('Server error:', message.message);
      alert(`Error: ${message.message || 'Invalid move. Please try again.'}`);
      break;
  }
  } catch (error) {
    console.error('❌ CRITICAL ERROR in handleServerMessage:', error);
    console.error('Stack trace:', error.stack);
    console.error('Message was:', message);
    // Don't close WebSocket connection - just log the error
    alert(`⚠️  Frontend Error: ${error.message}\n\nCheck console for details.`);
  }
}

function toggleAIPlayPause(){
  aiAutoPaused = !aiAutoPaused;
  const btn = qs('aiPlayPauseBtn');
  const icon = document.getElementById('aiPlayPauseIcon');
  
  if(aiAutoPaused){
    // Paused - show Play icon
    icon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"/>';
    btn.title = 'Play AI';
    btn.setAttribute('data-tip', 'Play AI');
    btn.style.background = 'rgba(245,158,11,.12)';
    btn.style.borderColor = 'rgba(245,158,11,.35)';
    showToast('AI Auto-Play Paused');
  } else {
    // Playing - show Pause icon
    icon.innerHTML = '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
    btn.title = 'Pause AI';
    btn.setAttribute('data-tip', 'Pause AI');
    btn.style.background = 'rgba(16,185,129,.12)';
    btn.style.borderColor = 'rgba(16,185,129,.35)';
    showToast('AI Auto-Play Resumed');
    
    // If an AI should move now, trigger it
    if(!aiAutoPaused && data){
      const currentTurn = (data.status && data.status.turn_by_ply && data.status.turn_by_ply.length > 0) 
        ? data.status.turn_by_ply[0] : 'B';
      const blackName = data.players?.black?.name;
      const whiteName = data.players?.white?.name;
      const isBlackAI = blackName && blackName !== 'Human' && blackName !== 'Human Player';
      const isWhiteAI = whiteName && whiteName !== 'Human' && whiteName !== 'Human Player';
      const isCurrentSideAI = (currentTurn === 'B' && isBlackAI) || (currentTurn === 'W' && isWhiteAI);
      
      if(isCurrentSideAI && wsConnection && wsConnection.readyState === WebSocket.OPEN){
        console.log('Resuming AI - requesting move for side:', currentTurn);
        wsSend({ type: 'ai_move_request', side: currentTurn });
      }
    }
  }
}

function toggleOpeningHints(){
  showOpeningHints = !showOpeningHints;
  const btn = qs('toggleOpeningBtn');
  
  if(showOpeningHints){
    // Active - gold style
    btn.style.background = 'rgba(245,158,11,.18)';
    btn.style.borderColor = 'rgba(245,158,11,.45)';
    btn.style.color = '#fbbf24';
    btn.title = 'Hide opening hints';
    btn.setAttribute('data-tip', 'Hide opening hints');
    showToast('📚 Opening hints enabled');
  } else {
    // Inactive - normal style
    btn.style.background = 'rgba(255,255,255,.05)';
    btn.style.borderColor = 'rgba(255,255,255,.14)';
    btn.style.color = 'var(--txt)';
    btn.title = 'Show opening hints';
    btn.setAttribute('data-tip', 'Show opening hints');
    showToast('Opening hints disabled');
  }
  
  // Re-render board to apply changes
  render();
}

function submitMove(move){
  if(!wsConnection || wsConnection.readyState !== WebSocket.OPEN){
    return;
  }
  
  // Double-check current turn and human status
  const currentTurn = (data && data.status && data.status.turn_by_ply && data.status.turn_by_ply.length > 0) 
    ? data.status.turn_by_ply[0] : 'B';
  
  const isBlackHuman = !data?.players?.black?.name || data.players.black.name === 'Human' || data.players.black.name === 'Human Player';
  const isWhiteHuman = !data?.players?.white?.name || data.players.white.name === 'Human' || data.players.white.name === 'Human Player';
  const isCurrentSideHuman = (currentTurn === 'B' && isBlackHuman) || (currentTurn === 'W' && isWhiteHuman);
  
  if(!isCurrentSideHuman){
    console.log('Cannot submit move: current side is AI. Current turn:', currentTurn);
    return;
  }
  
  console.log('Submitting human move:', move, 'for side:', currentTurn);
  wsSend({ type: 'human_move', move: move });
}

function checkAndRequestAIMove(){
  console.log('🤖 checkAndRequestAIMove called - gameOverInfo:', gameOverInfo, 'aiAutoPaused:', aiAutoPaused);
  
  if(!data || !wsConnection || wsConnection.readyState !== WebSocket.OPEN){
    console.log('❌ Cannot request AI move - missing data or connection');
    return;
  }
  
  // Don't request if game is over
  if(gameOverInfo){
    console.log('❌ Game is over - not requesting AI move. gameOverInfo:', gameOverInfo);
    return;
  }
  
  // Don't request if board is full (64 pieces)
  if(data.status && (data.status.black_count + data.status.white_count) >= 64){
    console.log('❌ Board is full - game over, not requesting AI move');
    return;
  }
  
  // Don't request if paused
  if(aiAutoPaused){
    console.log('⏸️  AI auto-play paused - not requesting move');
    return;
  }
  
  // Get current turn
  const currentTurn = (data.status && data.status.turn_by_ply && data.status.turn_by_ply.length > 0) 
    ? data.status.turn_by_ply[0] : 'B';
  
  // Check if current side is AI
  const blackName = data.players?.black?.name;
  const whiteName = data.players?.white?.name;
  const isBlackAI = blackName && blackName !== 'Human' && blackName !== 'Human Player';
  const isWhiteAI = whiteName && whiteName !== 'Human' && whiteName !== 'Human Player';
  const isCurrentSideAI = (currentTurn === 'B' && isBlackAI) || (currentTurn === 'W' && isWhiteAI);
  
  if(isCurrentSideAI){
    console.log('✅ Current turn is AI:', currentTurn, '- requesting AI move');
    setTimeout(() => {
      wsSend({ type: 'ai_move_request', side: currentTurn });
    }, 100);
  } else {
    console.log('👤 Current turn is human:', currentTurn, '- waiting for user input');
  }
}

/* ========================================
   PLAYER CACHE - Preload player data for fast avatar lookups
   ======================================== */
async function loadPlayersCache(){
  try {
    console.log('👥 Loading players cache from API...');
    const response = await fetch('http://localhost:8000/api/players');
    if(response.ok){
      const data = await response.json();
      playersCache = data.players || [];
      console.log(`✅ Players cache loaded: ${playersCache.length} players`);
      return playersCache;
    }
  } catch(error){
    console.warn('⚠️  Could not load players cache:', error);
  }
  return [];
}

function getPlayerFromCache(playerName){
  if(!playersCache || !playerName) return null;
  return playersCache.find(p => 
    p.name === playerName || 
    p.name.toUpperCase() === playerName.toUpperCase()
  );
}

/* ========================================
   VERSION LOADING - Load from centralized source
   ======================================== */
async function loadVersion(){
  try {
    console.log('📦 Loading version from API...');
    const response = await fetch('http://localhost:8000/api/version');
    if(response.ok){
      const versionData = await response.json();
      gameVersion = versionData.version || '6.1.0';
      console.log(`✅ Version loaded: ${gameVersion}`);
      
      // Update initial setup screen
      const initialVersionEl = document.getElementById('initialSetupVersion');
      if(initialVersionEl){
        initialVersionEl.textContent = `v${gameVersion}`;
      }
      
      // Update game screen
      const gameVersionEl = document.getElementById('versionText');
      if(gameVersionEl){
        gameVersionEl.textContent = `v${gameVersion}`;
      }
      
      // Update version badge title with full info
      const versionBadge = document.getElementById('versionBadge');
      if(versionBadge && versionData.author){
        versionBadge.title = `Reversi42 v${gameVersion}\nby ${versionData.author}`;
      }
      
      return gameVersion;
    }
  } catch(error){
    console.warn('⚠️  Could not load version from API, using fallback:', gameVersion);
  }
  return gameVersion;
}

/* ========================================
   INITIAL SETUP SCREEN - Player Selection
   ======================================== */
function setupInitialScreen(){
  console.log('🔧 setupInitialScreen called');
  console.log('   DOM ready:', document.readyState);
  
  // Add class to body so modal can have higher z-index
  document.body.classList.add('initial-setup-active');
  console.log('✅ Added initial-setup-active class to body');
  
  const initialSelectBlackBtn = document.getElementById('initialSelectBlackBtn');
  const initialSelectWhiteBtn = document.getElementById('initialSelectWhiteBtn');
  const initialStartGameBtn = document.getElementById('initialStartGameBtn');
  const initialBlackCard = document.getElementById('initialBlackCard');
  const initialWhiteCard = document.getElementById('initialWhiteCard');
  
  console.log('   Elements found:', {
    blackBtn: !!initialSelectBlackBtn,
    whiteBtn: !!initialSelectWhiteBtn,
    startBtn: !!initialStartGameBtn,
    blackCard: !!initialBlackCard,
    whiteCard: !!initialWhiteCard
  });
  console.log('   window.openPlayersModal:', typeof window.openPlayersModal);
  
  // Verify modal exists
  const playersModal = document.getElementById('playersModal');
  console.log('   playersModal element:', !!playersModal);
  if(playersModal){
    console.log('   playersModal display:', window.getComputedStyle(playersModal).display);
  }
  
  // Load default avatars
  console.log('🎨 Loading default avatars for initial screen...');
  updateInitialPlayerDisplay('black', initialBlackPlayer);
  updateInitialPlayerDisplay('white', initialWhitePlayer);
  
  // Handler for opening black player picker
  const openBlackPicker = (e) => {
    e?.preventDefault();
    e?.stopPropagation();
    console.log('🎯 BLACK PICKER REQUESTED!');
    console.log('   initialSetupComplete:', initialSetupComplete);
    console.log('   window.openPlayersModal:', typeof window.openPlayersModal);
    
    initialSelectingFor = 'black';
    
    if(typeof window.openPlayersModal === 'function'){
      console.log('   ✅ Calling window.openPlayersModal("B")');
      try {
        window.openPlayersModal('B');
        console.log('   ✅ Modal opened');
      } catch(err) {
        console.error('   ❌ Error:', err);
      }
    } else {
      console.error('❌ window.openPlayersModal not available!');
    }
  };
  
  // Handler for opening white player picker
  const openWhitePicker = (e) => {
    e?.preventDefault();
    e?.stopPropagation();
    console.log('🎯 WHITE PICKER REQUESTED!');
    console.log('   initialSetupComplete:', initialSetupComplete);
    console.log('   window.openPlayersModal:', typeof window.openPlayersModal);
    
    initialSelectingFor = 'white';
    
    if(typeof window.openPlayersModal === 'function'){
      console.log('   ✅ Calling window.openPlayersModal("W")');
      try {
        window.openPlayersModal('W');
        console.log('   ✅ Modal opened');
      } catch(err) {
        console.error('   ❌ Error:', err);
      }
    } else {
      console.error('❌ window.openPlayersModal not available!');
    }
  };
  
  // TEST: Add a basic test click handler to see if ANY click works
  if(initialSelectBlackBtn){
    console.log('🧪 TEST: Adding test click handler to Black button');
    initialSelectBlackBtn.onclick = function(e) {
      console.log('🧪 TEST CLICK DETECTED ON BLACK BUTTON!');
      console.log('   Event:', e);
      console.log('   Target:', e.target);
      console.log('   CurrentTarget:', e.currentTarget);
      openBlackPicker(e);
    };
    console.log('   ✅ Test handler attached via onclick');
  } else {
    console.error('❌ initialSelectBlackBtn not found in DOM!');
  }
  
  // Make entire Black card clickable
  if(initialBlackCard){
    console.log('✅ Making Black card clickable');
    initialBlackCard.onclick = function(e) {
      // Don't trigger if clicking on the button (will handle separately)
      if(e.target.closest('#initialSelectBlackBtn')) {
        console.log('   Click on button, ignoring card handler');
        return;
      }
      console.log('🎯 BLACK CARD CLICKED!');
      openBlackPicker(e);
    };
  }
  
  if(initialSelectWhiteBtn){
    console.log('🧪 TEST: Adding test click handler to White button');
    initialSelectWhiteBtn.onclick = function(e) {
      console.log('🧪 TEST CLICK DETECTED ON WHITE BUTTON!');
      console.log('   Event:', e);
      console.log('   Target:', e.target);
      console.log('   CurrentTarget:', e.currentTarget);
      openWhitePicker(e);
    };
    console.log('   ✅ Test handler attached via onclick');
  } else {
    console.error('❌ initialSelectWhiteBtn not found in DOM!');
  }
  
  // Make entire White card clickable
  if(initialWhiteCard){
    console.log('✅ Making White card clickable');
    initialWhiteCard.onclick = function(e) {
      // Don't trigger if clicking on the button (will handle separately)
      if(e.target.closest('#initialSelectWhiteBtn')) {
        console.log('   Click on button, ignoring card handler');
        return;
      }
      console.log('🎯 WHITE CARD CLICKED!');
      openWhitePicker(e);
    };
  }
  
  if(initialStartGameBtn){
    console.log('✅ Attaching to Start button');
    initialStartGameBtn.addEventListener('click', () => {
      console.log('🎮 Starting game with:', initialBlackPlayer, 'vs', initialWhitePlayer);
      startGameWithPlayers(initialBlackPlayer, initialWhitePlayer);
    });
    console.log('   ✅ Attached');
  } else {
    console.error('❌ initialStartGameBtn not found in DOM!');
  }
  
  // Swap button in initial screen
  const initialSwapPlayersBtn = document.getElementById('initialSwapPlayersBtn');
  if(initialSwapPlayersBtn){
    console.log('✅ Attaching to Swap button in initial screen');
    initialSwapPlayersBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      console.log('🔄 Swap button clicked in initial screen');
      swapInitialPlayers();
    });
  }
  
  // Cancel button
  const initialCancelBtn = document.getElementById('initialCancelBtn');
  if(initialCancelBtn){
    console.log('✅ Attaching to Cancel button');
    initialCancelBtn.addEventListener('click', () => {
      console.log('❌ Cancel clicked - returning to current game');
      cancelInitialSetup();
    });
    
    // Hide cancel button if this is the first load (no game to return to)
    if(!data || !data.status){
      console.log('   No current game - hiding Cancel button');
      initialCancelBtn.style.display = 'none';
    }
  }
  
  // Intercept ESC key to cancel setup
  console.log('✅ Adding ESC key handler for initial screen');
  const escHandler = (e) => {
    if(e.key === 'Escape'){
      const setupScreen = document.getElementById('initialSetupScreen');
      if(setupScreen && !setupScreen.classList.contains('hidden')){
        console.log('⌨️  ESC pressed - canceling initial setup');
        e.preventDefault();
        e.stopPropagation();
        cancelInitialSetup();
      }
    }
  };
  document.addEventListener('keydown', escHandler, true);
  
  // Global click test
  console.log('🧪 Adding global click listener for debugging...');
  document.addEventListener('click', function(e) {
    console.log('🖱️  GLOBAL CLICK:', e.target.id, e.target.className);
  }, true);
  
  console.log('🏁 setupInitialScreen completed');
}

async function updateInitialPlayerDisplay(side, playerName){
  const avatarEl = document.getElementById(side === 'black' ? 'initialBlackAvatar' : 'initialWhiteAvatar');
  const nameEl = document.getElementById(side === 'black' ? 'initialBlackName' : 'initialWhiteName');
  const descEl = document.getElementById(side === 'black' ? 'initialBlackDesc' : 'initialWhiteDesc');
  const tagsEl = document.getElementById(side === 'black' ? 'initialBlackTags' : 'initialWhiteTags');
  
  console.log(`🎨 updateInitialPlayerDisplay called: side=${side}, playerName=${playerName}`);
  
  if(!avatarEl || !nameEl){
    console.error('❌ Avatar or name element not found:', side);
    return;
  }
  
  // Update stored selection
  if(side === 'black'){
    initialBlackPlayer = playerName;
  } else {
    initialWhitePlayer = playerName;
  }
  
  // Update display
  nameEl.textContent = playerName;
  
  // Clear avatar content
  avatarEl.innerHTML = '';
  avatarEl.style.fontSize = '3rem'; // Reset font size for emoji
  
  // Get player data from API to get full info
  try{
    console.log(`📡 Fetching players from API for ${playerName}...`);
    const response = await fetch('http://localhost:8000/api/players');
    if(!response.ok){
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    console.log(`✅ API response received, total players: ${data.players?.length}`);
    
    // Normalize "Human" to "Human Player" for search
    const searchName = (playerName && playerName.toLowerCase() === 'human') ? 'Human Player' : playerName;
    
    const player = data.players?.find(p => 
      p.name === searchName || 
      p.name.toUpperCase() === searchName.toUpperCase()
    );
    console.log(`🔍 Searching for: "${playerName}" (normalized to: "${searchName}")`);
    console.log(`   Available players:`, data.players?.map(p => p.name));
    console.log(`   Found player:`, player ? `${player.name} (avatar_url: ${player.avatar_url})` : 'NOT FOUND');
    
    if(player){
      // Update description
      if(descEl && player.description){
        descEl.textContent = player.description;
        console.log(`📝 Description updated: ${player.description}`);
      }
      
      // Update tags
      if(tagsEl){
        tagsEl.innerHTML = '';
        const tags = [];
        
        // Add main tag (HUMAN/AI)
        if(player.tag){
          tags.push({ name: player.tag, class: player.tag.toLowerCase() });
        }
        
        // Add category (champion/premium/specialist/intermediate/beginner)
        if(player.category){
          tags.push({ name: player.category.toUpperCase(), class: player.category.toLowerCase() });
        }
        
        // Add config tags (Gladiators, depth, etc.)
        if(player.config_tags && Array.isArray(player.config_tags)){
          player.config_tags.slice(0, 3).forEach(tag => {
            tags.push({ name: tag.toUpperCase(), class: 'config' });
          });
        }
        
        console.log(`🏷️  Tags:`, tags);
        
        // Render tags
        tags.forEach(tag => {
          const tagEl = document.createElement('span');
          tagEl.className = `initial-tag ${tag.class}`;
          tagEl.textContent = tag.name;
          tagsEl.appendChild(tagEl);
        });
      }
      
      // Update avatar
      if(player.avatar_url){
        // Use PNG avatar
        console.log(`🖼️  Loading avatar image: ${player.avatar_url}`);
        const img = document.createElement('img');
        img.src = player.avatar_url;
        img.alt = playerName;
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        img.onerror = (e) => {
          console.error(`❌ Avatar image failed to load: ${player.avatar_url}`, e);
          // Fallback to icon/emoji if image fails
          avatarEl.innerHTML = '';
          avatarEl.textContent = player.icon || '🤖';
        };
        img.onload = () => {
          console.log(`✅ Avatar image loaded successfully: ${player.avatar_url}`);
        };
        avatarEl.appendChild(img);
      } else if(player.icon){
        // Use emoji icon
        console.log(`😀 Using emoji icon: ${player.icon}`);
        avatarEl.textContent = player.icon;
      } else {
        // Fallback to generic emoji
        const isHuman = playerName === 'Human' || playerName === 'Human Player';
        avatarEl.textContent = isHuman ? '👤' : '🤖';
        console.log(`⚠️  Using fallback emoji: ${isHuman ? '👤' : '🤖'}`);
      }
    } else {
      console.warn(`⚠️  Player ${playerName} not found in API response`);
      // Use fallback values
      if(descEl) descEl.textContent = 'Player description not available';
      if(tagsEl) tagsEl.innerHTML = '<span class="initial-tag">UNKNOWN</span>';
    }
  } catch(error){
    console.error('❌ Failed to load player data:', error);
    // Fallback
    const isHuman = playerName === 'Human' || playerName === 'Human Player';
    avatarEl.textContent = isHuman ? '👤' : '🤖';
    if(descEl) descEl.textContent = 'Error loading player data';
    if(tagsEl) tagsEl.innerHTML = '';
  }
}

function swapPlayersAndRestart(){
  console.log('🔄 Swapping players and restarting game');
  
  if(!data || !data.players){
    console.error('❌ No player data available to swap');
    showToast('No players to swap');
    return;
  }
  
  // Get current players
  const currentBlack = data.players.black?.name || 'Human Player';
  const currentWhite = data.players.white?.name || 'LIGHTNING STRIKE';
  
  console.log('🔀 Swapping:', { 
    before: { black: currentBlack, white: currentWhite },
    after: { black: currentWhite, white: currentBlack }
  });
  
  // Reset game state
  gameOverInfo = null;
  aiAutoPaused = false;
  
  if(wsConnection && wsConnection.readyState === WebSocket.OPEN){
    // Send set_players with SWAPPED positions
    console.log('📤 Sending set_players with swapped colors');
    wsSend({
      type: 'set_players',
      white: currentBlack,  // Old Black becomes new White
      black: currentWhite   // Old White becomes new Black
    });
    
    // Then reset game
    setTimeout(() => {
      console.log('📤 Sending reset_game');
      wsSend({ type: 'reset_game' });
      showToast(`Colors swapped: ${currentWhite} vs ${currentBlack}`);
    }, 150);
  }
}

function swapInitialPlayers(){
  console.log('🔀 Swapping players in initial screen');
  console.log('   Before:', { black: initialBlackPlayer, white: initialWhitePlayer });
  
  // Swap the stored values
  const tempBlack = initialBlackPlayer;
  initialBlackPlayer = initialWhitePlayer;
  initialWhitePlayer = tempBlack;
  
  console.log('   After:', { black: initialBlackPlayer, white: initialWhitePlayer });
  
  // Update displays with animation
  updateInitialPlayerDisplay('black', initialBlackPlayer);
  updateInitialPlayerDisplay('white', initialWhitePlayer);
  
  showToast('Players swapped! ⚫↔⚪');
}

function cancelInitialSetup(){
  console.log('❌ Canceling initial setup - returning to current game');
  
  // Hide initial setup screen
  const setupScreen = document.getElementById('initialSetupScreen');
  if(setupScreen){
    setupScreen.classList.add('hidden');
    console.log('✅ Initial setup screen hidden');
  }
  
  // Remove class from body
  document.body.classList.remove('initial-setup-active');
  
  // Restore setup state (if there was a game)
  if(data && data.status){
    initialSetupComplete = true;
    console.log('✅ Returned to current game');
    showToast('Setup canceled');
  } else {
    // No game to return to - this should not happen if Cancel is properly hidden
    console.warn('⚠️  No current game to return to');
  }
  
  // Clear selection state
  initialSelectingFor = null;
}

function reopenInitialSetup(){
  console.log('🔄 Reopening initial setup screen');
  
  // Update default players with current players
  if(data && data.players){
    const currentBlack = data.players.black?.name || 'Human Player';
    const currentWhite = data.players.white?.name || 'LIGHTNING STRIKE';
    
    console.log('📝 Updating defaults with current players:', { currentBlack, currentWhite });
    initialBlackPlayer = currentBlack;
    initialWhitePlayer = currentWhite;
    
    // Update display
    updateInitialPlayerDisplay('black', currentBlack);
    updateInitialPlayerDisplay('white', currentWhite);
  }
  
  // Show initial setup screen
  const setupScreen = document.getElementById('initialSetupScreen');
  if(setupScreen){
    setupScreen.classList.remove('hidden');
    console.log('✅ Initial setup screen shown');
  }
  
  // Show Cancel button (since there's a game to return to)
  const cancelBtn = document.getElementById('initialCancelBtn');
  if(cancelBtn){
    cancelBtn.style.display = 'flex';
    console.log('✅ Cancel button shown');
  }
  
  // Add class to body for z-index
  document.body.classList.add('initial-setup-active');
  
  // Reset setup state
  initialSetupComplete = false;
  initialSelectingFor = null;
  
  console.log('✅ Ready to select new players');
}

function startGameWithPlayers(blackPlayer, whitePlayer){
  console.log('🚀 Starting game with players:');
  console.log('   ⚫ Black (left):', blackPlayer);
  console.log('   ⚪ White (right):', whitePlayer);
  
  // Hide initial setup screen
  const setupScreen = document.getElementById('initialSetupScreen');
  if(setupScreen){
    setupScreen.classList.add('hidden');
  }
  
  // Remove initial-setup-active class from body
  document.body.classList.remove('initial-setup-active');
  console.log('✅ Removed initial-setup-active class from body');
  
  initialSetupComplete = true;
  
  // Reset game state variables for new game
  gameOverInfo = null;
  aiAutoPaused = false;
  console.log('🔄 Reset gameOverInfo and aiAutoPaused for new game');
  
  // CORRECT ORDER: First init to create session, THEN set_players
  if(wsConnection && wsConnection.readyState === WebSocket.OPEN){
    // First send init to CREATE the session
    console.log('📤 Step 1: Sending init to create session');
    wsSend({
      type: 'init',
      session_id: SESSION_ID
    });
    
    // Then set players (after session exists)
    setTimeout(() => {
      console.log('📤 Step 2: Sending set_players to backend:');
      console.log('   Backend will assign:');
      console.log('   - white (plays second) ←', whitePlayer);
      console.log('   - black (plays first) ←', blackPlayer);
      wsSend({
        type: 'set_players',
        white: whitePlayer,
        black: blackPlayer
      });
    }, 200);
  }
}

// Initialize on page load
async function init(){
  console.log('🚀 init() called');
  
  // Load version and players cache (parallel)
  await Promise.all([
    loadVersion(),
    loadPlayersCache()
  ]);
  
  // Test WebSocket indicator visibility
  const indicator = document.getElementById('wsStatusIndicator');
  if (indicator) {
    console.log('WebSocket indicator found:', indicator);
    console.log('Indicator styles:', window.getComputedStyle(indicator));
  } else {
    console.error('WebSocket indicator NOT found!');
  }
  
  // Build board once
  buildBoard();
  
  // Setup WebSocket
  initWebSocket();
  
  // Toolbar setup (must be before initial screen)
  setupToolbar();
  setupTooltips();
  setupPlayersUI();
  
  // Initial setup screen - MUST wait for DOM to be fully ready
  console.log('⏰ Scheduling setupInitialScreen() for next tick...');
  setTimeout(() => {
    console.log('⏰ Now calling setupInitialScreen()...');
    setupInitialScreen();
  }, 100);
  
  // History grid setup
  setupHistoryDemo();
  
  // Coord sync setup
  setupCoordSync();
  
  // Keyboard shortcuts
  window.addEventListener('keydown', (e)=>{
    if(!data) return;
    const maxPly = (data?.positions?.length || 1) - 1;
    if(e.key==='ArrowLeft'){ if(ply>0){ ply--; render(); } }
    if(e.key==='ArrowRight'){ if(ply<maxPly){ ply++; render(); } }
  });
}

// Start when DOM is ready
window.addEventListener('DOMContentLoaded', async () => {
  // Load HTML templates first
  await loadTemplates();
  // Then initialize game
  init();
});

function setupHistoryDemo(){
  const histHead = document.getElementById('histHead');
  const histGrid = document.getElementById('historyGrid');
  const histBadge = document.getElementById('histBadge');
  const movesOl = document.getElementById('movesOl');
  
  window.buildHistory = function(){
    if(!data) return;
    if(!histGrid || !histHead) return;
    
    // Read moves from JSON
    const moves = data?.moves || [];
    
    histGrid.innerHTML='';
    
    if(moves.length === 0){
      // Show header and an empty-state row when there are no moves
      histHead.classList.remove('hidden');
      histGrid.classList.remove('hidden');
      const emptyRow = document.createElement('div');
      emptyRow.className = 'historyCell';
      emptyRow.style.gridColumn = '1 / -1';
      emptyRow.style.padding = '0.6rem 0.5rem';
      emptyRow.style.textAlign = 'center';
      emptyRow.style.color = 'var(--muted)';
      emptyRow.textContent = 'No moves yet';
      histGrid.appendChild(emptyRow);
      return;
    }
    
    let rowNo=1;
    const maxPly = (data?.positions?.length || 1) - 1;
    
    // Process moves in pairs (Black, White)
    for(let i=0; i<moves.length; i+=2){
      const b = moves[i] || '';
      const w = moves[i+1] || '';
      
      const row = document.createElement('div'); 
      row.className='historyRow'; 
      row.dataset.row=rowNo;
      
      const cNo = document.createElement('div'); 
      cNo.className='historyCell historyNo'; 
      cNo.textContent=rowNo;
      
      const cB = document.createElement('div'); 
      cB.className='historyCell historyMove'; 
      // Display passed moves as "-"
      cB.textContent = (b.toUpperCase() === 'PASSED' || b === '-') ? '—' : b;
      cB.title = `Move ${rowNo} (Black)`;
      cB.onclick = ()=>{ 
        const targetPly = (rowNo-1)*2 + 1; 
        if(targetPly<=maxPly){ 
          ply = targetPly; 
          render(); 
          highlightDemoRow(rowNo, /*isWhite*/false); 
        } 
      };
      
      const cW = document.createElement('div'); 
      cW.className='historyCell historyMove'; 
      // Display passed moves as "-"
      cW.textContent = (w.toUpperCase() === 'PASSED' || w === '-') ? '—' : w;
      cW.title = `Move ${rowNo} (White)`;
      cW.onclick = ()=>{ 
        const targetPly = (rowNo-1)*2 + 2; 
        if(targetPly<=maxPly){ 
          ply = targetPly; 
          render(); 
          highlightDemoRow(rowNo, /*isWhite*/true); 
        } 
      };
      
      row.appendChild(cNo); 
      row.appendChild(cB); 
      row.appendChild(cW); 
      histGrid.appendChild(row);
      rowNo++;
    }
    
    // Show history grid if there are moves
    histHead.classList.remove('hidden');
    histGrid.classList.remove('hidden');
    movesOl?.classList.add('hidden');
    
    // Highlight only the last move (most recent move)
    highlightLastMove(moves);
  }
  
  function highlightLastMove(moves){
    if(!histGrid || !moves || moves.length === 0) return;
    
    // Clear all active states
    histGrid.querySelectorAll('.historyMove').forEach(n=>n.classList.remove('active', 'last-move'));
    
    // Find the last non-empty move
    let lastNonEmptyIdx = moves.length - 1;
    while(lastNonEmptyIdx >= 0 && (!moves[lastNonEmptyIdx] || moves[lastNonEmptyIdx] === '' || moves[lastNonEmptyIdx] === '-')) {
      lastNonEmptyIdx--;
    }
    
    if(lastNonEmptyIdx >= 0) {
      const rowNo = Math.floor(lastNonEmptyIdx / 2) + 1;
      const isWhite = lastNonEmptyIdx % 2 === 1;
      const row = histGrid.querySelector(`.historyRow[data-row="${rowNo}"]`);
      if(row){ 
        const cell = row.children[isWhite?2:1]; 
        cell?.classList.add('active', 'last-move'); 
        row.scrollIntoView({block:'nearest'}); 
      }
    }
  }
  
  function highlightDemoRow(rowNo, isWhite){
    if(!histGrid) return;
    histGrid.querySelectorAll('.historyMove').forEach(n=>n.classList.remove('active'));
    const row = histGrid.querySelector(`.historyRow[data-row="${rowNo}"]`);
    if(row){ 
      const cell = row.children[isWhite?2:1]; 
      cell?.classList.add('active'); 
      row.scrollIntoView({block:'nearest'}); 
    }
  };
  
  buildHistory();
}

function setupCoordSync(){
  const rowsNums = document.querySelector('.rows-nums');
  const elBoard = document.getElementById('board');
  
  window.syncRowCoords = function(){
    if(!rowsNums || !elBoard) return;
    const PADDING = 12;
    const innerHeight = Math.max(0, elBoard.clientHeight - (PADDING*2));
    rowsNums.style.height = innerHeight + 'px';
    rowsNums.style.marginTop = PADDING + 'px';
    rowsNums.style.marginRight = '-18px';
  };
  
  window.syncRowCoords();
  const ro = new ResizeObserver(()=> window.syncRowCoords());
  ro.observe(elBoard);
  window.addEventListener('resize', window.syncRowCoords);
}

function setupToolbar(){
  const undoBtn = qs('undoBtn');
  const redoBtn = qs('redoBtn');
  const copyBtn = qs('copyBtn');
  const pasteBtn = qs('pasteBtn');
  const saveBtn = qs('saveBtn');
  const loadBtn = qs('loadBtn');
  const newBtn  = qs('newGameBtn');
  const swapPlayersBtn = qs('swapPlayersBtn');
  const setupPlayersBtn = qs('setupPlayersBtn');
  const fsBtn   = qs('fsBtn');
  const aiPlayPauseBtn = qs('aiPlayPauseBtn');
  const toggleOpeningBtn = qs('toggleOpeningBtn');
  // Don't access data here - it might not be loaded yet

  if (aiPlayPauseBtn) aiPlayPauseBtn.addEventListener('click', toggleAIPlayPause);
  if (toggleOpeningBtn) toggleOpeningBtn.addEventListener('click', toggleOpeningHints);
  if (undoBtn) undoBtn.addEventListener('click', ()=>{ if(wsConnection && wsConnection.readyState === WebSocket.OPEN){ wsSend({ type: 'undo' }); } });
  if (redoBtn) redoBtn.addEventListener('click', ()=>{ if(wsConnection && wsConnection.readyState === WebSocket.OPEN){ wsSend({ type: 'redo' }); } });
  if (copyBtn) copyBtn.addEventListener('click', async ()=>{ 
    const text = getCompactHistory();
    const ok = await copyTextStrict(text);
    showToast(ok ? `Copied: ${text || '—'}` : 'Copy failed');
  });
  if (pasteBtn){
    console.log('✅ Paste button found in DOM, registering click handler');
    pasteBtn.addEventListener('click', async (e)=>{
      console.log('🔵 PASTE BUTTON CLICKED - starting paste operation');
      e.preventDefault();
      e.stopPropagation();
      
      let text = null;
      
      // Try clipboard API first
      try{
        console.log('Attempting to read from clipboard API...');
        text = await navigator.clipboard.readText();
        console.log('✅ Read from clipboard successfully:', text);
      }catch(e){
        console.warn('❌ Clipboard API failed:', e.message);
        console.log('Falling back to manual prompt...');
      }
      
      // Fallback: prompt user to paste manually
      if(!text || text.trim().length === 0){
        console.log('Opening prompt for manual paste...');
        text = prompt('Paste compact history:\n\nFormat: "C4e3F6e6F4c5" (uppercase=Black, lowercase=White)');
        console.log('User input from prompt:', text, 'Type:', typeof text);
        if(text === null || text === undefined){
          console.log('User cancelled prompt (null/undefined)');
          showToast('Paste cancelled');
          return;
        }
        if(text.trim().length === 0){
          console.log('User provided empty string');
          showToast('No input provided');
          return;
        }
      }
      
      const trimmed = text.trim();
      console.log('Trimmed input:', trimmed, 'Length:', trimmed.length);
      
      // Validate and extract moves
      const moves = trimmed.match(/[A-Ha-h][1-8]/g);
      console.log('Extracted moves:', moves, 'Count:', moves?.length);
      
      if(!moves || moves.length === 0){
        console.error('No valid moves found');
        showToast('❌ No valid moves found');
        alert('No valid moves found.\n\nExpected: "C4e3F6e6F4c5"\nGot: "' + trimmed + '"');
        return;
      }
      
      const cleanHistory = moves.join('');
      console.log('Clean history to send:', cleanHistory);
      
      // Load via WebSocket
      if(wsConnection && wsConnection.readyState === WebSocket.OPEN){
        console.log('✅ WebSocket open, sending load_history');
        wsSend({ type:'load_history', history: cleanHistory });
        showToast('📥 Loading game...');
        console.log('Load history sent, waiting for response...');
      } else {
        console.error('❌ WebSocket not connected, state:', wsConnection?.readyState);
        showToast('❌ Not connected');
        alert('WebSocket not connected. Reload the page and try again.');
      }
    });
  } else {
    console.error('❌ Paste button NOT found in DOM!');
  }
  if (saveBtn) saveBtn.addEventListener('click', ()=>{
    // Save in XOT format (eXtended Othello Transcript)
    const xotContent = generateXOT();
    if(!xotContent){ 
      showToast('Nothing to save'); 
      return; 
    }
    
    // Generate filename with timestamp
    const now = new Date();
    const timestamp = now.toISOString()
      .replace(/[T:]/g, '_')
      .replace(/\..+/, '')
      .replace(/-/g, '');
    const filename = `reversi42_${timestamp}.xot`;
    
    const blob = new Blob([xotContent], {type:'text/plain'});
    const a = document.createElement('a'); 
    a.href = URL.createObjectURL(blob); 
    a.download = filename;
    a.click();
    setTimeout(()=>URL.revokeObjectURL(a.href), 1000);
    
    showToast(`💾 Saved: ${filename}`);
    console.log('Game saved in XOT format:', filename);
  });
  if (loadBtn) loadBtn.addEventListener('click', ()=>{
    const inp = document.createElement('input'); 
    inp.type='file'; 
    inp.accept='.xot,.r42,.rev,.txt,text/plain'; // Accept XOT and legacy formats
    
    inp.onchange = async ()=>{
      const file = inp.files?.[0]; 
      if(!file) return;
      
      try{
        const fileContent = await file.text();
        const format = detectFileFormat(fileContent);
        
        console.log(`📂 Loading file: ${file.name}, detected format: ${format}`);
        
        let historyToLoad = '';
        let metadata = null;
        
        if(format === 'xot'){
          // Parse XOT format
          const parsed = parseXOT(fileContent);
          if(parsed){
            historyToLoad = parsed.history;
            metadata = parsed.metadata;
            console.log('XOT metadata:', metadata);
            showToast(`📖 Loading XOT: ${metadata.black} vs ${metadata.white}`);
          } else {
            throw new Error('Invalid XOT format');
          }
        } else if(format === 'compact'){
          // Extract compact history
          historyToLoad = fileContent.trim();
          showToast('📖 Loading compact format...');
        } else {
          throw new Error('Unknown file format');
        }
        
        // Send to backend
        if(wsConnection && wsConnection.readyState === WebSocket.OPEN){
          wsSend({ type:'load_history', history: historyToLoad });
          wsSend({ type:'get_state' });
          
          // TODO: If XOT has player names, we could set them too
          // This would require a new backend message type
        } else {
          showToast('❌ Not connected');
        }
        
      }catch(e){ 
        console.error('Load file error:', e); 
        showToast(`❌ Load failed: ${e.message}`);
        alert(`Failed to load file:\n\n${e.message}\n\nSupported formats:\n- XOT (.xot)\n- Compact (.rev, .r42)`);
      }
    }; 
    
    inp.click();
  });
  if (newBtn) newBtn.addEventListener('click', ()=>{
    if(wsConnection && wsConnection.readyState === WebSocket.OPEN){
      // Reset game over state immediately to prevent AI blocking
      gameOverInfo = null;
      aiAutoPaused = false;
      wsConnection.send(JSON.stringify({ type: 'reset_game' }));
    }
  });
  
  if (swapPlayersBtn) swapPlayersBtn.addEventListener('click', ()=>{
    console.log('🔄 Swap Players button clicked - inverting colors');
    swapPlayersAndRestart();
  });
  
  if (setupPlayersBtn) setupPlayersBtn.addEventListener('click', ()=>{
    console.log('🔄 Setup Players button clicked - reopening initial screen');
    reopenInitialSetup();
  });
  
  if (fsBtn) fsBtn.addEventListener('click', ()=>{ if(!document.fullscreenElement){ document.documentElement.requestFullscreen?.(); } else { document.exitFullscreen?.(); } });
}

function setupTooltips(){
  const tip = document.createElement('div');
  tip.id = 'globalTooltip';
  document.body.appendChild(tip);
  function show(el){
    const text = el.getAttribute('data-tip');
    if(!text) return;
    tip.textContent = text;
    tip.style.display = 'block';
    position(el);
  }
  function hide(){ tip.style.display = 'none'; }
  function position(el){
    const r = el.getBoundingClientRect();
    const pad = 8;
    const x = r.left + r.width/2;
    const y = r.top - pad;
    const tw = tip.offsetWidth; const th = tip.offsetHeight;
    let left = Math.round(x - tw/2);
    let top  = Math.round(y - th);
    // clamp within viewport
    left = Math.min(Math.max(8, left), window.innerWidth - tw - 8);
    top  = Math.max(8, top);
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }
  const targets = document.querySelectorAll('.btn[data-tip], .miniIconBtn[data-tip]');
  targets.forEach(el=>{
    el.addEventListener('mouseenter', ()=>show(el));
    el.addEventListener('mouseleave', hide);
    el.addEventListener('mousemove', ()=>position(el));
    window.addEventListener('scroll', ()=>{ if(tip.style.display==='block') position(el); }, true);
    window.addEventListener('resize', ()=>{ if(tip.style.display==='block') position(el); });
  });
}

function setupPlayersUI(){
  const overlay = document.getElementById('playersModal');
  const closeBtn = document.getElementById('playersCloseBtn');
  const btnB = document.getElementById('changeBlackBtn');
  const btnW = document.getElementById('changeWhiteBtn');
  const list = document.getElementById('playersList');
  const title = document.getElementById('playersTitle');
  const subtitle = document.getElementById('playersSubtitle');
  let currentSide = 'W';

  // Players loaded ONLY from API - NO hardcoded data
  let AVAILABLE_PLAYERS = [];
  let playersLoaded = false;
  
  // Active filters for tags
  let activeTagFilters = new Set();
  
  // Toggle tag filter
  function toggleTagFilter(tagName){
    if(activeTagFilters.has(tagName)){
      activeTagFilters.delete(tagName);
    } else {
      activeTagFilters.add(tagName);
    }
    updateFilters();
  }
  
  // Update filtered cards based on active tags
  function updateFilters(){
    const cards = list.querySelectorAll('.playerCard');
    let visibleCount = 0;
    
    cards.forEach(card => {
      if(activeTagFilters.size === 0){
        // No filters active - show all
        card.classList.remove('filtered-out');
        visibleCount++;
      } else {
        // Check if card has any of the active tags
        const cardTags = card.dataset.tags ? card.dataset.tags.split('|') : [];
        const hasActiveTag = cardTags.some(tag => activeTagFilters.has(tag));
        
        if(hasActiveTag){
          card.classList.remove('filtered-out');
          visibleCount++;
        } else {
          card.classList.add('filtered-out');
        }
      }
    });
    
    // Update filter controls
    updateFilterControls(visibleCount, cards.length);
    
    // Update active state on ALL tags (configTag and playerTag)
    document.querySelectorAll('.configTag, .playerTag').forEach(tagEl => {
      const tagName = tagEl.dataset.tag;
      if(tagName && activeTagFilters.has(tagName)){
        tagEl.classList.add('active');
      } else {
        tagEl.classList.remove('active');
      }
    });
  }
  
  // Update filter controls UI
  function updateFilterControls(visibleCount, totalCount){
    let controlsDiv = document.getElementById('filterControls');
    if(!controlsDiv){
      controlsDiv = document.createElement('div');
      controlsDiv.id = 'filterControls';
      controlsDiv.className = 'filterControls';
      list.parentElement.insertBefore(controlsDiv, list);
    }
    
    const hasFilters = activeTagFilters.size > 0;
    const filterNames = Array.from(activeTagFilters).join(', ');
    
    controlsDiv.innerHTML = `
      <div class="filterInfo">
        <span>Showing <span class="filterCount">${visibleCount}</span> of ${totalCount} players</span>
        ${hasFilters ? `<span style="color:rgba(59,130,246,.8)">• Filters: ${filterNames}</span>` : ''}
      </div>
      <button class="clearFiltersBtn" onclick="clearAllFilters()" ${!hasFilters ? 'disabled' : ''}>
        ✕ Clear Filters
      </button>
    `;
    
    controlsDiv.style.display = hasFilters || visibleCount !== totalCount ? 'flex' : 'none';
  }
  
  // Clear all filters
  window.clearAllFilters = function(){
    activeTagFilters.clear();
    updateFilters();
  };
  
  // Load players from API - ONLY source of truth
  async function loadPlayersFromAPI(){
    if(playersLoaded) return;
    
    try{
      console.log('📡 Loading players from API (YAML configs)...');
      const response = await fetch('http://localhost:8000/api/players');
      
      if(!response.ok){
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if(data.error){
        throw new Error(data.error);
      }
      
      if(!data.players || !Array.isArray(data.players)){
        throw new Error('Invalid API response format');
      }
      
      AVAILABLE_PLAYERS = data.players.map(p => ({
        name: p.name,
        desc: p.description,
        headline: p.headline,
        tag: p.tag,
        icon: p.icon,
        category: p.category,
        directory: p.directory,  // NEW: Directory tag from file location
        elo: p.elo,
        stats: p.stats,  // null for human players
        avatar_url: p.avatar_url,
        config_tags: p.config_tags || []  // Already includes directory tag as first element
      }));
      
      playersLoaded = true;
      console.log(`✅ Loaded ${AVAILABLE_PLAYERS.length} players from YAML configs`);
      console.log('Players with avatars:', AVAILABLE_PLAYERS.filter(p => p.avatar_url).map(p => `${p.name}: ${p.avatar_url}`));
      
    } catch(error){
      console.error('❌ Failed to load players from API:', error);
      console.error('Please ensure the server is running on http://localhost:8000');
      
      // Show user-friendly error
      showToast('Failed to load players. Check server connection.');
      
      // Re-throw to prevent showing empty list
      throw error;
    }
  }

  async function renderPlayers(side){
    if(!list) return;
    
    // Load players if not yet loaded
    try{
      await loadPlayersFromAPI();
    } catch(error){
      // Show error message in list
      list.innerHTML = `
        <div style="grid-column:1/-1; text-align:center; padding:40px; color:rgba(255,255,255,.6)">
          <div style="font-size:48px; margin-bottom:16px">⚠️</div>
          <div style="font-size:18px; font-weight:700; margin-bottom:8px; color:var(--txt)">Failed to Load Players</div>
          <div style="font-size:13px; margin-bottom:16px">Please ensure the server is running on port 8000</div>
          <div style="font-size:12px; font-family:monospace; color:rgba(255,68,68,.8)">${error.message}</div>
        </div>
      `;
      return;
    }
    
    list.innerHTML = '';
    
    // Check if we have players
    if(AVAILABLE_PLAYERS.length === 0){
      list.innerHTML = `
        <div style="grid-column:1/-1; text-align:center; padding:40px; color:rgba(255,255,255,.6)">
          <div style="font-size:48px; margin-bottom:16px">🎮</div>
          <div style="font-size:18px; font-weight:700; margin-bottom:8px; color:var(--txt)">No Players Found</div>
          <div style="font-size:13px">Check your YAML configuration files</div>
        </div>
      `;
      return;
    }
    
    // Update subtitle based on side
    if(subtitle){
      subtitle.textContent = side === 'B' ? 'Choose Black Player · Dark Side' : 'Choose White Player · Light Side';
    }
    
    // Sort players: Human first, then AI by ELO descending
    const sortedPlayers = [...AVAILABLE_PLAYERS].sort((a, b) => {
      // Human always first
      if(a.tag === 'HUMAN') return -1;
      if(b.tag === 'HUMAN') return 1;
      // Then by ELO descending
      return (b.elo || 0) - (a.elo || 0);
    });
    
    const frag = document.createDocumentFragment();
    sortedPlayers.forEach(p=>{
      const card = document.createElement('div');
      card.className = 'playerCard';
      
      // Add type and category classes
      if(p.tag === 'HUMAN') card.classList.add('human');
      if(p.tag === 'AI') card.classList.add('ai');
      if(p.category) card.classList.add(p.category);
      
      // Generate avatar content (image or initials)
      const initials = p.name.split(/\s+/).map(w => w[0]).join('').slice(0,2).toUpperCase();
      let avatarContent = initials;
      if(p.avatar_url){
        console.log(`Loading avatar for ${p.name}: ${p.avatar_url}`);
        avatarContent = `<img src="${p.avatar_url}" alt="${p.name}" style="display:block" onerror="console.error('Avatar failed for ${p.name}:', this.src); this.style.display='none'; this.parentElement.innerHTML='${initials}';">`;
      }
      
      // Build stats HTML (only for AI players with stats)
      const statsHTML = (p.stats && p.tag !== 'HUMAN') ? `
        <div class="playerStats">
          <div class="statRow">
            <div class="statLabel">Power</div>
            <div class="statBarContainer">
              <div class="statBar power" style="width:${p.stats.power * 10}%"></div>
            </div>
            <div class="statValue">${p.stats.power}</div>
          </div>
          <div class="statRow">
            <div class="statLabel">Speed</div>
            <div class="statBarContainer">
              <div class="statBar speed" style="width:${p.stats.speed * 10}%"></div>
            </div>
            <div class="statValue">${p.stats.speed}</div>
          </div>
          <div class="statRow">
            <div class="statLabel">Accuracy</div>
            <div class="statBarContainer">
              <div class="statBar accuracy" style="width:${p.stats.accuracy * 10}%"></div>
            </div>
            <div class="statValue">${p.stats.accuracy}</div>
          </div>
          <div class="statRow">
            <div class="statLabel">Depth</div>
            <div class="statBarContainer">
              <div class="statBar depth" style="width:${p.stats.depth * 10}%"></div>
            </div>
            <div class="statValue">${p.stats.depth}</div>
          </div>
          <div class="statRow">
            <div class="statLabel">Lethality</div>
            <div class="statBarContainer">
              <div class="statBar lethality" style="width:${p.stats.lethality * 10}%"></div>
            </div>
            <div class="statValue">${p.stats.lethality}</div>
          </div>
        </div>
      ` : '';
      
      // Build meta HTML
      const metaHTML = `
        <div class="playerMeta">
          ${p.elo ? `<div class="playerElo">ELO ${p.elo}</div>` : '<div style="color:rgba(255,255,255,.4); font-style:italic; font-size:11px">Human Player</div>'}
          <div class="playerCategory">${p.category || 'Unknown'}</div>
        </div>
      `;
      
      // Build config tags HTML with click handlers
      const configTagsHTML = (p.config_tags && p.config_tags.length > 0) ? `
        <div class="playerConfigTags">
          ${p.config_tags.map(tag => `<div class="configTag" data-tag="${tag}">${tag}</div>`).join('')}
        </div>
      ` : '';
      
      // Store all tags in data attribute for filtering (include category and config tags)
      const allTags = [];
      if(p.category) allTags.push(p.category);
      if(p.tag) allTags.push(p.tag);
      if(p.config_tags) allTags.push(...p.config_tags);
      card.dataset.tags = allTags.join('|');
      
      // Config button (only for AI players) - placed at bottom
      const configButtonHTML = p.tag !== 'HUMAN' ? `
        <div class="playerConfigBtn" data-player="${p.name}" title="View Configuration">
          <svg viewBox="0 0 24 24">
            <path d="M7 4 Q5 12 7 20"/>
            <path d="M17 4 Q19 12 17 20"/>
            <line x1="7" y1="7" x2="17" y2="7" stroke-width="2.5"/>
            <line x1="7" y1="12" x2="17" y2="12" stroke-width="2.5"/>
            <line x1="7" y1="17" x2="17" y2="17" stroke-width="2.5"/>
            <circle cx="7" cy="4" r="1.8" fill="currentColor"/>
            <circle cx="17" cy="4" r="1.8" fill="currentColor"/>
            <circle cx="7" cy="20" r="1.8" fill="currentColor"/>
            <circle cx="17" cy="20" r="1.8" fill="currentColor"/>
          </svg>
          <span>View Config</span>
        </div>
      ` : '';
      
      card.innerHTML = `
        ${p.icon ? `<div class="playerIcon">${p.icon}</div>` : ''}
        <div class="playerCardHeader">
          <div class="playerAvatar ${p.tag === 'HUMAN' ? 'human' : (p.category || 'ai')}">${avatarContent}</div>
          <div class="playerInfo">
            <div class="playerName">${p.name}</div>
            ${p.headline ? `<div class="playerHeadline">${p.headline}</div>` : ''}
            <div class="playerTags">
              <div class="playerTag ${p.tag === 'HUMAN' ? 'human' : 'ai'}" data-tag="${p.tag}">${p.tag}</div>
              ${p.category ? `<div class="playerTag ${p.category}" data-tag="${p.category}">${p.category}</div>` : ''}
            </div>
          </div>
        </div>
        <div class="playerDesc">${p.desc}</div>
        ${configTagsHTML}
        ${statsHTML}
        ${metaHTML}
        ${configButtonHTML}
      `;
      
      // Add click handler for player selection (not on tags or config button)
      card.addEventListener('click', (e)=> {
        // If clicking on config button, open config viewer
        if(e.target.closest('.playerConfigBtn')){
          e.stopPropagation();
          const configBtn = e.target.closest('.playerConfigBtn');
          const playerName = configBtn.dataset.player;
          if(playerName && typeof openAIConfig === 'function'){
            console.log(`Opening config for ${playerName}`);
            openAIConfig(playerName);
          }
          return;
        }
        
        // If clicking on any tag (configTag or playerTag), handle filter instead
        if(e.target.classList.contains('configTag') || e.target.classList.contains('playerTag')){
          e.stopPropagation();
          const tagName = e.target.dataset.tag;
          if(tagName){
            toggleTagFilter(tagName);
          }
        } else {
          applySelection(side, p);
        }
      });
      
      frag.appendChild(card);
    });
    list.appendChild(frag);
    
    // Initialize filter controls (hidden by default)
    updateFilterControls(sortedPlayers.length, sortedPlayers.length);
  }

  function open(side){
    currentSide = side || 'W';
    if(title){ 
      title.textContent = currentSide === 'B' ? 'Select Black Player' : 'Select White Player';
    }
    
    // Reset filters when opening modal
    activeTagFilters.clear();
    
    renderPlayers(currentSide);
    if(overlay){ overlay.style.display = 'flex'; }
  }
  function close(){ if(overlay){ overlay.style.display = 'none'; } }

  async function applySelection(side, player){
    try{
      console.log('🎯 applySelection called:', {
        side, 
        playerName: player.name,
        initialSetupComplete,
        initialSelectingFor
      });
      
      // If we're in initial setup phase, update the initial screen instead
      if(!initialSetupComplete){
        console.log('✅ In initial setup phase - updating initial screen');
        // Convert side 'B'/'W' to 'black'/'white'
        const sideForInitial = (side === 'B') ? 'black' : 'white';
        console.log(`   Converting side ${side} to ${sideForInitial}`);
        await updateInitialPlayerDisplay(sideForInitial, player.name);
        close();
        initialSelectingFor = null;
        return;
      }
      
      // Update UI immediately
      if(!data) data = {};
      if(!data.players) data.players = { black:{}, white:{} };
      if(side==='B'){
        data.players.black.name = player.name;
        data.players.black.avatar = initials(player.name);
        data.players.black.avatar_url = player.avatar_url;  // FIX: Copy avatar_url
        data.players.black.icon = player.icon;  // FIX: Copy icon
      } else {
        data.players.white.name = player.name;
        data.players.white.avatar = initials(player.name);
        data.players.white.avatar_url = player.avatar_url;  // FIX: Copy avatar_url
        data.players.white.icon = player.icon;  // FIX: Copy icon
      }
      render();

      // Send players config to backend (supports Human/AI for both sides)
      const whiteChoice = (side==='W' ? player.name : (data.players.white?.name || 'Human'));
      const blackChoice = (side==='B' ? player.name : (data.players.black?.name || 'Human'));
      const payload = { type:'set_players', white: whiteChoice, black: blackChoice };
      if(side==='W' && player.tag==='AI'){ pendingSelectedAI = player.name; showToast(`Loading ${player.name}...`); }
      wsSend(payload);
    }catch(e){ console.error('applySelection error', e); }
    finally{ close(); }
  }

  btnB?.addEventListener('click', ()=> open('B'));
  btnW?.addEventListener('click', ()=> open('W'));
  closeBtn?.addEventListener('click', close);
  overlay?.addEventListener('click', (e)=>{ if(e.target === overlay) close(); });
  window.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') close(); });
  
  // Expose open function globally for initial setup screen
  window.openPlayersModal = open;
}

function showToast(msg){
  let t = document.getElementById('toast');
  if(!t){ t = document.createElement('div'); t.id='toast'; document.body.appendChild(t); }
  t.textContent = msg;
  t.style.display = 'block';
  clearTimeout(showToast._tid);
  showToast._tid = setTimeout(()=>{ t.style.display='none'; }, 1500);
}

function render(){
  try {
    if(!data) {
      console.log('No data to render yet');
      return; // Don't render if data is not loaded
    }
    
    const elBoard = document.getElementById('board');
    const movesOl = document.getElementById('movesOl');
    
    if(!elBoard) {
      console.error('❌ Board element not found!');
      return;
    }
  
  // keep rows numbers aligned after any layout change
  try{ window.syncRowCoords(); }catch(_){}
  const turn = (data.status?.turn_by_ply && data.status.turn_by_ply[ply]) || (ply%2===0 ? 'B':'W');
  // ensure partial resets on jump/undo/redo safely
  if(typeof partial!=='undefined'){
    if(typeof lastTurn==='undefined' || lastTurn===null) lastTurn = turn;
    if(turn !== lastTurn){ partial[turn]=0; lastTurn = turn; }
  }
  // Update turn indicators on player sides (show/hide dots and chip borders)
  const p1TurnDot = qs('p1TurnDot');
  const p2TurnDot = qs('p2TurnDot');
  const p1TurnChip = qs('p1Turn');
  const p2TurnChip = qs('p2Turn');
  
  if(gameOverInfo){
    // Hide both turn indicators on game over
    if(p1TurnDot) p1TurnDot.style.display = 'none';
    if(p2TurnDot) p2TurnDot.style.display = 'none';
    if(p1TurnChip) p1TurnChip.style.opacity = '0';
    if(p2TurnChip) p2TurnChip.style.opacity = '0';
  } else {
    // Show turn dot and chip only on the active player's side
    if(turn === 'B'){
      if(p1TurnDot) p1TurnDot.style.display = 'inline-block';
      if(p2TurnDot) p2TurnDot.style.display = 'none';
      if(p1TurnChip) p1TurnChip.style.opacity = '1';
      if(p2TurnChip) p2TurnChip.style.opacity = '0';
    } else {
      if(p1TurnDot) p1TurnDot.style.display = 'none';
      if(p2TurnDot) p2TurnDot.style.display = 'inline-block';
      if(p1TurnChip) p1TurnChip.style.opacity = '0';
      if(p2TurnChip) p2TurnChip.style.opacity = '1';
    }
  }
  // removed move number display from header

  // Board position
  const s = normalize64(data.positions?.[ply]);
  for(let i=0;i<64;i++){
    const inner = elBoard.children[i].firstElementChild;
    inner.innerHTML='';
    if(s[i]==='B' || s[i]==='W'){
      const d=document.createElement('div'); d.className='disc '+(s[i]==='B'?'black':'white'); inner.appendChild(d);
    }
  }

  // Remove all last-move indicators from all cell-contents
  elBoard.querySelectorAll('.last-move-indicator').forEach(el => {
    el.classList.remove('last-move-indicator');
  });
  
  // Also remove from all cells (in case it was added to cell instead of cell-content)
  [...elBoard.children].forEach(cell => {
    cell.classList.remove('last-move-indicator');
  });
  
  // Valid moves
  const vm = (data.valid_by_ply?.[ply]) || [];
  vm.map(coordToIdx).forEach(i=>{
    const dot=document.createElement('div'); dot.className='valid';
    elBoard.children[i].firstElementChild.appendChild(dot);
  });
  
  // Clear previous opening overlays (badges and opening rings)
  elBoard.querySelectorAll('.book-move-badge').forEach(el=>el.remove());
  elBoard.querySelectorAll('.hint[data-__om="1"]').forEach(el=>el.remove());

  // Opening book moves with variant count (draw only if also valid now AND showOpeningHints is true)
  const openingMoves = (data.opening_by_ply || []);
  const validSetNow = new Set(vm.map(String));
  if(showOpeningHints && Array.isArray(openingMoves) && openingMoves.length > 0) {
    openingMoves.forEach(obj => {
      if(obj && obj.move) {
        const idx = coordToIdx(obj.move);
        const cell = elBoard.children[idx];
        // guard: only draw if this opening move is valid now
        if(!validSetNow.has(String(obj.move).toUpperCase())) return;
        if(cell && cell.firstElementChild) {
          // Add opening highlight ring
          const ring = document.createElement('div');
          ring.className = 'hint';
          ring.dataset.__om = '1';
          ring.textContent = '';
          cell.firstElementChild.appendChild(ring);
          // Add variant count badge
          const badge = document.createElement('div');
          badge.className = 'book-move-badge';
          const v = Number(obj.variants || 0);
          const small = window.matchMedia && window.matchMedia('(max-width: 480px)').matches;
          const displayV = (small && v > 99) ? '99+' : String(v);
          badge.textContent = displayV; // only number on board
          badge.title = `${obj.move} · ${v} variant(s) in opening book`;
          cell.firstElementChild.appendChild(badge);
        }
      }
    });
  }
  
  // Highlight last move with elegant red dot
  if(data.moves && data.moves.length > 0) {
    const lastMove = data.moves[data.moves.length - 1];
    const lastMoveIdx = coordToIdx(lastMove);
    const cell = elBoard.children[lastMoveIdx];
    if(cell) {
      const cellContent = cell.firstElementChild; // Get cell-content
      if(cellContent) {
        cellContent.classList.add('last-move-indicator');
      }
    }
  }

  // Counts + delta
  const counts = countBW(s); 
  qs('p1Count').textContent = `● ${counts.b}`; 
  qs('p2Count').textContent = `○ ${counts.w}`;
  const adv = counts.b - counts.w; 
  setDelta('p1Delta', adv); 
  setDelta('p2Delta', -adv);

  // Toggle Undo/Redo availability using server-provided flags when available
  const st = data.status || {};
  const open = !!(wsConnection && wsConnection.readyState === WebSocket.OPEN);
  const undoBtnEl = qs('undoBtn');
  if(undoBtnEl){
    const canUndo = (st.can_undo !== undefined) ? !!st.can_undo : (Array.isArray(data.moves) && data.moves.length > 0);
    undoBtnEl.disabled = !(open && canUndo);
  }
  const redoBtnEl = qs('redoBtn');
  if(redoBtnEl){
    const canRedo = (st.can_redo !== undefined) ? !!st.can_redo : false;
    redoBtnEl.disabled = !(open && canRedo);
  }
  // Always allow saving (even empty game saves as empty history)
  const saveBtnEl = qs('saveBtn');
  if(saveBtnEl){ saveBtnEl.disabled = false; }

  // highlight (removed ply display) 
  if(movesOl){
    [...movesOl.children].forEach(li=> li.classList.remove('active'));
    if(ply>0){ const li = [...movesOl.children].find(el => +el.dataset.ply === ply);         if(li) li.classList.add('active'); }
  }
  } catch (error) {
    console.error('❌ CRITICAL ERROR in render():', error);
    console.error('Stack trace:', error.stack);
    console.error('Current data:', data);
  }
}

/* ========================================
   GLOBAL EXPORTS - Reusable Functions
   ======================================== */
window.reloadGameData = loadGameData;

/* ========================================
   UTILITY FUNCTIONS - DOM & Helpers
   ======================================== */
function qs(id){ return document.getElementById(id); }
function idx(r,c){ return r*8 + c; }
function coordToIdx(coord){ const L='ABCDEFGH'; const c=L.indexOf(String(coord).toUpperCase()[0]); const r=parseInt(String(coord).slice(1),10)-1; return r*8 + c; }
function initials(name){ return (name||'').trim().split(/\s+/).map(s=>s[0]).join('').slice(0,2).toUpperCase() || '?'; }

/* ========================================
   GAME FORMAT - Import/Export Functions
   ======================================== */
function buildCompactHistoryFromMoves(moves){
  if(!Array.isArray(moves)) return '';
  return moves.map((m,i)=> i%2===0 ? String(m).toUpperCase() : String(m).toLowerCase()).join('');
}
function getCompactHistory(){
  if(data && typeof data.history_compact === 'string' && data.history_compact.length>0) return data.history_compact;
  return buildCompactHistoryFromMoves(data?.moves);
}

// === XOT FORMAT SUPPORT ===

function generateXOT(){
  /**
   * Generate XOT (eXtended Othello Transcript) format file content
   * Returns a complete XOT file as string
   */
  if(!data) return null;
  
  const now = new Date();
  const timestamp = now.toISOString().replace('T', ' ').substring(0, 19);
  const blackName = data.players?.black?.name || 'Human';
  const whiteName = data.players?.white?.name || 'Human';
  const turn = data.status?.turn_by_ply?.[0] || 'B';
  const blackScore = data.status?.black_count || 2;
  const whiteScore = data.status?.white_count || 2;
  const size = 8;
  const history = getCompactHistory();
  const moveCount = history ? Math.floor(history.length / 2) : 0;
  
  // Get board state (current position)
  const boardPos = data.positions?.[data.positions.length - 1] || data.positions?.[0];
  const board64 = normalize64(boardPos);
  
  let xot = [];
  xot.push('# Reversi42 Game Save - XOT Format v1.0');
  xot.push(`# Saved: ${timestamp}`);
  xot.push('');
  xot.push('[GAME]');
  xot.push(`Black=${blackName}`);
  xot.push(`White=${whiteName}`);
  xot.push(`Turn=${turn}`);
  xot.push(`BlackScore=${blackScore}`);
  xot.push(`WhiteScore=${whiteScore}`);
  xot.push(`Size=${size}`);
  xot.push('');
  xot.push('[MOVES]');
  xot.push(`History=${history}`);
  xot.push(`Count=${moveCount}`);
  xot.push('');
  xot.push('[BOARD]');
  
  // Board state - 8 rows of 8 characters
  for(let row = 0; row < 8; row++){
    let rowStr = '';
    for(let col = 0; col < 8; col++){
      const idx = row * 8 + col;
      rowStr += board64[idx];
    }
    xot.push(rowStr);
  }
  xot.push('');
  
  return xot.join('\n');
}

function parseXOT(content){
  /**
   * Parse XOT format file content
   * Returns { history, metadata } or null if not XOT format
   */
  if(!content || typeof content !== 'string') return null;
  
  // Check if it's XOT format (must start with # Reversi42 or contain [GAME])
  if(!content.includes('[GAME]') && !content.includes('# Reversi42')) {
    return null; // Not XOT format
  }
  
  const lines = content.split('\n').map(l => l.trim());
  let history = '';
  let metadata = {
    black: 'Human',
    white: 'Human',
    turn: 'B',
    blackScore: 2,
    whiteScore: 2,
    size: 8
  };
  
  let currentSection = null;
  
  for(const line of lines){
    // Skip comments and empty lines
    if(!line || line.startsWith('#')) continue;
    
    // Section headers
    if(line.startsWith('[')){
      if(line.includes('[GAME]')) currentSection = 'game';
      else if(line.includes('[MOVES]')) currentSection = 'moves';
      else if(line.includes('[BOARD]')) currentSection = 'board';
      continue;
    }
    
    // Parse based on current section
    if(currentSection === 'game'){
      if(line.startsWith('Black=')) metadata.black = line.substring(6);
      else if(line.startsWith('White=')) metadata.white = line.substring(6);
      else if(line.startsWith('Turn=')) metadata.turn = line.substring(5);
      else if(line.startsWith('BlackScore=')) metadata.blackScore = parseInt(line.substring(11)) || 2;
      else if(line.startsWith('WhiteScore=')) metadata.whiteScore = parseInt(line.substring(11)) || 2;
      else if(line.startsWith('Size=')) metadata.size = parseInt(line.substring(5)) || 8;
    }
    else if(currentSection === 'moves'){
      if(line.startsWith('History=')) history = line.substring(8);
    }
    // Board section is optional, we ignore it (we replay from history)
  }
  
  return {
    history: history,
    metadata: metadata
  };
}

function detectFileFormat(content){
  /**
   * Auto-detect file format: 'xot', 'compact', or 'unknown'
   */
  if(!content || typeof content !== 'string') return 'unknown';
  
  const trimmed = content.trim();
  
  // Check for XOT format markers
  if(trimmed.includes('[GAME]') || trimmed.includes('[MOVES]') || trimmed.startsWith('# Reversi42')){
    return 'xot';
  }
  
  // Check for compact format (only move notation, no metadata)
  // Compact format: C4e3F6e6F4c5... (letters + numbers only)
  const compactRegex = /^[A-Ha-h][1-8]+$/;
  if(compactRegex.test(trimmed)){
    return 'compact';
  }
  
  // If it contains valid moves but with extra characters, try to extract
  const moves = trimmed.match(/[A-Ha-h][1-8]/g);
  if(moves && moves.length > 0){
    return 'compact'; // Probably compact with extra formatting
  }
  
  return 'unknown';
}
function normalize64(pos){ 
  // Support both formats: string (legacy) and coordinate object (new)
  if(typeof pos === 'string'){
    const raw = (pos||'').trim(); 
    if(raw.length!==64){ 
      const a = Array(64).fill('.'); a[27]='W'; a[28]='B'; a[35]='B'; a[36]='W'; 
      return a; 
    } 
    return raw.split(''); 
  }
  // Convert coordinate object to 64-char array
  if(typeof pos === 'object' && pos !== null){
    const coords = ['A1','B1','C1','D1','E1','F1','G1','H1','A2','B2','C2','D2','E2','F2','G2','H2',
                    'A3','B3','C3','D3','E3','F3','G3','H3','A4','B4','C4','D4','E4','F4','G4','H4',
                    'A5','B5','C5','D5','E5','F5','G5','H5','A6','B6','C6','D6','E6','F6','G6','H6',
                    'A7','B7','C7','D7','E7','F7','G7','H7','A8','B8','C8','D8','E8','F8','G8','H8'];
    return coords.map(coord => pos[coord] || '.');
  }
  // Default fallback
  const a = Array(64).fill('.'); a[27]='W'; a[28]='B'; a[35]='B'; a[36]='W'; 
  return a; 
}
function countBW(arr){ let b=0,w=0; for(const ch of arr){ if(ch==='B') b++; else if(ch==='W') w++; } return {b,w}; }
function msToClock(ms){ const s = Math.max(0, Math.floor(ms/1000)); const m = String(Math.floor(s/60)).padStart(2,'0'); const ss = String(s%60).padStart(2,'0'); return `${m}:${ss}`; }
function escapeHtml(str){ return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }
function setDelta(id, n){ const el = qs(id); if(!el) return; if(n===0){ el.textContent = '±0'; return; } el.textContent = `${n>0?'+':'−'}${Math.abs(n)}`; }

/* ========================================
   AI STATS - Compact Display Helpers
   ======================================== */
function fmtK(num){
  const n = Number(num);
  if(!isFinite(n)) return '—';
  const abs = Math.abs(n);
  if(abs >= 1e9) return (n/1e9).toFixed(1).replace(/\.0$/,'') + 'B';
  if(abs >= 1e6) return (n/1e6).toFixed(1).replace(/\.0$/,'') + 'M';
  if(abs >= 1e3) return (n/1e3).toFixed(1).replace(/\.0$/,'') + 'K';
  return String(Math.round(n));
}
function fmtPct(val){
  if(val === null || val === undefined) return '—';
  if(typeof val === 'string'){
    if(/%/.test(val)) return val; // already formatted
    const parsed = Number(val);
    if(isFinite(parsed)) val = parsed; else return '—';
  }
  // Treat 0-1 as ratio
  const p = (val <= 1 ? val*100 : val);
  return `${Math.round(p)}%`;
}
function fmtEval(val){
  const n = Number(val);
  if(!isFinite(n)) return '—';
  const s = n>0?'+':'';
  return s + n.toFixed(Math.abs(n) < 10 ? 1 : 0);
}
function fmtDepth(val){
  const n = parseInt(String(val).replace(/[^0-9]/g,''),10);
  if(!isFinite(n)) return '—';
  return 'D' + n;
}
function formatDurationMs(ms){
  const n = Number(ms);
  if(!isFinite(n) || n < 0) return '—';
  if(n < 1000) return `${Math.round(n)}ms`;
  const s = n / 1000;
  if(s < 60) return `${s.toFixed(s < 10 ? 1 : 0).replace(/\.0$/,'')}s`;
  const m = Math.floor(s / 60);
  const remS = Math.floor(s % 60);
  if(m < 60) return `${m}m ${String(remS).padStart(2,'0')}s`;
  const h = Math.floor(m / 60);
  const remM = m % 60;
  if(h < 24) return `${h}h ${String(remM).padStart(2,'0')}m`;
  const d = Math.floor(h / 24);
  const remH = h % 24;
  return `${d}d ${String(remH).padStart(2,'0')}h`;
}

function fmtMs(val){
  if(val === null || val === undefined) return '—';
  // Accept strings like "123ms" or "1.23s"
  if(typeof val === 'string'){
    const s = val.trim();
    if(/ms$/i.test(s)){
      const n = parseFloat(s.replace(/ms/i,''));
      return formatDurationMs(isFinite(n) ? n : NaN);
    }
    if(/s$/i.test(s)){
      const n = parseFloat(s.replace(/s/i,''));
      return formatDurationMs(isFinite(n) ? n*1000 : NaN);
    }
    const n = parseFloat(s);
    return formatDurationMs(isFinite(n) ? n : NaN);
  }
  // Numbers are treated as milliseconds
  return formatDurationMs(val);
}

// === AI VISUAL FEEDBACK ===
function updateAIAnalysis(aiData){
  try {
    if(!data) return;
    if(!aiData) {
      console.warn('updateAIAnalysis called with null/undefined aiData');
      return;
    }
    
    // Determine which AI just moved (from aiData.title or infer from last move)
    // NEVER use "Human" - filter it out
    let aiName = aiData.title || 'AI';
    if(aiName === 'Human' || aiName === 'Human Player'){
      // If aiData.title is Human, determine AI from players
      const blackName = data.players?.black?.name;
      const whiteName = data.players?.white?.name;
      const isBlackAI = blackName && blackName !== 'Human' && blackName !== 'Human Player';
      const isWhiteAI = whiteName && whiteName !== 'Human' && whiteName !== 'Human Player';
      
      if(isBlackAI) aiName = blackName;
      else if(isWhiteAI) aiName = whiteName;
      else aiName = 'AI';
    }
  
  // Create dynamic AI analysis notes with all available data
  const aiAnalysis = {
    // Always update title to show AI name
    title: aiName,
    
    // Basic analysis data - use available data or defaults
    selected_move: aiData.move || aiData.selected_move || aiData.best_move || 'N/A',
    evaluation: aiData.evaluation !== undefined ? String(aiData.evaluation) : '0',
    depth: aiData.depth !== undefined ? `${aiData.depth} plies` : 
           aiData.depth_reached !== undefined ? `${aiData.depth_reached} plies` : '0 plies',
    
    // Search statistics from engine
    nodes_searched: (aiData.nodes_searched ?? aiData.nodes ?? 0).toLocaleString(),
    nodes_pruned: (aiData.nodes_pruned ?? aiData.pruning ?? 0).toLocaleString(),
    pruning_ratio: aiData.pruning_ratio !== undefined ? `${(aiData.pruning_ratio * 100).toFixed(1)}%` : 
                   aiData.pruning_efficiency !== undefined ? `${aiData.pruning_efficiency.toFixed(1)}%` : '0%',
    avg_search_time: aiData.avg_search_time || aiData.total_time_ms ? `${aiData.total_time_ms}ms` : '0ms',
    total_searches: aiData.total_searches ?? 0,
    nodes_per_second: aiData.nodes_per_second ?? 0, // Add N/s
    
    // Advanced statistics - use 0 instead of N/A for consistency
    transposition_hits: (aiData.transposition_hits ?? aiData.tt_hits ?? 0).toLocaleString(),
    transposition_size: (aiData.transposition_size ?? aiData.tt_size ?? 0).toLocaleString(),
    killer_moves: (aiData.killer_moves ?? aiData.pv_move_hits ?? 0).toLocaleString(),
    history_entries: (aiData.history_entries ?? 0).toLocaleString(),
    
    // Pruning statistics - use 0 instead of N/A
    null_move_cutoffs: (aiData.null_move_cutoffs ?? aiData.null_move_cuts ?? 0).toLocaleString(),
    null_move_searches: (aiData.null_move_searches ?? 0).toLocaleString(),
    futility_pruned: (aiData.futility_pruned ?? aiData.futility_cuts ?? 0).toLocaleString(),
    lmr_reductions: (aiData.lmr_reductions ?? 0).toLocaleString(),
    lmr_researches: (aiData.lmr_researches ?? 0).toLocaleString(),
    multi_cut_pruned: (aiData.multi_cut_pruned ?? aiData.multi_cut_prunes ?? 0).toLocaleString()
  };
  
  // NOTE: Old notes panel removed - now using updateAIQuickStats() instead
  // This function still exists for backward compatibility with data storage
  
  // Store for reference
  data.notes = aiAnalysis;
  } catch (error) {
    console.error('❌ Error in updateAIAnalysis:', error);
    console.error('Stack trace:', error.stack);
    console.error('aiData was:', aiData);
  }
}



function addThinkingIconToPlayerName(side = 'W'){
  // Add rotating icon to player name based on side
  const playerName = (side === 'B') ? qs('p1Name') : qs('p2Name');
  if(playerName && !playerName.querySelector('.thinking-icon')){
    const icon = document.createElement('span');
    icon.className = 'thinking-icon';
    icon.innerHTML = '↻';
    icon.style.cssText = 'display:inline-block;margin-right:8px;animation:spin 1s linear infinite;color:var(--accent2);font-size:1.2em;vertical-align:middle;';
    playerName.insertBefore(icon, playerName.firstChild);
  }
}

function removeThinkingIconFromPlayerName(side = 'W'){
  // Remove rotating icon from player name based on side
  const playerName = (side === 'B') ? qs('p1Name') : qs('p2Name');
  if(playerName){
    const icon = playerName.querySelector('.thinking-icon');
    if(icon){
      icon.remove();
    }
  }
}

/* ========================================
   AI QUICK STATS - Sidebar Panel
   ======================================== */
// Reset cumulative stats for new move
/**
 * Schedule AI stats update with throttling (max 1 update per second)
 * Works for both sequential and parallel search modes
 */
function scheduleStatsUpdate(stats, isFinal = false){
  if(!stats) return;
  
  // Store latest stats
  pendingQuickStats = stats;
  
  // If final, update immediately
  if(isFinal){
    if(statsUpdateTimer) clearTimeout(statsUpdateTimer);
    updateAIQuickStats(stats, true);
    return;
  }
  
  // Check throttling
  const now = Date.now();
  const timeSinceLastUpdate = now - lastQuickStatsUpdate;
  
  if(timeSinceLastUpdate >= QUICK_STATS_THROTTLE_MS){
    // Enough time passed, update now
    updateAIQuickStats(stats, false);
  } else if(!statsUpdateTimer){
    // Schedule update for later
    const delay = QUICK_STATS_THROTTLE_MS - timeSinceLastUpdate;
    statsUpdateTimer = setTimeout(() => {
      statsUpdateTimer = null;
      if(pendingQuickStats){
        updateAIQuickStats(pendingQuickStats, false);
      }
    }, delay);
  }
}

/**
 * Update AI Quick Stats panel with latest statistics
 * Unified handler for both sequential and parallel modes
 */
function updateAIQuickStats(stats, isFinal = false){
  if(!stats) return;
  
  const quickStatsPanel = document.getElementById('aiQuickStats');
  const emptyState = document.getElementById('aiQuickStatsEmpty');
  const progressPanel = document.getElementById('aiQuickStatsProgress');
  
  if(!quickStatsPanel || !emptyState) return;
  
  // Extract values (support multiple key names for compatibility)
  const nodes = stats.nodes_searched || stats.nodes || 0;
  const pruned = stats.nodes_pruned || stats.pruning || 0;
  const depth = stats.depth_reached || (typeof stats.depth === 'number' ? stats.depth : 0);
  const timeMs = stats.search_time_ms || stats.time_ms || stats.total_time_ms || 0;
  const nps = stats.nodes_per_second || (timeMs > 0 ? Math.floor((nodes * 1000) / timeMs) : 0);
  
  // Skip ONLY if absolutely no data (initial message)
  if(nodes === 0 && depth === 0 && !isFinal) return;
  
  // Update timestamp
  lastQuickStatsUpdate = Date.now();
  pendingQuickStats = null;
  
  // Show stats panel, hide others
  quickStatsPanel.style.display = 'flex';
  emptyState.style.display = 'none';
  if(progressPanel) progressPanel.style.display = 'none';
  statsCurrentlyVisible = true; // Mark as visible
  
  // Calculate pruning percentage
  const totalNodes = nodes + pruned;
  const prunePercent = totalNodes > 0 ? ((pruned / totalNodes) * 100) : 0;
  
  // Format helper functions
  const formatNumber = (n) => {
    if(n >= 1e9) return `${(n/1e9).toFixed(2)}G`;
    if(n >= 1e6) return `${(n/1e6).toFixed(1)}M`;
    if(n >= 1e3) return `${(n/1e3).toFixed(1)}K`;
    return n.toString();
  };
  
  const formatNPS = (n) => {
    if(n >= 1e9) return `${(n/1e9).toFixed(2)}G/s`;
    if(n >= 1e6) return `${(n/1e6).toFixed(1)}M/s`;
    if(n >= 1e3) return `${(n/1e3).toFixed(1)}K/s`;
    return `${n}/s`;
  };
  
  const formatTime = (ms) => {
    if(ms < 1000) return `${Math.round(ms)}ms`;
    const s = ms / 1000;
    if(s < 60) return `${s.toFixed(1)}s`;
    const m = Math.floor(s / 60);
    const remS = Math.round(s % 60);
    if(m < 60) return `${m}m ${remS}s`;
    const h = Math.floor(m / 60);
    const remM = m % 60;
    return `${h}h ${remM}m`;
  };
  
  // Update UI elements
  const depthElem = document.getElementById('aiQuickDepth');
  const nodesElem = document.getElementById('aiQuickNodes');
  const npsElem = document.getElementById('aiQuickNPS');
  const pruneElem = document.getElementById('aiQuickPrune');
  const timeElem = document.getElementById('aiQuickTime');
  
  if(depthElem) depthElem.textContent = depth || '--';
  if(nodesElem) nodesElem.textContent = formatNumber(nodes);
  if(npsElem) npsElem.textContent = formatNPS(nps);
  if(pruneElem) pruneElem.textContent = `${prunePercent.toFixed(1)}%`;
  if(timeElem) timeElem.textContent = formatTime(timeMs);
}

// Show "Searching..." state when AI starts thinking
function showAISearchingState(){
  const quickStatsPanel = document.getElementById('aiQuickStats');
  const emptyState = document.getElementById('aiQuickStatsEmpty');
  const progressPanel = document.getElementById('aiQuickStatsProgress');
  
  if(!quickStatsPanel || !emptyState) return;
  
  // Show empty state while waiting for stats
  quickStatsPanel.style.display = 'none';
  emptyState.style.display = 'block';
  if(progressPanel) progressPanel.style.display = 'none';
  statsCurrentlyVisible = false; // Mark as not visible
  
  // Reset to placeholders
  const elements = ['aiQuickDepth', 'aiQuickNodes', 'aiQuickNPS', 'aiQuickPrune', 'aiQuickTime'];
  elements.forEach(id => {
    const elem = document.getElementById(id);
    if(elem) elem.textContent = '--';
  });
}

// Show AI stats panel (called when AI player is detected)
function showAIQuickStatsPanel(){
  const emptyState = document.getElementById('aiQuickStatsEmpty');
  if(emptyState) emptyState.style.display = 'block';
}

// Hide AI stats (called when no AI player)
function hideAIQuickStats(){
  const quickStatsPanel = document.getElementById('aiQuickStats');
  const emptyState = document.getElementById('aiQuickStatsEmpty');
  if(quickStatsPanel) quickStatsPanel.style.display = 'none';
  if(emptyState) emptyState.style.display = 'block';
}

function updatePlayerIcons(){
  // Update change-player icons based on current player types
  const blackName = data?.players?.black?.name;
  const whiteName = data?.players?.white?.name;
  const isBlackAI = blackName && blackName !== 'Human';
  const isWhiteAI = whiteName && whiteName !== 'Human';
  
  const blackIcon = document.getElementById('changeBlackIcon');
  const whiteIcon = document.getElementById('changeWhiteIcon');
  
  // AI icon (computer/monitor)
  const aiIconPaths = `
    <rect x="2" y="3" width="20" height="14" rx="2"/>
    <path d="M8 21h8"/>
    <path d="M12 17v4"/>
  `;
  
  // Human icon (person)
  const humanIconPaths = `
    <path d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4"/>
    <path d="M3 21a9 9 0 0 1 18 0"/>
  `;
  
  if(blackIcon){
    blackIcon.innerHTML = isBlackAI ? aiIconPaths : humanIconPaths;
  }
  if(whiteIcon){
    whiteIcon.innerHTML = isWhiteAI ? aiIconPaths : humanIconPaths;
  }
}

// === NOTES RENDERING ===
function renderNotes(notes){
  const box = qs('deepeningSummary'); 
  if(!box){ return; }
  
  const nd = { ...notes };
  delete nd.title;
  
  // Extract key fields with fallbacks
  const evalVal  = nd.selected_value ?? nd.evaluation;
  const depthVal = nd.final_depth ?? nd.depth;
  const nodes    = nd.nodes_searched;
  const pruned   = nd.nodes_pruned;
  const pruneR   = nd.pruning_ratio;
  const avgMs    = nd.avg_search_time;
  function parseMsInt(v){
    if(v === null || v === undefined) return null;
    if(typeof v === 'number' && isFinite(v)) return Math.round(v);
    const s = String(v).trim();
    // Accept "123.4ms" or "0.123s" or plain number string
    if(/ms$/i.test(s)){
      const n = parseFloat(s.replace(/ms/i,''));
      return isFinite(n) ? Math.round(n) : null;
    }
    if(/s$/i.test(s)){
      const n = parseFloat(s.replace(/s/i,''));
      return isFinite(n) ? Math.round(n*1000) : null;
    }
    const n = parseFloat(s);
    return isFinite(n) ? Math.round(n) : null;
  }
  const lastMsNum = parseMsInt(nd.last_search_time_ms);
  const searches = nd.total_searches;

  // Compute Nodes/s (approximate) from nodes and avg_search_time
  function parseSeconds(s){
    if(!s) return null;
    if(typeof s === 'number') return s; // already seconds
    const str = String(s).trim();
    if(/ms$/i.test(str)){
      const n = parseFloat(str.replace(/ms/i,''));
      return isFinite(n) ? n/1000 : null;
    }
    if(/s$/i.test(str)){
      const n = parseFloat(str.replace(/s/i,''));
      return isFinite(n) ? n : null;
    }
    const n = parseFloat(str);
    return isFinite(n) ? n : null;
  }
  // Compute Nodes/s - use provided value if available, otherwise calculate
  let nps = nd.nodes_per_second; // Use from backend if available
  console.log('[renderNotes] nodes_per_second from data:', nd.nodes_per_second, 'nodes:', nodes, 'lastMsNum:', lastMsNum);
  if(!nps || nps === 0){
    const secs = (lastMsNum !== null && lastMsNum > 0)
      ? (lastMsNum / 1000)
      : parseSeconds(avgMs);
    if(typeof nodes === 'number' && nodes > 0 && secs && secs > 0){
      nps = nodes / secs;
      console.log('[renderNotes] Calculated nps:', nps, 'from nodes:', nodes, 'secs:', secs);
    } else {
      nps = 0;
      console.log('[renderNotes] Cannot calculate nps - missing data');
    }
  } else {
    console.log('[renderNotes] Using provided nps:', nps);
  }

  // Decide which tiles to show (compact): hide Eval/Depth if not available
  const showEval = Number.isFinite(Number(evalVal));
  const depthNum = parseInt(String(depthVal).replace(/[^0-9]/g,''),10);
  const showDepth = Number.isFinite(depthNum) && depthNum > 0;

  let tiles = '';
  if(showEval){ tiles += `<div class="statBadge"><span class="statLabel">Eval</span><span class="statValue">${fmtEval(evalVal)}</span></div>`; }
  if(showDepth){ tiles += `<div class="statBadge"><span class="statLabel">Depth</span><span class="statValue">${fmtDepth(depthVal)}</span></div>`; }
  tiles += `<div class="statBadge"><span class="statLabel">Nodes</span><span class="statValue">${fmtK(nodes)}</span></div>`;
  tiles += `<div class="statBadge"><span class="statLabel">N/s</span><span class="statValue">${typeof nps==='number' && nps > 0 ? fmtK(nps) : '0'}</span></div>`;
  tiles += `<div class=\"statBadge\"><span class=\"statLabel\">Prune</span><span class=\"statValue\">${fmtPct(pruneR)}</span></div>`;
  tiles += `<div class=\"statBadge\"><span class=\"statLabel\">Last</span><span class=\"statValue\">${lastMsNum !== null ? formatDurationMs(lastMsNum) : fmtMs(avgMs)}</span></div>`;
  tiles += `<div class="statBadge"><span class="statLabel">Searches</span><span class="statValue">${fmtK(searches)}</span></div>`;

  box.innerHTML = `<div class="statGrid">${tiles}</div>`;
}

// === OPENING TREE RENDERING ===
  function renderOpeningTree(tree){
  const box = document.getElementById('openingTree');
  if(!box) return;
  const hasChildren = !!(tree && Array.isArray(tree.children) && tree.children.length>0);
  const hasNames = !!(tree && Array.isArray(tree.names_at_position) && tree.names_at_position.length>0);
  const hasCurrent = !!(tree && tree.current_opening);
  if(!hasChildren && !hasNames && !hasCurrent){
    box.innerHTML = '<div class="opening-tree-empty">Nessuna linea di libro dalla posizione corrente</div>';
    return;
  }

  // Clear
  box.innerHTML = '';

  // Build set of valid moves for current position to avoid highlighting invalid variants
  const validSet = new Set(((data && data.valid_by_ply && data.valid_by_ply[0]) || []).map(String));

  // Current opening header
  if(tree.current_opening){
    const currentHeader = document.createElement('div');
    currentHeader.className = 'opening-tree-current';
    
    const icon = document.createElement('div');
    icon.className = 'opening-tree-current-icon';
    icon.textContent = '📖';
    
    const text = document.createElement('div');
    text.className = 'opening-tree-current-text';
    text.textContent = tree.current_opening;
    
    currentHeader.appendChild(icon);
    currentHeader.appendChild(text);
    box.appendChild(currentHeader);
  }

  // Helper functions
  function advClass(adv){
    if(adv === undefined || adv === null) return 'opening-tree-adv opening-tree-adv-unk';
    if(adv === '=') return 'opening-tree-adv opening-tree-adv-eq';
    const a = String(adv).toLowerCase();
    if(a==='w') return 'opening-tree-adv opening-tree-adv-w';
    if(a==='w+') return 'opening-tree-adv opening-tree-adv-wp';
    if(a==='w++') return 'opening-tree-adv opening-tree-adv-wpp';
    if(a==='b') return 'opening-tree-adv opening-tree-adv-b';
    if(a==='b+') return 'opening-tree-adv opening-tree-adv-bp';
    if(a==='b++') return 'opening-tree-adv opening-tree-adv-bpp';
    return 'opening-tree-adv opening-tree-adv-eq';
  }

  function advLabel(adv){
    if(adv === undefined || adv === null) return '?';
    if(adv === '=') return '=';
    const a = String(adv).toLowerCase();
    if(a==='w') return 'W';
    if(a==='w+') return 'W+';
    if(a==='w++') return 'W++';
    if(a==='b') return 'B';
    if(a==='b+') return 'B+';
    if(a==='b++') return 'B++';
    return '=';
  }

  function highlightCell(move){
    try{
      const i = coordToIdx(move);
      const cell = document.getElementById('board')?.children[i]?.firstElementChild;
      if(!cell) return;
      const hint = document.createElement('div');
      hint.className = 'hint';
      hint.textContent = '•';
      hint.dataset.__ot = '1';
      cell.appendChild(hint);
    }catch(_){/* noop */}
  }

  function clearHighlights(){
    document.querySelectorAll('.hint[data-__ot="1"]').forEach(e=>e.remove());
  }

  function createTreeNode(n, depth=0){
    // Node container
    const node = document.createElement('div');
    node.className = 'opening-tree-node';
    node.dataset.depth = depth;

    // Node content
    const content = document.createElement('div');
    content.className = 'opening-tree-node-content';

    // Move badge
    const moveEl = document.createElement('div');
    moveEl.className = 'opening-tree-move';
    moveEl.textContent = (n.move || '').toUpperCase();
    content.appendChild(moveEl);

    // Advantage indicator (only show if not null/undefined/?)
    const advLabelText = advLabel(n.advantage);
    if(advLabelText && advLabelText !== '?'){
      const advEl = document.createElement('div');
      advEl.className = advClass(n.advantage);
      advEl.textContent = advLabelText;
      content.appendChild(advEl);
    }

    // Opening names
    const namesFull = Array.isArray(n.names) && n.names.length
      ? n.names
      : (Array.isArray(n.openings) ? n.openings.map(o=>o && o.name ? String(o.name) : '').filter(Boolean) : []);
    
    if(namesFull.length > 0){
      const namesEl = document.createElement('div');
      namesEl.className = 'opening-tree-names';
      const namesShort = namesFull.slice(0, 3).join(' • ');
      namesEl.textContent = namesShort;
      namesEl.title = namesFull.join('\n');
      content.appendChild(namesEl);
    } else {
      // Spacer when no names
      const spacer = document.createElement('div');
      spacer.style.flex = '1';
      content.appendChild(spacer);
    }

    // Interaction handlers
    content.onmouseenter = ()=>{ 
      clearHighlights(); 
      if(validSet.has(String(n.move).toUpperCase())){ highlightCell(n.move); }
    };
    content.onmouseleave = ()=>{ clearHighlights(); };
    content.onclick = ()=>{
      try{
        const i = coordToIdx(n.move); 
        const cell = document.getElementById('board')?.children[i];
        cell?.scrollIntoView({block:'nearest', inline:'nearest'});
      }catch(_){/* noop */}
    };

    node.appendChild(content);

    // Render children if available (for hierarchical tree)
    if(Array.isArray(n.children) && n.children.length > 0 && depth < 2){
      const childrenContainer = document.createElement('div');
      childrenContainer.className = 'opening-tree-children';
      n.children.forEach(child => {
        const childNode = createTreeNode(child, depth + 1);
        childrenContainer.appendChild(childNode);
      });
      node.appendChild(childrenContainer);
    }

    return node;
  }

  // If we have children, render them as a tree
  if(hasChildren){
    const treeList = document.createElement('div');
    treeList.className = 'opening-tree-list';
    box.appendChild(treeList);

    // Filter only valid moves
    const filteredChildren = (tree.children || []).filter(n => validSet.has(String(n.move).toUpperCase()));
    
    // Limit to top 8 moves for better readability
    const topMoves = filteredChildren.slice(0, 8);
    
    topMoves.forEach(child => {
      const node = createTreeNode(child, 0);
      treeList.appendChild(node);
    });

    // Show count if there are more moves
    if(filteredChildren.length > 8){
      const moreInfo = document.createElement('div');
      moreInfo.className = 'opening-tree-empty';
      moreInfo.textContent = `+${filteredChildren.length - 8} more variations`;
      moreInfo.style.opacity = '0.5';
      moreInfo.style.fontSize = '11px';
      moreInfo.style.padding = '4px 8px';
      moreInfo.style.marginTop = '4px';
      box.appendChild(moreInfo);
    }
  } else {
    // No children: show variant names only
    if(hasNames){
      const namesContainer = document.createElement('div');
      namesContainer.style.cssText = 'padding:8px 10px;font-size:11px;color:rgba(255,255,255,.6);line-height:1.6';
      const names = Array.from(new Set(tree.names_at_position)).slice(0, 12);
      namesContainer.textContent = names.join(' • ');
      box.appendChild(namesContainer);
    }
  }
}

// ============================================================================
// AI CONFIGURATION VIEWER
// ============================================================================

let aiConfigEditor = null;
let currentAIPlayerName = null;

async function openAIConfig(playerName) {
  try {
    console.log(`Loading configuration for ${playerName}...`);
    
    // Fetch player configuration from server
    const response = await fetch(`http://localhost:8000/api/player-config/${encodeURIComponent(playerName)}`);
    const data = await response.json();
    
    if (data.error) {
      alert(`Error loading configuration: ${data.error}`);
      return;
    }
    
    // Update modal content
    document.getElementById('configPlayerName').textContent = `${data.player_name} Configuration`;
    document.getElementById('configFilePath').textContent = data.config_path;
    
    // Initialize CodeMirror if not already done
    if (!aiConfigEditor) {
      const textarea = document.getElementById('aiConfigEditor');
      aiConfigEditor = CodeMirror.fromTextArea(textarea, {
        mode: 'yaml',
        theme: 'monokai',
        lineNumbers: true,
        readOnly: true,
        lineWrapping: false,
        matchBrackets: true,
        viewportMargin: Infinity
      });
      aiConfigEditor.setSize('100%', '100%');
    }
    
    // Set YAML content
    aiConfigEditor.setValue(data.yaml_content);
    aiConfigEditor.refresh();
    
    // Show modal
    document.getElementById('aiConfigModal').style.display = 'flex';
    
    // Refresh editor after modal is visible
    setTimeout(() => aiConfigEditor.refresh(), 100);
    
  } catch (error) {
    console.error('Error loading AI configuration:', error);
    alert(`Failed to load configuration: ${error.message}`);
  }
}

function closeAIConfigModal() {
  document.getElementById('aiConfigModal').style.display = 'none';
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && document.getElementById('aiConfigModal').style.display === 'flex') {
    closeAIConfigModal();
  }
});

// Setup button click handler
document.addEventListener('DOMContentLoaded', () => {
  const viewConfigBtn = document.getElementById('viewWhiteConfigBtn');
  if (viewConfigBtn) {
    viewConfigBtn.addEventListener('click', () => {
      if (currentAIPlayerName) {
        openAIConfig(currentAIPlayerName);
      }
    });
  }
});
