"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 400, 560
BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_LEFT = (WIDTH - BOARD_SIZE) // 2
BOARD_TOP = 95
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)
COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)
COLOR_TEXT = (30, 30, 30)
COLOR_SUBTEXT = (100, 100, 100)
COLOR_ACCENT = (180, 40, 40)


def board_pos_to_cell(pos):
    x, y = pos
    x -= BOARD_LEFT
    y -= BOARD_TOP
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return int(row), int(col)


def draw_board(surface, board):
    surface.fill(COLOR_BG)
    for i in range(1, 3):
        # Vertical grid lines
        pygame.draw.line(surface, COLOR_LINE,
                         (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP),
                         (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + BOARD_SIZE), 3)
        # Horizontal grid lines
        pygame.draw.line(surface, COLOR_LINE,
                         (BOARD_LEFT, BOARD_TOP + i * CELL_SIZE),
                         (BOARD_LEFT + BOARD_SIZE, BOARD_TOP + i * CELL_SIZE), 3)

    for r in range(3):
        for c in range(3):
            symbol = board[r][c]
            if symbol is None:
                continue
            center = (BOARD_LEFT + c * CELL_SIZE + CELL_SIZE // 2,
                      BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2)
            if symbol == 'X':
                offset = CELL_SIZE // 3
                pygame.draw.line(surface, COLOR_X,
                                 (center[0] - offset, center[1] - offset),
                                 (center[0] + offset, center[1] + offset), 6)
                pygame.draw.line(surface, COLOR_X,
                                 (center[0] + offset, center[1] - offset),
                                 (center[0] - offset, center[1] + offset), 6)
            else:
                pygame.draw.circle(surface, COLOR_O, center, CELL_SIZE // 3, 6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text, color=COLOR_ACCENT):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(surface.get_width() // 2, BOARD_TOP + BOARD_SIZE + 28))
    surface.blit(surf, rect)


def draw_ui(surface, font, engine):
    # Top Status: Current turn or Round Over
    if engine.round_over:
        status_text = "Round Finished"
    elif engine.current_player == 'X':
        status_text = "Your Turn (X)"
    else:
        status_text = "Computer's Turn (O)"

    # Render turn status (top left)
    draw_text(surface, font, status_text, (20, 14), COLOR_TEXT)

    # Render Starter indicator (top right)
    starter_text = f"Starts: {engine.starting_player}"
    starter_surf = font.render(starter_text, True, COLOR_SUBTEXT)
    surface.blit(starter_surf, (WIDTH - 20 - starter_surf.get_width(), 14))

    # Render Scoreboard (centered at y = 52)
    score_text = f"X: {engine.scores['X']}  |  O: {engine.scores['O']}  |  Draws: {engine.scores['Draw']}"
    score_surf = font.render(score_text, True, (40, 40, 80))
    score_rect = score_surf.get_rect(center=(WIDTH // 2, 52))
    surface.blit(score_surf, score_rect)

    # Bottom Area: Result banner and Control cues
    if engine.round_over:
        if engine.winner:
            banner_text = f"{engine.winner} wins!"
            banner_color = COLOR_X if engine.winner == 'X' else COLOR_O
        else:
            banner_text = "It's a Draw!"
            banner_color = (80, 80, 80)
        draw_banner(surface, font, banner_text, banner_color)
    else:
        # Prompt for starter toggle while round is active
        hint_surf = font.render("[T] Toggle Starter (X/O)", True, COLOR_SUBTEXT)
        hint_rect = hint_surf.get_rect(center=(WIDTH // 2, BOARD_TOP + BOARD_SIZE + 25))
        surface.blit(hint_surf, hint_rect)

    # Controls instruction (bottom)
    controls_text = "[R] New Round    [M] Reset Match"
    ctrl_surf = font.render(controls_text, True, COLOR_TEXT)
    ctrl_rect = ctrl_surf.get_rect(center=(WIDTH // 2, BOARD_TOP + BOARD_SIZE + 55))
    surface.blit(ctrl_surf, ctrl_rect)
