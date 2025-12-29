import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [
                [random.randint(0, 1) for _ in range(self.cols)]
                for _ in range(self.rows)
            ]
        return [[0] * self.cols for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        r, c = cell
        neighbours = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbours.append(self.curr_generation[nr][nc])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()
        for r in range(self.rows):
            for c in range(self.cols):
                alive = self.curr_generation[r][c]
                neighbours = sum(self.get_neighbours((r, c)))

                if alive and neighbours in (2, 3):
                    new_grid[r][c] = 1
                elif not alive and neighbours == 3:
                    new_grid[r][c] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        lines = filename.read_text().splitlines()
        rows = len(lines)
        cols = len(lines[0])
        life = GameOfLife((rows, cols), randomize=False)
        life.curr_generation = [[int(ch) for ch in line] for line in lines]
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        text = "\n".join(
            "".join(str(cell) for cell in row)
            for row in self.curr_generation
        )
        filename.write_text(text)
