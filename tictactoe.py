import logging
from typing import List, Optional

from colorama import Fore, Style, init

init(autoreset=True)

# Configure logging
logging.basicConfig(
    filename="tictactoe.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

BOARD_TEMPLATE = """
{a} | {b} | {c}
--+---+--
{d} | {e} | {f}
--+---+--
{g} | {h} | {i}
"""

class TicTacToe:
    def __init__(self):
        self.board: List[str] = [str(i) for i in range(1, 10)]
        self.current_player: str = "X"
        logging.debug("Game initialized. Board reset.")

    def display_board(self) -> None:
        colored_board = [self._color_cell(cell) for cell in self.board]
        board_str = BOARD_TEMPLATE.format(
            a=colored_board[0], b=colored_board[1], c=colored_board[2],
            d=colored_board[3], e=colored_board[4], f=colored_board[5],
            g=colored_board[6], h=colored_board[7], i=colored_board[8],
        )
        print(board_str)

    def _color_cell(self, cell: str) -> str:
        if cell == "X":
            return Fore.RED + cell + Style.RESET_ALL
        elif cell == "O":
            return Fore.BLUE + cell + Style.RESET_ALL
        return cell

    def make_move(self, position: int) -> bool:
        if self.board[position] in ["X", "O"]:
            logging.warning("Invalid move: position %s already taken", position + 1)
            return False
        self.board[position] = self.current_player
        logging.info("Player %s moved to position %s", self.current_player, position + 1)
        return True

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        logging.debug("Switched player. Current player: %s", self.current_player)

    def check_winner(self) -> Optional[str]:
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
            (0, 4, 8), (2, 4, 6),             # diagonals
        ]
        for i, j, k in combos:
            if self.board[i] == self.board[j] == self.board[k]:
                logging.info("Player %s wins! Combination: %s-%s-%s", self.board[i], i+1, j+1, k+1)
                return self.board[i]
        if all(cell in ["X", "O"] for cell in self.board):
            logging.info("Game ends in a draw.")
            return "Draw"
        return None

def play_game():
    game = TicTacToe()
    game.display_board()
    while True:
        try:
            move = int(input(f"Player {game.current_player}, choose a position (1-9): ")) - 1
            if move not in range(9):
                logging.warning("Player %s made an invalid selection: %s", game.current_player, move + 1)
                print("Invalid position. Choose from 1 to 9.")
                continue
        except ValueError:
            logging.warning("Player %s entered a non-integer value.", game.current_player)
            print("Please enter a valid number.")
            continue

        if not game.make_move(move):
            print("That position is already taken. Try again.")
            continue

        game.display_board()
        result = game.check_winner()
        if result:
            if result == "Draw":
                print("It's a draw!")
            else:
                print(f"Player {result} wins!")
            break

        game.switch_player()

if __name__ == "__main__":
    play_game()
