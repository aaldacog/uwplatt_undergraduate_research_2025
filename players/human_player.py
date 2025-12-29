from .base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def get_move(self, game):
        valid_moves = game.get_valid_moves()
        print(f"Player {self.player_id}'s turn. Valid moves: {valid_moves}")

        while True:
            try:
                if game.__class__.__name__ == "TicTacToe":
                    move_input = input("Enter your move as 'row,col': ")
                    row, col = map(int, move_input.split(','))
                    move = (row, col)
                else:  # ConnectFour
                    move = int(input("Enter column number: "))

                if move in valid_moves:
                    return move
                else:
                    print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Invalid input format. Try again.")