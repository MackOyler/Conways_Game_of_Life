# Conway's Game of Life Simulation with Python

This project is a grid-based simulation of **Conway's Game of Life** implemented using Python and Pygame. Conway's Game of Life is a cellular automaton devised by mathematician John Conway. The simulation consists of a grid of cells that evolve through iterations based on a set of rules. The purpose is to simulate complex behaviors and patterns from simple rules, demonstrating principles of emergence and self-organization.

## Features

- **Interactive Grid**: Click to add or remove cells.
- **Automatic Updates**: Cells update their states based on the number of neighboring cells.
- **Controls**:
  - Spacebar to start/pause the simulation.
  - 'C' key to clear the grid.
  - 'G' key to generate a random set of cells.

## How It Works

### Main Components

1. **Initialization**:
    - Initialize Pygame and set up the display.
    - Define colors and grid dimensions.

2. **Grid Generation**:
    - The `gen(num)` function generates a set of random cell positions.

3. **Drawing the Grid**:
    - The `draw_grid(positions)` function draws the cells and the grid lines on the screen.

4. **Adjusting the Grid**:
    - The `adjust_grid(positions)` function updates the grid based on Conway's rules:
        - A live cell with 2 or 3 live neighbors survives.
        - A dead cell with exactly 3 live neighbors becomes a live cell.
        - All other cells die or remain dead.

5. **Neighbor Calculation**:
    - The `get_neighbors(pos)` function returns a list of neighboring cells for a given cell position.

### Main Loop

- The `main()` function contains the main loop of the simulation:
  - Handles user inputs (mouse clicks and keyboard presses).
  - Toggles cells on mouse click.
  - Controls the simulation start/pause with the spacebar.
  - Clears the grid with the 'C' key.
  - Generates random cells with the 'G' key.
  - Updates the display and grid based on the defined rules and user actions.

## Usage

To run the simulation, execute the script. The Pygame window will open, displaying the grid. You can interact with the grid and control the simulation using the mouse and keyboard.

### Controls

- **Mouse Click**: Toggle cell state (alive/dead).
- **Spacebar**: Start or pause the simulation.
- **'C' Key**: Clear the grid and stop the simulation.
- **'G' Key**: Generate a random set of cells.

## Development

Mack Oyler