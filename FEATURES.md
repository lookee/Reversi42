# Reversi42 - New Features

## Overview
This document describes the new features added to Reversi42, including a splash screen, menu system, and enhanced game controls.

## New Features

### 1. Splash Screen
- Displays the Reversi42 logo on startup
- Shows for 3 seconds before transitioning to the main menu
- Falls back to a text-based splash if the image is not found

### 2. Player Selection Menu
- Elegant menu system with cursor navigation
- Select player types for both Black and White:
  - **Human**: Human player with mouse and keyboard controls
  - **AI**: Computer player with configurable difficulty
  - **Monkey**: Random move player
- AI difficulty levels from 1-10 (depth of search)
- Navigate with arrow keys, select with ENTER, go back with ESC

### 3. Enhanced Game Controls
- **Mouse Controls**: Click on any valid move to select it
- **Keyboard Navigation**: 
  - Press 'C' to toggle cursor navigation mode
  - Use arrow keys to move the yellow cursor
  - Press ENTER or SPACE to select the move at cursor position
  - Press ESC or Q to quit the game

### 4. Visual Improvements
- **Smaller Move Indicators**: Possible moves now show as smaller circles
- **Yellow Cursor**: Elegant yellow rectangle highlights the selected position
- **Red Last Move**: Red dot indicates the last move played
- **Hoshi Points**: Reference dots at board intersections

## How to Play

1. **Start the Game**: Run `python3 src/reversi42.py`
2. **Configure Players**: Use the menu to select player types and AI difficulty
3. **Start Game**: Select "Start Game" from the menu
4. **Make Moves**: 
   - Click on highlighted circles to make moves
   - Or press 'C' and use arrow keys for keyboard navigation
5. **Game End**: The game shows final results and piece counts

## Controls Summary

### Menu Navigation
- **Arrow Keys**: Navigate menu options
- **ENTER**: Select option
- **ESC**: Go back or exit

### Game Controls
- **Mouse Click**: Select move
- **C Key**: Toggle cursor navigation mode
- **Arrow Keys**: Move cursor (when in cursor mode)
- **ENTER/SPACE**: Select move at cursor
- **ESC/Q**: Quit game

## Technical Details

### Files Modified/Created
- `src/Menu.py`: New menu system with splash screen
- `src/Board/BoardView.py`: Enhanced with cursor navigation and smaller move indicators
- `src/Board/BoardControl.py`: Added keyboard controls and cursor mode
- `src/reversi42.py`: Updated to use menu system

### Player Types
- **HumanPlayer**: Interactive player with full control options
- **AIPlayer**: Minimax algorithm with configurable depth
- **Monkey**: Random move selection for testing

The game maintains full compatibility with the original Reversi rules while providing a much more user-friendly and feature-rich experience.
