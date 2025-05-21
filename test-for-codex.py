import logging
import random
from typing import List, Optional

import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

# Configure logging
logging.basicConfig(
    filename="tictactoe.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def init_game():
    if "board" not in st.session_state:
        st.session_state.board = ["" for _ in range(9)]
    if "current_player" not in st.session_state:
        st.session_state.current_player = "X"
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}
    if "mode" not in st.session_state:
        st.session_state.mode = "Single Player"
    if "winning_combo" not in st.session_state:
        st.session_state.winning_combo = None
    logging.debug("Game initialized")


def check_winner() -> Optional[str]:
    board = st.session_state.board
    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for i, j, k in combos:
        if board[i] and board[i] == board[j] == board[k]:
            logging.info("Player %s wins with combo %s-%s-%s", board[i], i+1, j+1, k+1)
            st.session_state.winning_combo = (i, j, k)
            return board[i]
    if all(cell for cell in board):
        logging.info("Game ends in a draw")
        return "Draw"
    return None


def handle_move(pos: int):
    if st.session_state.board[pos] or st.session_state.game_over:
        return
    st.session_state.board[pos] = st.session_state.current_player
    logging.info("Player %s moved to position %s", st.session_state.current_player, pos+1)
    result = check_winner()
    if result:
        st.session_state.game_over = True
        if result == "Draw":
            st.session_state.scores["Draw"] += 1
            st.success("It's a draw!")
        else:
            st.session_state.scores[result] += 1
            st.success(f"Player {result} wins!")
    else:
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

        if st.session_state.mode == "Single Player" and st.session_state.current_player == "O":
            ai_move()


def ai_move():
    """Make a move for the computer player using a simple strategy."""
    board = st.session_state.board
    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    def find_move(player: str) -> Optional[int]:
        for i, j, k in combos:
            line = [board[i], board[j], board[k]]
            if line.count(player) == 2 and line.count("") == 1:
                return [i, j, k][line.index("")]
        return None

    # win if possible
    move = find_move("O")
    if move is None:
        # block opponent
        move = find_move("X")
    if move is None and board[4] == "":
        move = 4
    if move is None:
        corners = [i for i in [0, 2, 6, 8] if board[i] == ""]
        move = random.choice(corners) if corners else None
    if move is None:
        empty = [i for i, cell in enumerate(board) if cell == ""]
        move = random.choice(empty)

    handle_move(move)

def reset_game():
    st.session_state.board = ["" for _ in range(9)]
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winning_combo = None
    logging.debug("Game reset")


init_game()

st.title("Tic Tac Toe")

st.sidebar.header("Settings")
mode = st.sidebar.radio(
    "Mode",
    options=["Single Player", "Two Player"],
    index=0 if st.session_state.mode == "Single Player" else 1,
)
if mode != st.session_state.mode:
    st.session_state.mode = mode
    reset_game()

st.sidebar.subheader("Scoreboard")
st.sidebar.write(f"X: {st.session_state.scores['X']}")
st.sidebar.write(f"O: {st.session_state.scores['O']}")
st.sidebar.write(f"Draws: {st.session_state.scores['Draw']}")

status = st.empty()
board = st.session_state.board

for row in range(3):
    cols = st.columns(3)
    for col_idx in range(3):
        idx = row * 3 + col_idx
        label = board[idx] if board[idx] else " "
        if st.session_state.game_over:
            highlight = (
                st.session_state.winning_combo
                and idx in st.session_state.winning_combo
            )
            style = (
                "background-color:#fffb91;font-size:40px;text-align:center;" "height:60px;line-height:60px;"
                if highlight
                else "font-size:40px;text-align:center;height:60px;line-height:60px;"
            )
            cols[col_idx].markdown(
                f"<div style='{style}'>{label}</div>", unsafe_allow_html=True
            )
        else:
            if cols[col_idx].button(label, key=f"cell{idx}", use_container_width=True):
                handle_move(idx)

if st.session_state.game_over:
    pass
else:
    status.write(f"Player {st.session_state.current_player}'s turn")

st.button("Reset Game", on_click=reset_game)
