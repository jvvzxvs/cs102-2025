import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                char = "█" if cell else " "
                screen.addch(i + 1, j + 1, char)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)

        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                key = screen.getch()
                if key == ord("q"):
                    break

                self.life.step()
                curses.napms(100)
        finally:
            curses.endwin()


if __name__ == "__main__":
    c = Console(GameOfLife((24, 80), True, 80))
    c.run()