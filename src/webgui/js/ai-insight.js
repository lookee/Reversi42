/**
 * Reversi42 - AI Insight Panel
 * 
 * Real-time AI reasoning visualization
 * Shows live search logs, move evaluations, and thinking process
 * 
 * Features:
 *  - Live AI reasoning logs
 *  - Search progress tracking
 *  - Move evaluation details
 *  - Auto-scroll to latest logs
 * 
 * @version 3.2.0
 */

// AI Insight Panel Management
const toggleAiInsightBtn = document.getElementById('toggleAiInsight');
const aiInsightWrapper = document.getElementById('aiInsightWrapper');
const closeAiInsightBtn = document.getElementById('closeAiInsight');
const clearAiLogsBtn = document.getElementById('clearAiLogs');
const aiLogsContent = document.getElementById('aiLogsContent');

// Toggle AI Insight panel
if(toggleAiInsightBtn){
  toggleAiInsightBtn.addEventListener('click', () => {
    const isVisible = aiInsightWrapper.style.display !== 'none';
    aiInsightWrapper.style.display = isVisible ? 'none' : 'flex';
  });
}

// Close AI Insight panel
if(closeAiInsightBtn){
  closeAiInsightBtn.addEventListener('click', () => {
    aiInsightWrapper.style.display = 'none';
  });
}

// Clear AI logs
if(clearAiLogsBtn){
  clearAiLogsBtn.addEventListener('click', () => {
    if(aiLogsContent){
      aiLogsContent.innerHTML = '<div style="color:#63b3ed;padding:20px;text-align:center;opacity:0.6">AI reasoning logs will appear here during search...</div>';
    }
  });
}

// Append AI log entry
function appendAILog(logData){
  if(!aiLogsContent) return;
  
  // Remove placeholder if it exists
  if(aiLogsContent.children.length === 1 && aiLogsContent.children[0].textContent.includes('will appear here')){
    aiLogsContent.innerHTML = '';
  }
  
  const { timestamp, log_type, message, details } = logData;
  
  // Create log entry
  const logEntry = document.createElement('div');
  logEntry.className = `ai-log-entry ai-log-${log_type}`;
  
  // Format timestamp
  const timestampSpan = document.createElement('span');
  timestampSpan.className = 'ai-log-timestamp';
  timestampSpan.textContent = `[${timestamp}]`;
  
  // Format message
  const messageSpan = document.createElement('span');
  messageSpan.className = 'ai-log-message';
  messageSpan.textContent = ` ${message}`;
  
  logEntry.appendChild(timestampSpan);
  logEntry.appendChild(messageSpan);
  
  // Add to container
  aiLogsContent.appendChild(logEntry);
  
  // Auto-scroll to bottom
  const container = aiLogsContent.parentElement;
  if(container){
    container.scrollTop = container.scrollHeight;
  }
}

// Make appendAILog available globally
window.appendAILog = appendAILog;
