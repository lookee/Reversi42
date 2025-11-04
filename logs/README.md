# Logs Directory

This directory contains application log files generated during runtime.

## Contents

- `server.log` - WebGUI server logs (FastAPI/Uvicorn)
- `*.log` - Other application logs

## Note

All `.log` files in this directory are automatically ignored by git.

Log files are generated automatically when running:
- `reversi42` - CLI command
- `reversi42-server` - Server-only mode
- `python -m webgui.server.reversi42_server` - Direct server execution

## Cleanup

To clean old logs:
```bash
rm -f logs/*.log
```

## Configuration

Log level can be set via:
```bash
reversi42 --log-level debug
reversi42 --log-level warning
```

