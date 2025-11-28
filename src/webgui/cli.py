#!/usr/bin/env python3
"""
Reversi42 CLI - Command Line Interface
Main entry point for the Reversi42 web application.

Usage:
    reversi42                           # Start with defaults (port 8000, auto-open browser)
    reversi42 --port 3000              # Custom port
    reversi42 --no-browser             # Don't open browser
    reversi42-server                   # Server only mode (no browser)

    reversi42 --player "APOCALYPTRON"  # Set AI opponent
    reversi42 --host 0.0.0.0           # Bind to all interfaces
    reversi42 --help                   # Show help
"""

import argparse
import asyncio
import os
import signal
import sys
import time
import webbrowser
from pathlib import Path
from typing import Optional

# Version info
try:
    from __version__ import __version__
except ImportError:
    __version__ = "6.2.1"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="reversi42",
        description="🎮 Reversi42 - AI-Powered Reversi/Othello Web Game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  reversi42                           Start game with defaults
  reversi42 --port 3000              Start on custom port
  reversi42 --player "ZEN MASTER"   Choose AI opponent
  reversi42 --no-browser             Server only (no auto-open)
  reversi42 --list-players           List all AI players
  reversi42-server                   Alias for --no-browser

Configuration:
  Player configs: config/players/enabled/gladiators/*.yaml
  Game settings:  config/game.yaml
  
Homepage: https://github.com/lookee/Reversi42
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        metavar="PORT",
        help="Port to run the server on (default: 8000)",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        metavar="HOST",
        help="Host to bind to (default: 127.0.0.1, use 0.0.0.0 for all interfaces)",
    )

    parser.add_argument(
        "--player",
        type=str,
        default="DIVZERO.EXE",
        metavar="NAME",
        help="AI opponent name (default: DIVZERO.EXE)",
    )

    parser.add_argument(
        "--no-browser", action="store_true", help="Don't automatically open browser"
    )

    parser.add_argument(
        "--list-players", action="store_true", help="List all available AI players and exit"
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development (requires uvicorn[standard])",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
        help="Logging level (default: info)",
    )

    return parser.parse_args()


def list_available_players() -> int:
    """List all available AI players."""
    print("\n" + "=" * 80)
    print("🎮 Available AI Players")
    print("=" * 80 + "\n")

    try:
        # Add src to path
        src_dir = Path(__file__).parent.parent
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))

        from Players.config import PlayerRegistry

        registry = PlayerRegistry()
        registry.print_summary()
        return 0

    except Exception as e:
        print(f"❌ Failed to load players: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


def open_browser_delayed(url: str, delay: float = 1.5):
    """Open browser after a delay to ensure server is ready."""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"✅ Browser opened: {url}")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print(f"   Please open manually: {url}")


def serve(
    host: str = "127.0.0.1",
    port: int = 8000,
    player: str = "DIVZERO.EXE",
    open_browser: bool = False,
    reload: bool = False,
    log_level: str = "info",
) -> int:
    """
    Start the Reversi42 web server.

    Args:
        host: Host to bind to
        port: Port to run on
        player: AI opponent name
        open_browser: Whether to open browser automatically
        reload: Enable auto-reload for development
        log_level: Logging level

    Returns:
        Exit code (0 = success)
    """
    try:
        # Add src to path
        src_dir = Path(__file__).parent.parent
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))

        # Import after path is set
        import uvicorn

        # Print startup banner
        print("\n" + "=" * 80)
        print("🎮 REVERSI42 - AI-Powered Reversi/Othello")
        print("=" * 80)
        print(f"Version: {__version__}")
        print(f"Server:  http://{host}:{port}")
        print(f"AI:      {player}")
        print("=" * 80 + "\n")

        # Open browser in background thread if requested
        if open_browser:
            url = f"http://{'localhost' if host == '127.0.0.1' else host}:{port}"
            print(f"🌐 Opening browser in 1.5 seconds...")

            import threading

            browser_thread = threading.Thread(target=open_browser_delayed, args=(url,), daemon=True)
            browser_thread.start()

        # Configure server
        config = uvicorn.Config(
            "webgui.server.reversi42_server:app",
            host=host,
            port=port,
            log_level=log_level,
            reload=reload,
            reload_dirs=[str(src_dir)] if reload else None,
            access_log=log_level == "debug",
        )

        server = uvicorn.Server(config)

        # Track Ctrl+C presses for forced exit
        shutdown_count = [0]
        shutdown_initiated = [False]

        # Graceful shutdown handler for Ctrl+C
        def signal_handler(sig, frame):
            if shutdown_initiated[0]:
                # Already shutting down, force exit immediately
                print("\n⚠️  Force exit (Ctrl+C during shutdown)")
                import os
                os._exit(130)
            
            shutdown_count[0] += 1
            shutdown_initiated[0] = True
            count = shutdown_count[0]
            
            print(f"\n\n⚠️  Received shutdown signal (Ctrl+C) - Press #{count}")
            print("Closing connections and cleaning up...")
            
            # Set shutdown flag
            server.should_exit = True
            
            # Try aggressive shutdown
            try:
                if hasattr(server, 'shutdown'):
                    server.shutdown()
            except:
                pass
            
            # Force exit on second Ctrl+C
            if count >= 2:
                print("⚠️  Force shutdown (Ctrl+C pressed twice)")
                import os
                os._exit(130)
            
            # Set timeout - force exit if server doesn't stop
            import threading
            def force_exit_timeout():
                import time
                time.sleep(2)
                if shutdown_initiated[0]:
                    print("\n⚠️  Server not responding, forcing exit...")
                    import os
                    os._exit(130)
            
            timeout_thread = threading.Thread(target=force_exit_timeout, daemon=True)
            timeout_thread.start()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start server
        try:
            print("Press Ctrl+C to stop the server...")
            server.run()
            print("\n✅ Server stopped cleanly")
            return 0
        except KeyboardInterrupt:
            # This should be caught by signal handler, but just in case
            print("\n\n⚠️  Interrupted by user (KeyboardInterrupt)")
            shutdown_initiated[0] = True
            server.should_exit = True
            try:
                if hasattr(server, 'shutdown'):
                    server.shutdown()
            except:
                pass
            print("✅ Server stopped cleanly")
            return 130

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130

    except Exception as e:
        print(f"\n❌ Failed to start server: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


def main() -> int:
    """
    Main entry point (reversi42 command).
    Starts server with browser auto-open.
    """
    args = parse_args()

    # Handle list-players
    if args.list_players:
        return list_available_players()

    # Start server with browser
    return serve(
        host=args.host,
        port=args.port,
        player=args.player,
        open_browser=not args.no_browser,
        reload=args.reload,
        log_level=args.log_level,
    )


def serve_only() -> int:
    """
    Server-only entry point (reversi42-server command).
    Starts server WITHOUT browser auto-open.
    """
    # Parse args but force no-browser
    sys.argv.append("--no-browser")
    args = parse_args()

    # Handle list-players
    if args.list_players:
        return list_available_players()

    # Start server without browser
    return serve(
        host=args.host,
        port=args.port,
        player=args.player,
        open_browser=False,
        reload=args.reload,
        log_level=args.log_level,
    )


if __name__ == "__main__":
    sys.exit(main())
