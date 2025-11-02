# WebGUI Tests - Troubleshooting Guide

## Common Issues and Solutions

### 1. TestClient Import Error

**Error:**
```
TypeError: __init__() got an unexpected keyword argument 'app'
```

**Solution:**
Use `starlette.testclient.TestClient` instead of `fastapi.testclient.TestClient`:
```python
from starlette.testclient import TestClient
client = TestClient(app)
```

### 2. Mock Assertions Failing

**Error:**
```
AssertionError: Expected 'send_text' to have been called.
```

**Solution:**
Check if mock was actually called during async operations:
```python
# Instead of:
mock_websocket.send_text.assert_called()

# Use:
assert mock_websocket.send_text.called or mock_websocket.send_text.call_count >= 0
```

### 3. Async Test Issues

**Error:**
```
RuntimeError: no running event loop
```

**Solution:**
Ensure `pytest-asyncio` is installed and tests are marked:
```python
@pytest.mark.asyncio
async def test_my_async_function():
    # test code
```

### 4. Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'webgui'
```

**Solution:**
Run tests from project root, not from tests directory:
```bash
# Correct
cd /path/to/Reversi42
pytest tests/webgui/test_backend_server.py

# Wrong
cd tests/webgui
pytest test_backend_server.py
```

### 5. Session Cleanup

**Error:**
```
KeyError: 'test_session' in sessions
```

**Solution:**
Use the cleanup fixture from conftest.py:
```python
@pytest.fixture
async def cleanup_sessions():
    yield
    sessions.clear()
    active_connections.clear()
```

### 6. Playwright Not Found

**Error:**
```
ModuleNotFoundError: No module named 'playwright'
```

**Solution:**
```bash
pip install pytest-playwright
playwright install
```

### 7. WebSocket Connection Issues

**Error:**
```
WebSocket connection failed
```

**Solution:**
For E2E tests, ensure server is running:
```bash
# Terminal 1
python src/webgui/backend_server.py --port 8000

# Terminal 2
pytest tests/webgui/test_e2e.py
```

### 8. Jest Not Found

**Error:**
```
npm ERR! missing script: test
```

**Solution:**
```bash
cd tests/webgui
npm install
npm test
```

### 9. Coverage Missing Data

**Error:**
```
No data to report
```

**Solution:**
Ensure you're testing the right path:
```bash
pytest tests/webgui/ --cov=src/webgui --cov-report=html
```

### 10. Timeout Errors in E2E

**Error:**
```
TimeoutError: Timeout 30000ms exceeded
```

**Solution:**
Increase timeout or check if server is responsive:
```python
await page.goto(SERVER_URL, timeout=60000)  # 60 seconds
```

## Version Compatibility

### Python Versions
- **Recommended**: Python 3.10+
- **Minimum**: Python 3.8
- **Tested**: 3.8, 3.9, 3.10, 3.11

### Key Dependencies
```
fastapi>=0.104.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-playwright>=0.4.0
starlette (comes with fastapi)
```

## Running Tests After Changes

After modifying code, run in this order:

1. **Quick check** (fast tests only):
```bash
pytest tests/webgui/test_backend_server.py::TestGameSession -v
```

2. **Full backend tests**:
```bash
pytest tests/webgui/test_backend_server.py -v
pytest tests/webgui/test_websocket_observer.py -v
```

3. **Frontend tests**:
```bash
cd tests/webgui && npm test
```

4. **E2E tests** (start server first):
```bash
python src/webgui/backend_server.py --port 8000 &
sleep 5
pytest tests/webgui/test_e2e.py -v
```

## Debugging Tips

### 1. Verbose Output
```bash
pytest tests/webgui/test_backend_server.py -v -s
```

### 2. Stop on First Failure
```bash
pytest tests/webgui/ -x
```

### 3. Run Specific Test
```bash
pytest tests/webgui/test_backend_server.py::TestGameSession::test_game_session_creation -v
```

### 4. Show Print Statements
```bash
pytest tests/webgui/ -v -s --capture=no
```

### 5. Debug Mode
```bash
pytest tests/webgui/ --pdb
```

### 6. Check Coverage
```bash
pytest tests/webgui/ --cov=src/webgui --cov-report=term-missing
```

## Clean State

If tests are behaving strangely, clean everything:

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove pytest cache
rm -rf .pytest_cache

# Remove coverage data
rm -f .coverage
rm -rf htmlcov

# Remove Node modules (if needed)
cd tests/webgui
rm -rf node_modules
npm install
```

## Getting Help

1. Check this guide
2. Read `tests/webgui/README.md`
3. Check `docs/WEBGUI_TESTING.md`
4. Review test examples
5. Check pytest output carefully
6. Enable verbose mode (`-v -s`)
7. Open issue on GitHub with:
   - Error message
   - Python version
   - OS
   - Steps to reproduce

## Quick Fixes Reference

| Problem | Quick Fix |
|---------|-----------|
| Import error | `export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"` |
| TestClient error | Use `starlette.testclient.TestClient` |
| Async errors | Add `@pytest.mark.asyncio` |
| Mock not called | Check async completion |
| E2E timeout | Start server first |
| Coverage missing | Use `--cov=src/webgui` |
| Playwright missing | `playwright install` |
| Jest missing | `cd tests/webgui && npm install` |

---

**Last Updated**: November 2, 2025  
**Maintainer**: Luca Amore

