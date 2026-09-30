import unittest
import os

# Set dummy video driver so pygame tests run headlessly without opening an actual window
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()

from game.rules import check_winner, is_board_full
from game.game_engine import GameEngine


class TestTicTacToe(unittest.TestCase):
    def test_diagonal_wins(self):
        # Task 1: Test main diagonal win
        board_diag1 = [
            ['X', 'O', None],
            ['O', 'X', None],
            [None, None, 'X']
        ]
        self.assertEqual(check_winner(board_diag1), 'X')

        # Task 1: Test anti-diagonal win
        board_diag2 = [
            [None, 'X', 'O'],
            ['X', 'O', None],
            ['O', None, 'X']
        ]
        self.assertEqual(check_winner(board_diag2), 'O')

    def test_win_on_last_move_is_not_draw(self):
        # Task 1: Board is completely full, but X has a winning row
        board = [
            ['X', 'X', 'X'],
            ['O', 'X', 'O'],
            ['O', 'O', 'X']
        ]
        engine = GameEngine()
        engine.board = board
        engine.check_round_end()
        self.assertTrue(engine.round_over)
        self.assertEqual(engine.winner, 'X', "Win on full board must be declared a win, not draw")
        self.assertEqual(engine.scores['X'], 1)
        self.assertEqual(engine.scores['Draw'], 0)

    def test_genuine_draw(self):
        board = [
            ['X', 'O', 'X'],
            ['X', 'O', 'O'],
            ['O', 'X', 'X']
        ]
        engine = GameEngine()
        engine.board = board
        engine.check_round_end()
        self.assertTrue(engine.round_over)
        self.assertIsNone(engine.winner)
        self.assertEqual(engine.scores['Draw'], 1)

    def test_occupied_cell_move_rejected(self):
        # Task 3: Clicking on occupied cell should be ignored
        engine = GameEngine()
        # Pretend cell (0, 0) is already 'O'
        engine.board[0][0] = 'O'
        engine.current_player = 'X'

        # Click on cell (0, 0): center is (20 + 60, 95 + 60) = (80, 155)
        engine.handle_click((80, 155))

        # Cell should still be 'O', and turn should still be 'X'
        self.assertEqual(engine.board[0][0], 'O')
        self.assertEqual(engine.current_player, 'X')

    def test_no_moves_accepted_after_round_over(self):
        # Task 1: Clicking empty cells after round ended should do nothing
        engine = GameEngine()
        engine.round_over = True
        engine.winner = 'X'
        engine.board[1][1] = None

        # Click cell (1, 1): center is (20 + 120 + 60, 95 + 120 + 60) = (200, 275)
        engine.handle_click((200, 275))
        self.assertIsNone(engine.board[1][1])

    def test_persistent_scoreboard(self):
        # Task 2: Scoreboard persists across new_round, resets only on reset_match
        engine = GameEngine()
        engine.scores = {'X': 3, 'O': 2, 'Draw': 1}

        # Start new round
        engine.new_round()
        self.assertEqual(engine.scores, {'X': 3, 'O': 2, 'Draw': 1})
        self.assertFalse(engine.round_over)

        # Full match reset
        engine.reset_match()
        self.assertEqual(engine.scores, {'X': 0, 'O': 0, 'Draw': 0})

    def test_starting_player_choice_and_computer_first_move(self):
        # Task 4: When O is set as starter, computer makes the first move on new round
        engine = GameEngine()
        engine.set_starter('O')
        self.assertEqual(engine.starting_player, 'O')

        # Check that computer has placed one symbol
        occupied = sum(1 for r in range(3) for c in range(3) if engine.board[r][c] is not None)
        self.assertEqual(occupied, 1)
        self.assertEqual(engine.current_player, 'X', "Turn should be handed over to X after O moves")


if __name__ == '__main__':
    unittest.main()
