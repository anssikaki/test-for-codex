import logging
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
            st.success("It's a draw!")
        else:
            st.success(f"Player {result} wins!")
    else:
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"


def reset_game():
    st.session_state.board = ["" for _ in range(9)]
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    logging.debug("Game reset")


init_game()

st.title("Tic Tac Toe")

status = st.empty()
board = st.session_state.board

for row in range(3):
    cols = st.columns(3)
    for col_idx in range(3):
        idx = row * 3 + col_idx
        label = board[idx] if board[idx] else " "
        if cols[col_idx].button(label, key=f"cell{idx}"):
            handle_move(idx)

if st.session_state.game_over:
    pass
else:
    status.write(f"Player {st.session_state.current_player}'s turn")

st.button("Reset Game", on_click=reset_game)
