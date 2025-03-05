from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "tic-tac-toe-secret-key"

def create_board():
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
    return board

def check_winner(board, player):
    for row in board:
        if row.count(player) == 3:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_board_full(board):
    for row in board:
        if None in row:
            return False
    return True

def make_move(board, row, col, player): 
    if row < 0 or row >= 3 or col < 0 or col >= 3:
        return False
    if board[row][col] is None:
        board[row][col] = player
        return True
    return False

@app.route('/')
def index():
    if 'board' not in session:
        session['board'] = create_board()
        session['current_player'] = 'X'
        session['game_over'] = False
        session['winner'] = None
        session['message'] = "Player X's turn"
    
    return render_template('index.html', 
                          board=session['board'], 
                          message=session['message'],
                          game_over=session['game_over'])

@app.route('/move', methods=['POST'])
def move():
    if session.get('game_over', True):
        return jsonify(success=False, message="Game is over. Start a new game.")
    row = int(request.form.get('row', -1))
    col = int(request.form.get('col', -1))
    board = session['board']
    player = session['current_player']
    
    if make_move(board, row, col, player):
        if check_winner(board, player):
            session['game_over'] = True
            session['winner'] = player
            session['message'] = f"Player {player} wins!"
        elif is_board_full(board):
            session['game_over'] = True
            session['message'] = "It's a draw!"
        else:
            if session['current_player'] == 'X':
                session['current_player'] = 'O'
            elif session['current_player'] == 'O':
                session['current_player'] = 'X'
            current_player = session['current_player']
            session['message'] = f"Player {current_player}'s turn"
        session['board'] = board
        
        return jsonify(
            success=True,
            board=session['board'],
            message=session['message'],
            game_over=session['game_over']
        )
    
    return jsonify(success=False, message="Invalid move")

@app.route('/reset', methods=['POST'])
def reset():
    session['board'] = create_board()
    session['current_player'] = 'X'
    session['game_over'] = False
    session['winner'] = None
    session['message'] = "Player X's turn"
    
    return jsonify(
        success=True,
        board=session['board'],
        message=session['message'],
        game_over=session['game_over']
    )

def main():
    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    main()

'''
We have used Claude to get instructions on how to efficiently execute our project idea. 
And we also used CS50 duck to understand certain concepts in the code like jsonify, sessions, etc. 
Claude helped us debug our code – we had a problem of the game not resetting, not ending even if the board is full, also we couldn't understand how to submit the data in web to our code.
It was a really cool experience that helped us learn a lot!
We used it mostly to guide and educated us. So the code was written by us, but AI helped us debug, understand and optimize.
'''