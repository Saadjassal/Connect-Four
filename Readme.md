# Connect 4 Project

## Overview

This is a **Connect 4 game** implemented in Python. Play locally on your computer using the Python application.

## How to Run

1. **Start Local HTTP Server** (optional)  
   Navigate to this folder and run:
   ```bash
   python -m http.server 8000 --bind 127.0.0.1
   ```

````

This starts a server at `http://127.0.0.1:8000`.

2. **Run the Game**
   Run the Python application to play:

   ```bash
   python app.py
   ```

## Game Description

- **Connect 4** is a two-player game.
- Players take turns dropping colored discs into a 7-column, 6-row grid.
- The first player to connect four discs **vertically, horizontally, or diagonally** wins.
- If the board fills up without a winner, the game ends in a draw.

## Requirements

- Python 3.x installed
- Run all commands from the project directory
````
