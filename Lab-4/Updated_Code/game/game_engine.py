"""
GameEngine: owns the board, turn state, round-end logic, scoreboard,
and match management.
"""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move

HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        # Match-level state (persists across rounds)
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        self.starting_player = 'X'

        # Round-level state
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.starting_player
        self.round_over = False
        self.winner = None

    def new_round(self):
        """Starts a new round, preserving the scoreboard."""
        self.board = [[None] * 3 for _ in range(3)]
        self.round_over = False
        self.winner = None
        self.current_player = self.starting_player
        self._maybe_take_computer_turn()

    def reset_match(self):
        """Resets the entire match, clearing the scoreboard."""
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        self.new_round()

    def toggle_starter(self):
        """Toggles who starts the round (X or O)."""
        self.starting_player = 'O' if self.starting_player == 'X' else 'X'
        # If no moves have been made yet in this round, apply immediately
        if self._is_board_empty() and not self.round_over:
            self.current_player = self.starting_player
            self._maybe_take_computer_turn()

    def set_starter(self, symbol):
        """Explicitly sets who starts the round ('X' or 'O')."""
        if symbol in ('X', 'O'):
            self.starting_player = symbol
            if self._is_board_empty() and not self.round_over:
                self.current_player = self.starting_player
                self._maybe_take_computer_turn()

    def _is_board_empty(self):
        return all(cell is None for row in self.board for cell in row)

    def handle_click(self, pos):
        # Task 1 Fix: ignore clicks once the round is over
        if self.round_over:
            return

        # Only allow human player to move on their turn
        if self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)
        if cell is None:
            return

        row, col = cell
        # Task 3 Fix: validate move - reject already occupied cell
        if self.board[row][col] is not None:
            return

        # Place player's symbol
        self.board[row][col] = self.current_player
        self.check_round_end()

        # If round continues, switch turn to computer
        if not self.round_over:
            self.current_player = COMPUTER_SYMBOL
            self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)
        if move is None:
            return

        row, col = move
        self.board[row][col] = self.current_player
        self.check_round_end()

        if not self.round_over:
            self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        import pygame
        if key == pygame.K_r:
            self.new_round()
        elif key == pygame.K_m:
            self.reset_match()
        elif key == pygame.K_t:
            self.toggle_starter()
        elif key == pygame.K_x:
            self.set_starter('X')
        elif key == pygame.K_o:
            self.set_starter('O')

    def check_round_end(self):
        if self.round_over:
            return

        # Task 1 Fix: Check winner BEFORE checking board full
        # This prevents a winning move on the 9th cell from being called a Draw
        winner = check_winner(self.board)
        if winner:
            self.round_over = True
            self.winner = winner
            self._record_score(winner)
            return

        if is_board_full(self.board):
            self.round_over = True
            self.winner = None
            self._record_score(None)

    def _record_score(self, winner):
        # Task 2: Update persistent scoreboard
        if winner == 'X':
            self.scores['X'] += 1
        elif winner == 'O':
            self.scores['O'] += 1
        else:
            self.scores['Draw'] += 1

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_board(surface, self.board)
        renderer.draw_ui(surface, font, self)
