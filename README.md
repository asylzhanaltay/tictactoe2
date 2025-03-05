# tictactoe2
# Web-Based Tic Tac Toe Game

#### Video Demo: https://youtu.be/cUzXHB18Kvo

#### Description:

This project is a simple web version of the classic Tic Tac Toe game using Python and Flask. Two players are needed to play this game. Player "X" and Player "O". Player "X" always starts first. They take turns in placing Xs and Os into the grid to form a consecutive line of three Xs or Os horizontally, vertically or diagonally. The Player that achieves that wins, but if the board gets full before that (in 9 moves), the game result becomes draw.

## Project Structure

The project consists of the following files:

- `project.py`: Main Python file containing the game logic and Flask routes
- `test_project.py`: Test file containing unit tests for the game logic
- `templates/index.html`: HTML template for rendering the game interface
- `requirements.txt`: List of required Python packages

### project.py

This is the core file of the project, containing both the game logic and the Flask web application. It includes:

1. **Game Logic Functions**:
   - `create_board()`: Creates a new empty 3x3 game board.
   - `check_winner(board, player)`: Checks if a player has won by examining all rows, columns, and diagonals.
   - `is_board_full(board)`: Checks if the board is full, which would result in a draw.
   - `make_move(board, row, col, player)`: Updates the board with a player's move.

2. **Flask Routes**:
   - index or `/`: Starts new game session - initial "entrance".
   - `/move/: Handles player moves and updates the game state. Checks if any of the players have won and if the board is full. If neither, then the game proceeds.
   - `/reset`: Resets the game to start a new round.

3. **Main Function**:
   - `main()`: Runs the Flask application.

### test_project.py

This file contains unit tests for the game logic functions in `project.py`. The tests ensure that:
- The board is created correctly with the right dimensions and initial values.
- The win detection works for all winning patterns (rows, columns, diagonals).
- The full board detection works correctly for empty, partially filled, and full boards.
- The move function correctly updates the board and validates moves.

### templates/index.html

This HTML template file defines the structure and styling of the game interface.
#### Structure:
- A 3x3 grid representing the game board.
- When the X or O is inserted into the grid, they are displayed in a visually appealing way.
- The message on top shows whose turn is it now and who won the game or if it is a draw.
- A New Game button to start a new game and reset the board.
- Jinja2 templating is used for server-side rendering.
#### CSS Styling:
- Player marks are color coded - X in red, O in blue
- Minimalist design with nothing extra
- Everything centered, clean, negative space around Xs and Os.
#### A little bit of Java Script
- AJAX-based move submission to submit data without reloading the page or redirecting to another URL.
- Board updates after every move.
- Prevents invalid moves (it is impossible actually, but we did it just in case)
- Handles game over scenarios of Player X win, Player O win or draw (board full)
#### Session management
- Tracks current player
- Stores every move within one game
- Manages game status
- Provides message updates
- No need for servers or databases
- Easy reset functionality

### requirements.txt

This file lists the Python packages required to run the project:
- Flask: For the web application framework
- pytest: For running the unit tests

## Design Choices

### User Interface
The UI is intentionally kept simple and intuitive:
- Clear visual distinction between X and O with different colors
- Empty cells await for user move to submit form via AJAX.
- Filled cells and cells in a finished game are not clickable, clicking any part other than grid doesn't give any response
- Game status message clearly indicates whose turn it is or the game outcome

### Game Logic Separation
We deliberately separated the core game logic from the Flask routes to make the code more modular and maintainable. It helped us quickly  fix the bugs.

## How to Run the Project
1. Install the required packages:
   pip install -r requirements.txt
2. Run the application:
   python project.py
3. Open a web browser and go to `http://127.0.0.1:5000/`
4. To run the tests:
   pytest test_project.py

## Future Improvements
While this project meets the assignment requirements, there are several potential enhancements:
- Adding a computer opponent with easy, medium, difficult modes
- Implementing user accounts to track game statistics
- Adding a multiplayer mode over the network
- Creating a more visually appealing interface with animations (e.g. crossing out animation when a player wins, background music, mark appearance animation, etc.)
- Adding sound effects for moves and game outcomes
- Even revolutioning the game by creating 5 or 7 grid boards.
