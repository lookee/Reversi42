# Reversi42 WebGUI Test Suite

Comprehensive test suite for the Reversi42 web interface, covering backend, frontend, and end-to-end testing.

## Test Structure

```
tests/webgui/
├── test_backend_server.py      # Backend WebSocket server tests
├── test_websocket_observer.py  # WebSocket observer tests
├── test_frontend.js            # Frontend JavaScript tests
├── test_e2e.py                 # End-to-end integration tests
├── package.json                # JavaScript dependencies
└── README.md                   # This file
```

## Test Coverage

### Backend Tests (`test_backend_server.py`)
- ✅ WebSocket connection lifecycle
- ✅ Message handling (init, moves, reset, undo/redo)
- ✅ Game state management
- ✅ AI integration
- ✅ Session management
- ✅ Error handling and edge cases
- ✅ Multiple concurrent sessions
- ✅ Opening book integration

### Observer Tests (`test_websocket_observer.py`)
- ✅ Observer lifecycle (start/complete)
- ✅ Real-time notifications
- ✅ Statistics tracking
- ✅ Message formatting
- ✅ Aspiration window tracking
- ✅ Parallel search notifications
- ✅ Performance metrics

### Frontend Tests (`test_frontend.js`)
- ✅ Board rendering
- ✅ Move validation
- ✅ JSON parsing
- ✅ UI interactions
- ✅ History navigation
- ✅ Utility functions
- ✅ Edge cases
- ✅ Performance benchmarks

### E2E Tests (`test_e2e.py`)
- ✅ Complete user workflows
- ✅ Browser compatibility (Chrome, Firefox, Safari)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ WebSocket communication
- ✅ Performance testing
- ✅ Accessibility
- ✅ Error handling

## Installation

### Python Dependencies

```bash
# Install all development dependencies
pip install -r requirements-dev.txt

# Install Playwright browsers
playwright install
```

### JavaScript Dependencies

```bash
# Navigate to tests/webgui directory
cd tests/webgui

# Install Node.js dependencies
npm install
```

## Running Tests

### All Tests

```bash
# Run all Python tests
pytest tests/webgui/ -v

# Run with coverage
pytest tests/webgui/ -v --cov=src/webgui --cov-report=html

# Run in parallel
pytest tests/webgui/ -v -n auto
```

### Backend Tests Only

```bash
# Basic run
pytest tests/webgui/test_backend_server.py -v

# With detailed output
pytest tests/webgui/test_backend_server.py -v -s

# Specific test class
pytest tests/webgui/test_backend_server.py::TestGameSession -v

# Specific test
pytest tests/webgui/test_backend_server.py::TestGameSession::test_game_session_creation -v
```

### Observer Tests Only

```bash
pytest tests/webgui/test_websocket_observer.py -v
```

### Frontend Tests (JavaScript)

```bash
# Navigate to tests/webgui
cd tests/webgui

# Run all frontend tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Run with verbose output
npm run test:verbose
```

### E2E Tests

```bash
# Make sure server is running first!
# In one terminal:
cd src/webgui
python backend_server.py --port 8000

# In another terminal:
pytest tests/webgui/test_e2e.py -v

# Run with specific browser
pytest tests/webgui/test_e2e.py -v --browser firefox

# Run headful (see browser)
pytest tests/webgui/test_e2e.py -v --headed
```

## Test Configuration

### Environment Variables

```bash
# Set test server URL (default: http://localhost:8000)
export TEST_SERVER_URL=http://localhost:8000

# Run tests
pytest tests/webgui/test_e2e.py -v
```

### Pytest Configuration

Add to `pyproject.toml` or `pytest.ini`:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    asyncio: mark test as async
    e2e: mark test as end-to-end
    slow: mark test as slow running
