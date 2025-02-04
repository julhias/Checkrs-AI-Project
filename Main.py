import pygame
from Board import Board
from Game import Game

pygame.init()

class Checkers:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.FPS = pygame.time.Clock()

    def _draw(self, board):
        board.draw(self.screen)
        pygame.display.update()

    def main(self, window_width, window_height):
        board_size = 8
        tile_width, tile_height = window_width // board_size, window_height // board_size
        board = Board(tile_width, tile_height, board_size)
        game = Game()
        current_turn = "red"  # Começa com o jogador "red"

        while self.running:
            game.check_jump(board)

            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.running = False

                if not game.is_game_over(board):
                    if current_turn == "red":
                        if self.event.type == pygame.MOUSEBUTTONDOWN:
                            board.handle_click(self.event.pos)
                            current_turn = "black"  # Após o jogador "red" jogar, passa para o "black"
                    elif current_turn == "black":
                        # Turno do computador (IA)
                        print("Vez do computador...")
                        _, best_move = game.negamax(board, depth=3, alpha=float('-inf'), beta=float('inf'), color=-1)  # "black" tem valor -1
                        if best_move:
                            board.execute_move(best_move)
                        current_turn = "red"  # Depois da IA jogar, volta para o jogador "red"
                else:
                    game.message()
                    self.running = False

            self._draw(board)
            self.FPS.tick(60)


if __name__ == "__main__":
    window_size = (640, 640)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Checkers")

    checkers = Checkers(screen)
    checkers.main(window_size[0], window_size[1])
