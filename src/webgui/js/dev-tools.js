/**
 * Reversi42 - Developer Tools
 * 
 * Developer insight panel with live backend logs and WebSocket traffic viewer
 * Provides real-time monitoring of server communication and debugging tools
 * 
 * Features:
 *  - Live server logs (tail -f style)
 *  - WebSocket traffic viewer with syntax highlighting
 *  - Auto-refresh functionality
 *  - Tab-based interface
 * 
 * @version 3.2.0
 */

// Initialize Developer Tools after template is loaded
function initDevTools() {
  function q(id){ return document.getElementById(id); }
  const toggleBtn = q('toggleJsonEditor');
  const editorWrapper = q('jsonEditorWrapper');
  const closeBtn2 = q('closeJsonEditor2');
if(toggleBtn) toggleBtn.addEventListener('click', () => {
  const isVisible = editorWrapper.style.display !== 'none';
  editorWrapper.style.display = isVisible ? 'none' : 'flex';
  if(!isVisible){
    loadLogs();
    if(logsAutoRefreshInterval) clearInterval(logsAutoRefreshInterval);
    logsAutoRefreshInterval = setInterval(loadLogs, 2000);
  } else {
    if(logsAutoRefreshInterval) { clearInterval(logsAutoRefreshInterval); logsAutoRefreshInterval = null; }
  }
});
if(closeBtn2) closeBtn2.addEventListener('click', () => { editorWrapper.style.display = 'none'; if(logsAutoRefreshInterval){ clearInterval(logsAutoRefreshInterval); logsAutoRefreshInterval = null; } });

// Logs functionality
const refreshLogsBtn = q('refreshLogs');
const clearLogsBtn = q('clearLogs');
const clearWsBtn = q('clearWs');
const tabBtnLogs = q('tabBtnLogs');
const tabBtnWs = q('tabBtnWs');
const tabLogsPane = q('tabLogsPane');
const tabWsPane = q('tabWsPane');
const logsContent = q('logsContent');

function colorizeLog(line) {
  let colorClass = 'log-info';
  if(line.includes('ERROR')) colorClass = 'log-error';
  else if(line.includes('WARNING')) colorClass = 'log-warning';
  else if(line.includes('INFO')) colorClass = 'log-info';
  else if(line.includes('DEBUG')) colorClass = 'log-debug';
  
  // Escape HTML and preserve the full line
  const escapedLine = line
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  
  return `<div class="log-line ${colorClass}">${escapedLine}</div>`;
}

function loadLogs() {
  // Fetch logs from backend API endpoint
  fetch('http://localhost:8000/logs')
    .then(response => response.text())
    .then(text => {
      const lines = text.split('\n').filter(l => l.trim());
      logsContent.innerHTML = lines.map(line => colorizeLog(line)).join('');
      
      // Auto-scroll to bottom (tail -f behavior)
      const logsContainer = logsContent.parentElement;
      logsContainer.scrollTop = logsContainer.scrollHeight;
    })
    .catch(err => {
      logsContent.innerHTML = `<div class="log-error">Error loading logs: ${err.message}</div>`;
    });
}

// Auto-refresh logs every 2 seconds (tail -f behavior)
let logsAutoRefreshInterval = null;

if(refreshLogsBtn) refreshLogsBtn.addEventListener('click', loadLogs);
if(clearLogsBtn) clearLogsBtn.addEventListener('click', () => {
  logsContent.innerHTML = '';
});
if(clearWsBtn) clearWsBtn.addEventListener('click', () => {
  const w = q('wsTrafficContent'); if(w) w.innerHTML = '';
});

// Tab switching between Logs and WebSocket
function activateTab(which){
  if(which==='logs'){
    tabBtnLogs?.classList.add('active'); tabBtnWs?.classList.remove('active');
    tabLogsPane?.classList.add('active'); tabWsPane?.classList.remove('active');
    if(logsAutoRefreshInterval) clearInterval(logsAutoRefreshInterval);
    logsAutoRefreshInterval = setInterval(loadLogs, 2000);
  } else {
    tabBtnWs?.classList.add('active'); tabBtnLogs?.classList.remove('active');
    tabWsPane?.classList.add('active'); tabLogsPane?.classList.remove('active');
    if(logsAutoRefreshInterval){ clearInterval(logsAutoRefreshInterval); logsAutoRefreshInterval = null; }
  }
}
tabBtnLogs?.addEventListener('click', ()=>activateTab('logs'));
tabBtnWs?.addEventListener('click', ()=>activateTab('ws'));
}

// Will be called by loadTemplates() in game.js after templates are loaded

