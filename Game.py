class Game:
    def __init__(self):
        self.winner = None

    # Função de avaliação simples
    def evaluate(self, board):
        red_piece, black_piece = self.check_piece(board)
        return red_piece - black_piece

    # Algoritmo Negamax
    def negamax(self, board, depth, alpha, beta, color):
        if depth == 0 or self.is_game_over(board):
            return color * self.evaluate(board), None

        max_eval = float('-inf')
        best_move = None

        # Gerar todos os movimentos válidos para o jogador atual
        moves = self.generate_all_moves(board, color)

        for move in moves:
            # Fazer o movimento
            board_copy = self.simulate_move(board, move)
            eval_score, _ = self.negamax(board_copy, depth - 1, -beta, -alpha, -color)
            eval_score = -eval_score

            # Desfazer o movimento (simulado no tabuleiro copiado)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break

        return max_eval, best_move

    def generate_all_moves(self, board, color):
        moves = []
        for tile in board.tile_list:
            if tile.occupying_piece and tile.occupying_piece.color == ("red" if color == 1 else "black"):
                moves.extend(tile.occupying_piece.valid_moves())
                for jump in tile.occupying_piece.valid_jumps():
                    moves.append(jump[0])  # Adiciona apenas a posição final dos saltos
        return moves

    def simulate_move(self, board, move):
        import copy
        board_copy = copy.deepcopy(board)
        piece = board_copy.get_tile_from_pos(move[0].pos).occupying_piece
        piece._move(move)  # Simula o movimento
        return board_copy

    # Verificar vencedores
    def check_piece(self, board):
        red_piece = 0
        black_piece = 0
        for y in range(board.board_size):
            for x in range(board.board_size):
                tile = board.get_tile_from_pos((x, y))
                if tile.occupying_piece is not None:
                    if tile.occupying_piece.color == "red":
                        red_piece += 1
                    else:
                        black_piece += 1
        return red_piece, black_piece

    def is_game_over(self, board):
        red_piece, black_piece = self.check_piece(board)
        if red_piece == 0 or black_piece == 0:
            self.winner = "red" if red_piece > black_piece else "black"
            return True
        else:
            return False

    def message(self):
        print(f"{self.winner} Wins!!")
