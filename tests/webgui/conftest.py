"""
Pytest configuration and fixtures for WebGUI tests.

This file provides shared fixtures and configuration for all WebGUI tests.
"""

import asyncio
import os
import subprocess
import sys
import time
import urllib.request

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

    If the server fails to start, the fixture will skip all E2E tests to prevent
    CI timeouts while maintaining quality checks.
    """
    # Use different port for each pytest-xdist worker to avoid conflicts
    base_port = 8000
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "")
    if worker_id:
        # Extract worker number from worker ID (e.g., "gw0" -> 0, "gw1" -> 1)
        try:
            worker_num = int(worker_id.replace("gw", ""))
            port = base_port + worker_num
        except ValueError:
            port = base_port
    else:
        port = base_port

    server_url = os.getenv("TEST_SERVER_URL", f"http://localhost:{port}")

    # Check if server is already running
    if _is_server_running(server_url):
        print(f"✓ Server already running at {server_url}, reusing it")
        yield server_url
        return

    # Start server in subprocess
    print(f"🚀 Starting WebGUI server on port {port}...")

    # Get Python executable
    python_exe = sys.executable

    # Verify required dependencies are available
    try:
        import fastapi
        import uvicorn

        print(f"✓ Dependencies found: fastapi={fastapi.__version__}, uvicorn={uvicorn.__version__}")
    except ImportError as e:
        error_msg = f"Required dependencies not installed: {e}\n"
        error_msg += "Please install: pip install fastapi uvicorn[standard]"
        raise RuntimeError(error_msg)

    # Start server process
    # Set PYTHONPATH to include src directory so webgui module can be found
    # Use absolute path and proper path separator for cross-platform compatibility
    env = os.environ.copy()
    src_dir_abs = os.path.abspath(src_dir)
    existing_pythonpath = env.get("PYTHONPATH", "")
    if existing_pythonpath:
        env["PYTHONPATH"] = src_dir_abs + os.pathsep + existing_pythonpath
    else:
        env["PYTHONPATH"] = src_dir_abs

    # Verify module can be imported
    try:
        import importlib.util

        server_module_path = os.path.join(src_dir_abs, "webgui", "server", "reversi42_server.py")
        if not os.path.exists(server_module_path):
            raise RuntimeError(f"Server module not found at: {server_module_path}")
        print(f"✓ Server module found at: {server_module_path}")
    except Exception as e:
        raise RuntimeError(f"Cannot verify server module: {e}")

    # Verify module can be imported
    try:
        import importlib.util

        server_module_path = os.path.join(src_dir_abs, "webgui", "server", "reversi42_server.py")
        if not os.path.exists(server_module_path):
            raise RuntimeError(f"Server module not found at: {server_module_path}")
        print(f"✓ Server module found at: {server_module_path}")
    except Exception as e:
        raise RuntimeError(f"Cannot verify server module: {e}")

    # Try multiple approaches for cross-platform compatibility
    # Approach 1: Use python -m with PYTHONPATH set (most reliable)
    # This works better on Windows where direct file execution can have issues
    server_process = None
    server_start_error = None

    # First try: python -m webgui.server.reversi42_server
    try:
        # On Windows, use CREATE_NO_WINDOW flag to avoid console window
        creation_flags = 0
        if sys.platform == "win32":
            import subprocess as subprocess_module

            creation_flags = subprocess_module.CREATE_NO_WINDOW

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
            stderr=subprocess.STDOUT,  # Merge stderr into stdout for easier debugging
            cwd=project_root,
            env=env,
            universal_newlines=True,  # Text mode for better cross-platform handling
            bufsize=1,  # Line buffered
            creationflags=creation_flags if sys.platform == "win32" else 0,
        )
        # Give it more time to start (longer in CI)
        wait_time = 2.0 if os.getenv("CI") else (1.0 if sys.platform == "win32" else 0.5)
        time.sleep(wait_time)

        # Check if process is still running
        if server_process.poll() is None:
            # Process is still running, good!
            print(f"✓ Server process started (PID: {server_process.pid})")
            # Try to read initial output to verify it's starting correctly
            if server_process.stdout:
                try:
                    import select

                    if sys.platform != "win32":
                        # Non-blocking read
                        if select.select([server_process.stdout], [], [], 0.5)[0]:
                            initial_line = server_process.stdout.readline()
                            if initial_line:
                                print(f"  Server output: {initial_line.strip()}")
                except Exception:
                    pass  # Ignore read errors
        else:
            # Process exited, try fallback
            returncode = server_process.returncode
            try:
                stdout, _ = server_process.communicate(timeout=2)
                server_start_error = f"Process exited with code {returncode}\n"
                if stdout:
                    server_start_error += f"Output:\n{stdout}"
                else:
                    server_start_error += "No output captured"
            except subprocess.TimeoutExpired:
                server_start_error = (
                    f"Process exited with code {returncode} before we could read output"
                )
            print(f"❌ Server process exited immediately: {server_start_error}")
            server_process = None
    except Exception as e:
        server_start_error = str(e)
        server_process = None

    # Fallback: Use direct file path if module approach failed
    if server_process is None:
        server_file = os.path.join(src_dir_abs, "webgui", "server", "reversi42_server.py")
        server_file = os.path.normpath(server_file)

        # Verify file exists before starting
        if not os.path.exists(server_file):
            error_msg = f"Server file not found: {server_file}\n"
            error_msg += f"src_dir_abs: {src_dir_abs}\n"
            error_msg += f"project_root: {project_root}\n"
            if server_start_error:
                error_msg += f"Previous attempt error: {server_start_error}"
            raise RuntimeError(error_msg)

        try:
            # On Windows, use CREATE_NO_WINDOW flag to avoid console window
            creation_flags = 0
            if sys.platform == "win32":
                import subprocess as subprocess_module

                creation_flags = subprocess_module.CREATE_NO_WINDOW

            server_process = subprocess.Popen(
                [
                    python_exe,
                    server_file,
                    "--port",
                    str(port),
                    "--host",
                    "127.0.0.1",  # Use localhost instead of 0.0.0.0 for tests
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout for easier debugging
                cwd=project_root,
                env=env,
                universal_newlines=True,  # Text mode for better cross-platform handling
                bufsize=1,  # Line buffered
                creationflags=creation_flags if sys.platform == "win32" else 0,
            )
            # Give it more time to start on Windows
            wait_time = 1.0 if sys.platform == "win32" else 0.5
            time.sleep(wait_time)
        except Exception as e:
            error_msg = f"Failed to start server with both approaches:\n"
            error_msg += f"Module approach error: {server_start_error}\n"
            error_msg += f"File approach error: {str(e)}"
            raise RuntimeError(error_msg)

    # Wait for server to be ready (longer timeout for CI environments)
    # CI environments may be slower, so increase timeout
    max_wait = 60.0 if os.getenv("CI") else (45.0 if sys.platform == "win32" else 30.0)
    wait_interval = 0.5
    waited = 0.0
    last_output = ""

    # Try to read initial output to catch early errors
    if server_process.stdout:
        try:
            # Non-blocking read attempt
            import select

            if sys.platform != "win32":  # select doesn't work with pipes on Windows
                if select.select([server_process.stdout], [], [], 0.1)[0]:
                    line = server_process.stdout.readline()
                    if line:
                        last_output += line
        except Exception:
            pass  # Ignore errors in non-blocking read

    while waited < max_wait:
        if _is_server_running(server_url):
            print(f"✓ Server is ready at {server_url}")
            break
        if server_process.poll() is not None:
            # Process exited unexpectedly - get error output immediately
            try:
                # Try to read remaining output
                remaining_output = ""
                if server_process.stdout:
                    try:
                        import select

                        if sys.platform != "win32":
                            while select.select([server_process.stdout], [], [], 0.1)[0]:
                                line = server_process.stdout.readline()
                                if not line:
                                    break
                                remaining_output += line
                    except Exception:
                        pass

                stdout, _ = server_process.communicate(timeout=2)
                # Since stderr is redirected to stdout, stdout contains everything
                # stdout is already a string when universal_newlines=True
                output_str = stdout if stdout else ""
                if remaining_output:
                    output_str = remaining_output + output_str
                if last_output:
                    output_str = last_output + output_str
            except subprocess.TimeoutExpired:
                output_str = last_output if last_output else ""

            error_msg = (
                f"Server process exited unexpectedly (returncode: {server_process.returncode})"
            )
            if output_str:
                # Limit output to last 2000 chars to avoid huge error messages
                if len(output_str) > 2000:
                    output_str = "... (truncated) ...\n" + output_str[-2000:]
                error_msg += f"\nOutput:\n{output_str}"
            else:
                error_msg += "\n(No output captured - server may have crashed silently)"
            raise RuntimeError(error_msg)

        # Try to read output periodically to catch errors early
        if server_process.stdout and waited % 2 == 0:  # Every 1 second
            try:
                import select

                if sys.platform != "win32":
                    if select.select([server_process.stdout], [], [], 0.1)[0]:
                        line = server_process.stdout.readline()
                        if line:
                            last_output += line
                            # Keep only last 1000 chars
                            if len(last_output) > 1000:
                                last_output = last_output[-1000:]
            except Exception:
                pass

        time.sleep(wait_interval)
        waited += wait_interval

    if not _is_server_running(server_url):
        # Get error output before terminating
        try:
            stdout, _ = server_process.communicate(timeout=2)
            # Since stderr is redirected to stdout, stdout contains everything
            # stdout is already a string when universal_newlines=True
            output_str = stdout if stdout else ""
            if last_output:
                output_str = last_output + output_str
        except subprocess.TimeoutExpired:
            output_str = last_output if last_output else ""

        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()

        # Get detailed error information
        error_msg = f"Server failed to start within {max_wait} seconds"
        if output_str:
            # Show full output for debugging
            if len(output_str) > 2000:
                error_msg += (
                    f"\nLast 2000 chars of output:\n... (truncated) ...\n{output_str[-2000:]}"
                )
            else:
                error_msg += f"\nFull output:\n{output_str}"
        else:
            error_msg += "\n(No output captured - server may have crashed silently)"

        # Print error for debugging
        print(f"\n❌ Server startup failed:\n{error_msg}")
        print(f"\nDebug info:")
        print(f"  - Python executable: {python_exe}")
        print(f"  - PYTHONPATH: {env.get('PYTHONPATH', 'not set')}")
        print(f"  - Port: {port}")
        print(f"  - Server URL: {server_url}")
        print(f"  - Project root: {project_root}")
        print(f"  - Source dir: {src_dir_abs}")

        # Raise error instead of skipping - we want to fix the issue
        raise RuntimeError(error_msg)

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
        req = urllib.request.Request(url, method="GET")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except (urllib.error.URLError, OSError, TimeoutError):
        return False
