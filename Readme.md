````markdown
# Connect 4 Game

## Overview

This project is a **Connect 4 game** implemented in Python.  
You can play it locally on your computer.

---

## How to Run

### 1. Start Local HTTP Server (Optional)

Navigate to the project folder in your terminal and run:

```bash
python -m http.server 8000 --bind 127.0.0.1
```
````

Access the server at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 2. Run the Python Game

To play the game, run:

```bash
python app.py
```

Make sure you are in the same directory as `app.py`.

---

## Game Description

- **Connect 4** is a two-player game.
- Players take turns dropping colored discs into a 7-column, 6-row grid.
- The first player to connect four discs **vertically, horizontally, or diagonally** wins.
- If the board fills up without a winner, the game ends in a draw.

---

## Requirements

- Python 3.x installed
- Run all commands from the project directory
