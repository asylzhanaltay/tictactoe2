import pytest
from flask import session
from project import app, create_board, check_winner, is_board_full, make_move, main

# Test game logic functions
def test_create_board():
    board = create_board()
    assert len(board) == 3
    for row in board:
        assert len(row) == 3
        assert all(cell is None for cell in row)

def test_check_winner():
    # Test row wins
    board = [[None, None, None], [None, None, None], [None, None, None]]
    assert not check_winner(board, 'X')
    
    board = [['X', 'X', 'X'], [None, None, None], [None, None, None]]
    assert check_winner(board, 'X')
    
    board = [[None, None, None], ['X', 'X', 'X'], [None, None, None]]
    assert check_winner(board, 'X')
    
    board = [[None, None, None], [None, None, None], ['X', 'X', 'X']]
    assert check_winner(board, 'X')
    
    # Test column wins
    board = [['X', None, None], ['X', None, None], ['X', None, None]]
    assert check_winner(board, 'X')
    
    board = [[None, 'X', None], [None, 'X', None], [None, 'X', None]]
    assert check_winner(board, 'X')
    
    board = [[None, None, 'X'], [None, None, 'X'], [None, None, 'X']]
    assert check_winner(board, 'X')
    
    # Test diagonal wins
    board = [['X', None, None], [None, 'X', None], [None, None, 'X']]
    assert check_winner(board, 'X')
    
    board = [[None, None, 'X'], [None, 'X', None], ['X', None, None]]
    assert check_winner(board, 'X')
    
    # Test no winner
    board = [['X', 'O', 'X'], ['X', 'O', 'O'], ['O', 'X', 'O']]
    assert not check_winner(board, 'X')
    assert not check_winner(board, 'O')

    # Test with the other player
    board = [['O', 'O', 'O'], [None, None, None], [None, None, None]]
    assert check_winner(board, 'O')
    assert not check_winner(board, 'X')

def test_is_board_full():
    # Test empty board
    board = create_board()
    assert not is_board_full(board)
    
    # Test partially filled board
    board = [['X', 'O', 'X'], ['X', None, 'O'], ['O', 'X', 'O']]
    assert not is_board_full(board)
    
    # Test full board
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
    assert is_board_full(board)

def test_make_move():
    board = create_board()
    
    # Test valid move
    assert make_move(board, 0, 0, 'X')
    assert board[0][0] == 'X'
    
    # Test invalid move (cell already filled)
    assert not make_move(board, 0, 0, 'O')
    assert board[0][0] == 'X'  # Should remain 'X'
    
    # Test with the other player
    assert make_move(board, 1, 1, 'O')
    assert board[1][1] == 'O'
    
    # Ensure the board is correctly updated
    expected_board = [
        ['X', None, None],
        [None, 'O', None],
        [None, None, None]
    ]
    assert board == expected_board

# Flask route tests
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_route(client):
    with client.session_transaction() as sess:
        # Clear any existing session data
        sess.clear()
        
    response = client.get('/')
    assert response.status_code == 200
    
    # Check session data was initialized
    with client.session_transaction() as sess:
        assert 'board' in sess
        assert sess['current_player'] == 'X'
        assert sess['game_over'] is False
        assert sess['winner'] is None
        assert sess['message'] == "Player X's turn"
    
    # Check HTML content
    html = response.data.decode('utf-8')
    assert 'Tic Tac Toe' in html
    assert 'New Game' in html
    assert 'makeMove' in html  # Check JS function exists

def test_move_route(client):
    # Initialize session with a new game
    with client.session_transaction() as sess:
        sess.clear()
        sess['board'] = create_board()
        sess['current_player'] = 'X'
        sess['game_over'] = False
        sess['winner'] = None
        sess['message'] = "Player X's turn"
    
    # Make a valid move
    response = client.post('/move', data={'row': 0, 'col': 0})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['board'][0][0] == 'X'
    
    # Check that the session was updated
    with client.session_transaction() as sess:
        assert sess['board'][0][0] == 'X'
        assert sess['current_player'] == 'O'
    
    # Make an invalid move (cell already filled)
    response = client.post('/move', data={'row': 0, 'col': 0})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is False