```

## Test Scenarios Covered

### Critical User Journeys
1. **Game Start** → Load page → See initial board → Verify 4 discs
2. **Make Move** → Click valid move → Board updates → Turn switches
3. **AI Move** → AI responds → Board updates → Game continues
4. **Undo/Redo** → Undo move → Board reverts → Redo → Board restores
5. **Game Complete** → Play to end → See winner → Final score

### Edge Cases
1. **Invalid Moves** → Click invalid cell → Error message → No state change
2. **Network Issues** → Disconnect → Reconnect → Resume game
3. **Rapid Clicks** → Multiple quick clicks → Only valid moves register
4. **Browser Refresh** → Refresh page → Game state preserved/reset
5. **Malformed Data** → Invalid JSON → Graceful error handling
6. **Empty History** → Undo at start → No crash → State consistent
7. **Concurrent Sessions** → Multiple games → Independent state
8. **Large Statistics** → 1B+ nodes → No overflow → Correct display

### Performance Benchmarks
- Page load: < 5 seconds
- Initial render: < 2 seconds
- Move response: < 500ms
- AI thinking: < 30 seconds (depth 8)
- WebSocket latency: < 100ms

## Continuous Integration

### GitHub Actions Example

```yaml
name: WebGUI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
        playwright install
    
    - name: Run backend tests
      run: pytest tests/webgui/test_backend_server.py -v
    
    - name: Run observer tests
      run: pytest tests/webgui/test_websocket_observer.py -v
    
    - name: Start server for E2E
      run: |
        python src/webgui/backend_server.py --port 8000 &
        sleep 5
    
    - name: Run E2E tests
      run: pytest tests/webgui/test_e2e.py -v
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install Node dependencies
      run: |
        cd tests/webgui
        npm install
    
    - name: Run frontend tests
      run: |
        cd tests/webgui
        npm test
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Troubleshooting

### Tests Failing?

1. **Server not running**: Start backend server first for E2E tests
   ```bash
   python src/webgui/backend_server.py --port 8000
   ```

2. **Module not found**: Install dependencies
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Playwright errors**: Install browsers
   ```bash
   playwright install
   ```

4. **Jest errors**: Install Node dependencies
   ```bash
   cd tests/webgui && npm install
   ```

5. **Async warnings**: Install pytest-asyncio
   ```bash
   pip install pytest-asyncio
   ```

### Common Issues

**Issue**: `WebSocket connection failed`
**Solution**: Ensure server is running and accessible

**Issue**: `Timeout waiting for selector`
**Solution**: Increase timeout or check if element exists

**Issue**: `Jest not found`
**Solution**: Run `npm install` in tests/webgui directory

**Issue**: `Module 'src.webgui' not found`
**Solution**: Run tests from project root, not from tests directory

## Coverage Reports

### Generate Coverage

```bash
# Python coverage
pytest tests/webgui/ --cov=src/webgui --cov-report=html
open htmlcov/index.html

# JavaScript coverage
cd tests/webgui
npm run test:coverage
open coverage/index.html
```

### Coverage Goals
- Backend: > 80%
- Frontend: > 70%
- E2E: Critical paths 100%

## Performance Profiling

### Profile Tests

```bash
# Profile test execution
pytest tests/webgui/test_backend_server.py --profile

# Profile with py-spy
py-spy record -o profile.svg -- pytest tests/webgui/test_backend_server.py
```

## Contributing

When adding new features, please:

1. ✅ Add corresponding tests
2. ✅ Ensure all tests pass
3. ✅ Maintain > 80% coverage
4. ✅ Update this README if needed
5. ✅ Follow existing test patterns

## Test Statistics

- **Total Tests**: 150+
- **Backend Tests**: 60+
- **Observer Tests**: 30+
- **Frontend Tests**: 40+
- **E2E Tests**: 20+
- **Average Runtime**: < 2 minutes
- **Coverage**: > 80%

## License

GPL-3.0-or-later - Same as Reversi42 project

## Author

Luca Amore - luca.amore@gmail.com

## Support

For issues or questions:
1. Check this README
2. Review test output
3. Check server logs
4. Open an issue on GitHub

