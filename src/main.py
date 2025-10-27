import pygame
from game_2048 import Game2048
import logging  # type: ignore
import logging.config
import os
from zack_ai_engine_2048 import ZackAIEngine

# Set up logging
def main():
    project_root = os.path.join(os.path.dirname(__file__), "..")
    logging.config.fileConfig(os.path.join(project_root, "logging.conf"))
    LOG = logging.getLogger(__name__)

    pygame.init()
    WINDOW_HEIGHT, WINDOW_WIDTH = 1024, 768

    GRID_SIZE = 4
    TILE_SIZE = 100
    TILE_MARGIN = 10
    GRID_WIDTH = (
        GRID_SIZE * (TILE_SIZE + TILE_MARGIN) - TILE_MARGIN
    )  # Total width of the grid
    GRID_OFFSET_X = (
        WINDOW_HEIGHT - GRID_WIDTH
    ) // 2  # Horizontal offset to centre the grid
    GRID_OFFSET_Y = 100
    FONT_SIZE = 36
    SCORE_HEIGHT = 80

    # Colors
    BACKGROUND_COLOR = (187, 173, 160)
    GRID_COLOR = (205, 193, 180)
    TILE_COLORS = {
        0: (205, 193, 180),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
    }
    TEXT_COLOR = (119, 110, 101)
    TEXT_COLOR_LIGHT = (249, 246, 242)

    screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    pygame.display.set_caption("2048 Game by Zack")
    font = pygame.font.Font(None, FONT_SIZE)


    def draw_tile(i, j, tile_value):
        """
        Draw a single tile at the position (i,j) with the given value
        """

        x = GRID_OFFSET_X + j * (TILE_SIZE + TILE_MARGIN)
        y = GRID_OFFSET_Y + i * (TILE_SIZE + TILE_MARGIN)
        color = TILE_COLORS.get(tile_value, TILE_COLORS[0])

        pygame.draw.rect(
            screen, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=5
        )

        text_color = TEXT_COLOR_LIGHT if tile_value >= 8 else TEXT_COLOR
        text = font.render(str(tile_value), True, text_color)
        text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        screen.blit(text, text_rect)


    def draw_grid(game: Game2048):
        """Draw the entire 4x4 grid and lines, tiles are drawn within a for loop with an offset"""
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(
            screen,
            GRID_COLOR,
            (GRID_OFFSET_X, GRID_OFFSET_Y, GRID_WIDTH, GRID_WIDTH),
            border_radius=5,
        )
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile_value = game.board[i][j]
                draw_tile(i, j, tile_value)


    def draw_game_state(game: Game2048):
        if game.is_end_game():
            # Create a semi-transparent overlay
            overlay = pygame.Surface((GRID_WIDTH, GRID_WIDTH), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (GRID_OFFSET_X, GRID_OFFSET_Y))

            if game.is_end_game() == 1:
                message = "You Won!"
                text_color = (0, 255, 0)  # Green for win
            elif game.is_end_game() == 2:
                message = "Game Over!"
                text_color = (255, 0, 0)  # Red for game over

            game_state_font = pygame.font.Font(None, 60)
            text = game_state_font.render(message, True, text_color)
            text_rect = text.get_rect(
                center=(
                    GRID_OFFSET_X + GRID_WIDTH // 2,
                    GRID_OFFSET_Y + GRID_WIDTH // 2,
                )
            )
            screen.blit(text, text_rect)

            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render(
                "Press R to Restart", True, TEXT_COLOR_LIGHT
            )
            restart_rect = restart_text.get_rect(
                center=(
                    GRID_OFFSET_X + GRID_WIDTH // 2,
                    GRID_OFFSET_Y + GRID_WIDTH // 2 + 50,
                )
            )
            screen.blit(restart_text, restart_rect)


    # Game instance creation
    zack_ai_engine = ZackAIEngine()
    game = Game2048(grid_size=GRID_SIZE, ai_engine=zack_ai_engine)
    game.start_game()
    clock = pygame.time.Clock()

    running = True
    gaming = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game.is_end_game():
                moved = False
                if event.key == pygame.K_LEFT:
                    moved = game.move_left()
                elif event.key == pygame.K_RIGHT:
                    moved = game.move_right()
                elif event.key == pygame.K_UP:
                    moved = game.move_up()
                elif event.key == pygame.K_DOWN:
                    moved = game.move_down()
                elif event.key == pygame.K_SPACE:
                    move = game.recommend_next_move()
                if moved:
                    game.generate_tile()
                    LOG.info("Game state updated after move")
                    if game.is_game_over():
                        LOG.info("Game is over !")
                    elif game.is_game_win():
                        LOG.info(
                            "Congratulations, you have won the game, press R to restart!"
                        )
            elif game.is_end_game() and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.start_game()

        draw_grid(game)
        draw_game_state(game)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()