def test_invalid_move_inputs(client):
    # Initialize session with a new game
    with client.session_transaction() as sess:
        sess.clear()
        sess['board'] = create_board()
        sess['current_player'] = 'X'
        sess['game_over'] = False
        sess['winner'] = None
        sess['message'] = "Player X's turn"
    
    # Test out of bounds - this will either return a JSON error or a 500 status
    response = client.post('/move', data={'row': 3, 'col': 0})
    if response.status_code == 200:
        data = response.get_json()
        assert not data.get('success', False)
    else:
        assert response.status_code >= 400
    
    # Test invalid types - will likely fail to convert to int
    response = client.post('/move', data={'row': 'a', 'col': '0'})
    if response.status_code == 200:
        data = response.get_json()
        assert not data.get('success', False)
    else:
        assert response.status_code >= 400

def test_win_condition(client):
    # Test winning scenario
    with client.session_transaction() as sess:
        sess.clear()
        sess['board'] = [
            ['X', 'X', None],
            ['O', 'O', None],
            [None, None, None]
        ]
        sess['current_player'] = 'X'
        sess['game_over'] = False
        sess['winner'] = None
        sess['message'] = "Player X's turn"
    
    response = client.post('/move', data={'row': 0, 'col': 2})
    data = response.get_json()
    assert data['success'] is True
    assert data['game_over'] is True
    assert "Player X wins" in data['message']
    
    # Check session data after win
    with client.session_transaction() as sess:
        assert sess['game_over'] is True
        assert sess['winner'] == 'X'

def test_draw_condition(client):
    # Test draw scenario
    with client.session_transaction() as sess:
        sess.clear()
        sess['board'] = [
            ['X', 'O', 'X'],
            ['X', 'O', 'X'],
            ['O', 'X', None]
        ]
        sess['current_player'] = 'O'
        sess['game_over'] = False
        sess['winner'] = None
        sess['message'] = "Player O's turn"
    
    response = client.post('/move', data={'row': 2, 'col': 2})
    data = response.get_json()
    assert data['success'] is True
    assert data['game_over'] is True
    assert "draw" in data['message'].lower()
    
    # Check session data after draw
    with client.session_transaction() as sess:
        assert sess['game_over'] is True
        assert sess['winner'] is None

def test_game_over_move(client):
    # Test moves after game is over
    with client.session_transaction() as sess:
        sess.clear()
        sess['board'] = [
            ['X', 'X', 'X'],
            ['O', 'O', None],
            [None, None, None]
        ]
        sess['current_player'] = 'O'
        sess['game_over'] = True
        sess['winner'] = 'X'
        sess['message'] = "Player X wins!"
    
    response = client.post('/move', data={'row': 1, 'col': 2})
    data = response.get_json()
    assert data['success'] is False
    assert "Game is over" in data['message']

def test_reset_route(client):
    # First set up a non-initial game state
    with client.session_transaction() as sess:
        sess.clear()
        sess['board'] = [
            ['X', 'O', None],
            [None, 'X', None],
            [None, None, 'O']
        ]
        sess['current_player'] = 'X'
        sess['game_over'] = False
        sess['winner'] = None
        sess['message'] = "Player X's turn"
    
    # Reset the game
    response = client.post('/reset')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Check that the session was reset
    with client.session_transaction() as sess:
        assert all(all(cell is None for cell in row) for row in sess['board'])
        assert sess['current_player'] == 'X'
        assert sess['game_over'] is False
        assert sess['winner'] is None
        assert sess['message'] == "Player X's turn"

def test_main_function(monkeypatch):
    # Mock app.run to avoid actually starting a server
    run_called = False
    
    def mock_run(debug=False, host='127.0.0.1'):
        nonlocal run_called
        run_called = True
        assert debug is True
        assert host == '0.0.0.0'
    
    monkeypatch.setattr(app, 'run', mock_run)
    
    # Call main function
    main()
    
    # Check that app.run was called
    assert run_called