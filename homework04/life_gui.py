import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.paused = False

        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for r, row in enumerate(self.life.curr_generation):
            for c, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                rect = pygame.Rect(
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.paused = not self.paused

                if self.paused and event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    c = x // self.cell_size
                    r = y // self.cell_size
                    self.life.curr_generation[r][c] ^= 1

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            if not self.paused:
                if self.life.is_changing and not self.life.is_max_generations_exceeded:
                    self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((24, 80), True, 80)
    gui = GUI(game)
    gui.run()
