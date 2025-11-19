"""
Pytest configuration and fixtures for WebGUI tests.

This file provides shared fixtures and configuration for all WebGUI tests.
"""

import asyncio
import os
import signal
import subprocess
import sys
import time
import urllib.request
from typing import Optional

import pytest

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)


@pytest.fixture(scope="session")
def event_loop_policy():
    """Set event loop policy for async tests"""
    return asyncio.get_event_loop_policy()


@pytest.fixture(scope="function")
async def cleanup_sessions():
    """Clean up sessions after each test"""
    yield

    # Clean up any remaining sessions
    try:
        from webgui.server.reversi42_server import active_connections, sessions

        sessions.clear()
        active_connections.clear()
    except ImportError:
        pass


@pytest.fixture
def mock_game_data():
    """Provide mock game data for tests"""
    return {
        "meta": {"variant": "Reversi/Othello", "size": 8},
        "players": {
            "black": {"name": "Test Player 1", "avatar": "TP1"},
            "white": {"name": "Test Player 2", "avatar": "TP2"},
        },
        "status": {"turn_by_ply": ["B"]},
        "positions": [
            {
                "A1": ".",
                "B1": ".",
                "C1": ".",
                "D1": ".",
                "E1": ".",
                "F1": ".",
                "G1": ".",
                "H1": ".",
                "A2": ".",
                "B2": ".",
                "C2": ".",
                "D2": ".",
                "E2": ".",
                "F2": ".",
                "G2": ".",
                "H2": ".",
                "A3": ".",
                "B3": ".",
                "C3": ".",
                "D3": ".",
                "E3": ".",
                "F3": ".",
                "G3": ".",
                "H3": ".",
                "A4": ".",
                "B4": ".",
                "C4": ".",
                "D4": "W",
                "E4": "B",
                "F4": ".",
                "G4": ".",
                "H4": ".",
                "A5": ".",
                "B5": ".",
                "C5": ".",
                "D5": "B",
                "E5": "W",
                "F5": ".",
                "G5": ".",
                "H5": ".",
                "A6": ".",
                "B6": ".",
                "C6": ".",
                "D6": ".",
                "E6": ".",
                "F6": ".",
                "G6": ".",
                "H6": ".",
                "A7": ".",
                "B7": ".",
                "C7": ".",
                "D7": ".",
                "E7": ".",
                "F7": ".",
                "G7": ".",
                "H7": ".",
                "A8": ".",
                "B8": ".",
                "C8": ".",
                "D8": ".",
                "E8": ".",
                "F8": ".",
                "G8": ".",
                "H8": ".",
            }
        ],
        "moves": [],
        "valid_by_ply": [["C4", "D3", "E6", "F5"]],
        "opening_by_ply": [],
        "notes": {"title": "Test Notes"},
    }


@pytest.fixture
def mock_statistics():
    """Provide mock AI statistics"""
    return {
        "nodes_searched": 10000,
        "nodes_pruned": 2000,
        "depth": 8,
        "null_move": {"cutoffs": 500},
        "futility": {"pruning_count": 300},
        "lmr": {"reductions": 200},
        "multi_cut": {"pruning_count": 100},
        "tt_hits": 1000,
        "tt_size": 100000,
    }


# Pytest markers
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "asyncio: mark test as async")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")


# Async test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# Server management for E2E tests
@pytest.fixture(scope="session")
def webgui_server():
    """
    Start the WebGUI server for E2E tests.
    
    This fixture starts the server in a subprocess and waits for it to be ready.
    The server is automatically stopped after all tests complete.
    """
    server_url = os.getenv("TEST_SERVER_URL", "http://localhost:8000")
    port = int(server_url.split(":")[-1].rstrip("/"))
    
    # Check if server is already running
    if _is_server_running(server_url):
        print(f"✓ Server already running at {server_url}, reusing it")
        yield server_url
        return
    
    # Start server in subprocess
    print(f"🚀 Starting WebGUI server on port {port}...")
    
    # Get Python executable
    python_exe = sys.executable
    
    # Start server process
    server_process = subprocess.Popen(
        [
            python_exe,
            "-m",
            "webgui.server.reversi42_server",
            "--port",
            str(port),
            "--host",
            "127.0.0.1",  # Use localhost instead of 0.0.0.0 for tests
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_root,
    )
    
    # Wait for server to be ready (max 30 seconds)
    max_wait = 30
    wait_interval = 0.5
    waited = 0
    
    while waited < max_wait:
        if _is_server_running(server_url):
            print(f"✓ Server is ready at {server_url}")
            break
        if server_process.poll() is not None:
            # Process exited unexpectedly
            stdout, stderr = server_process.communicate()
            error_msg = f"Server process exited unexpectedly:\nSTDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}"
            raise RuntimeError(error_msg)
        time.sleep(wait_interval)
        waited += wait_interval
    
    if not _is_server_running(server_url):
        server_process.terminate()
        server_process.wait(timeout=5)
        raise RuntimeError(f"Server failed to start within {max_wait} seconds")
    
    try:
        yield server_url
    finally:
        # Stop server
        print(f"🛑 Stopping WebGUI server...")
        try:
            server_process.terminate()
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print("⚠ Server didn't terminate gracefully, forcing kill...")
            server_process.kill()
            server_process.wait()
        print("✓ Server stopped")


def _is_server_running(url: str, timeout: float = 2.0) -> bool:
    """Check if server is running by making a request"""
    try:
        req = urllib.request.Request(url, method="HEAD")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except (urllib.error.URLError, OSError, TimeoutError):
        return False
