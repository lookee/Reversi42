#!/usr/bin/env python3
"""
Backend Monitor - Watches the backend server and restarts it if it crashes
"""

import subprocess
import time
import signal
import sys
import os
import logging
from datetime import datetime
import urllib.request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/backend_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BackendMonitor:
    def __init__(self, port=8000, player="DIVZERO.EXE"):
        self.port = port
        self.player = player
        self.process = None
        self.restart_count = 0
        self.max_restarts = 10
        self.restart_delay = 5  # seconds
        self.last_restart = None
        
    def start_backend(self):
        """Start the backend server"""
        try:
            logger.info(f"Starting backend server on port {self.port} with player {self.player}")
            
            # Set environment
            env = os.environ.copy()
            env['PYTHONPATH'] = "/Users/lucaamore/Documents/devel/Reversi42:" + env.get('PYTHONPATH', '')
            
            # Start process
            self.process = subprocess.Popen([
                '/Library/Developer/CommandLineTools/usr/bin/python3',
                '-m', 'src.webgui.backend_server',
                '--port', str(self.port),
                '--player', self.player
            ], 
            stdout=open('/tmp/backend.log', 'w'),
            stderr=subprocess.STDOUT,
            env=env,
            cwd='/Users/lucaamore/Documents/devel/Reversi42'
            )
            
            logger.info(f"Backend started with PID {self.process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start backend: {e}")
            return False
    
    def stop_backend(self):
        """Stop the backend server"""
        if self.process:
            try:
                logger.info(f"Stopping backend server (PID {self.process.pid})")
                self.process.terminate()
                self.process.wait(timeout=10)
                logger.info("Backend stopped gracefully")
            except subprocess.TimeoutExpired:
                logger.warning("Backend didn't stop gracefully, killing...")
                self.process.kill()
                self.process.wait()
            except Exception as e:
                logger.error(f"Error stopping backend: {e}")
            finally:
                self.process = None
    
    def is_backend_running(self):
        """Check if backend is running"""
        if not self.process:
            return False
        
        # Check if process is still running
        poll = self.process.poll()
        if poll is not None:
            logger.warning(f"Backend process ended with code {poll}")
            return False
        
        # Try to connect to the server using stdlib (avoid external deps)
        try:
            with urllib.request.urlopen(f"http://localhost:{self.port}", timeout=5) as response:
                # Consider any 2xx as healthy
                return 200 <= response.status < 300
        except Exception:
            return False
    
    def restart_backend(self):
        """Restart the backend server"""
        now = datetime.now()
        
        # Check restart limits
        if self.restart_count >= self.max_restarts:
            logger.error(f"Maximum restart limit ({self.max_restarts}) reached. Stopping monitor.")
            return False
        
        # Check restart frequency
        if self.last_restart:
            time_since_last = (now - self.last_restart).total_seconds()
            if time_since_last < self.restart_delay:
                logger.warning(f"Restart too soon ({time_since_last:.1f}s), waiting...")
                time.sleep(self.restart_delay - time_since_last)
        
        logger.info(f"Restarting backend (attempt {self.restart_count + 1}/{self.max_restarts})")
        
        # Stop current process
        self.stop_backend()
        
        # Wait a bit
        time.sleep(2)
        
        # Start new process
        if self.start_backend():
            self.restart_count += 1
            self.last_restart = now
            logger.info(f"Backend restarted successfully (restart #{self.restart_count})")
            return True
        else:
            logger.error("Failed to restart backend")
            return False
    
    def monitor_loop(self):
        """Main monitoring loop"""
        logger.info("Starting backend monitor...")
        
        # Start initial backend
        if not self.start_backend():
            logger.error("Failed to start initial backend")
            return
        
        try:
            while True:
                time.sleep(10)  # Check every 10 seconds
                
                if not self.is_backend_running():
                    logger.warning("Backend is not running, attempting restart...")
                    if not self.restart_backend():
                        logger.error("Failed to restart backend, exiting monitor")
                        break
                        
        except KeyboardInterrupt:
            logger.info("Monitor interrupted by user")
        except Exception as e:
            logger.error(f"Monitor error: {e}")
        finally:
            self.stop_backend()
            logger.info("Monitor stopped")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down monitor...")
    sys.exit(0)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backend Monitor')
    parser.add_argument('--port', type=int, default=8000, help='Port to monitor')
    parser.add_argument('--player', default='DIVZERO.EXE', help='AI player to use')
    parser.add_argument('--max-restarts', type=int, default=10, help='Maximum restart attempts')
    
    args = parser.parse_args()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run monitor
    monitor = BackendMonitor(port=args.port, player=args.player)
    monitor.max_restarts = args.max_restarts
    monitor.monitor_loop()

if __name__ == "__main__":
    main()
