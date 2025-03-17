# Snake Game

## Overview
This project is a classic Snake game built using Python and Pygame. The game features a graphical interface where the player controls a snake to collect apples while avoiding collisions with itself.

## Project Structure
- **snake.py**: Contains the game logic, including movement, collision detection, and score tracking.
- **apple.jpg**: Image used to represent the apple in the game.
- **block.jpg**: Image used to represent the snake's body.
- **data.json**: Stores the highest score (record) achieved.

## Dependencies
To run the project, install the following dependencies:
```sh
pip install pygame numpy json
```

## Running the Game
To play the game manually, execute:
```sh
python snake.py
```

## Features
- Snake moves and wraps around screen edges.
- Apples are randomly placed and collected to increase score.
- High score tracking using `data.json`.
- Adjustable game speed using number keys (1-4).
- Game over screen with restart option.

## Future Improvements
- Add sound effects and background music.
- Implement different game modes (e.g., obstacles, power-ups).


