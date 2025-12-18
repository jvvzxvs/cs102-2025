from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    Сносит одну стену рядом с клеткой coord
    Случайно выбирает направление вверх или вправо
    Если в выбранном направлении выход за границы, берет другое направление

    :param grid: Лабиринт (стены "■", проходы " ")
    :param coord: Координаты клетки (x, y), обычно с нечётными координатами
    :return: Тот же grid (меняется на месте)
    """

    x, y = coord
    rows, cols = len(grid), len(grid[0])

    direction = choice(("N", "E"))

    if direction == "N" and (x - 2) < 0:
        direction = "E"
    if direction == "E" and (y + 2) >= cols:
        direction = "N"

    if direction == "N" and (x - 2) < 0:
        return grid
    if direction == "E" and (y + 2) >= cols:
        return grid

    if direction == "N":
        grid[x - 1][y] = " "
    else:
        grid[x][y + 1] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """
    Генерирует лабиринт

    Проходы - клетки с нечетными координатами. Для каждой такой клетки
    сносится одна стена: вверх или вправо

    Две клетки на границе помечаются как вход/выход символом "X"

    :param rows: Количество строк
    :param cols: Количество столбцов
    :param random_exit: True вход/выход случайные, False фиксированные
    :return: Готовая сетка лабиринта

    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        remove_wall(grid, cell)

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    Находит все выходы "X" в лабиринте

    :param grid: Сетка лабиринта
    :return: Список координат (x, y) всех клеток "X"
    """

    exits: List[Tuple[int, int]] = []
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if v == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    Делает один шаг при поиске пути

    Из всех клеток со значением k помечает соседей, которые равны 0, значением k+1

    :param grid: Сетка, где стены "■", а свободные клетки числа
    :param k: Текущий номер шага
    :return: Тот же grid
    """

    rows, cols = len(grid), len(grid[0])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # собираем фронт чтобы не влиять на текущий проход по grid
    frontier: List[Tuple[int, int]] = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                frontier.append((i, j))

    for x, y in frontier:
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                grid[nx][ny] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    Восстанавливает кратчайший путь по размеченной сетке

    В grid уже должны быть числа расстояний

    Идем от exit_coord назад

    :param grid: Сетка с числами расстояний и стенами
    :param exit_coord: Координаты выхода, откуда начинаем восстановление
    :return: Список координат пути от выхода к старту, или None если пути нет
    """
    x, y = exit_coord
    if not isinstance(grid[x][y], int) or grid[x][y] == 0:
        return None

    k = grid[x][y]
    path: List[Tuple[int, int]] = [(x, y)]

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while k > 1:
        found = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == k - 1:
                x, y = nx, ny
                k -= 1
                path.append((x, y))
                found = True
                break
        if not found:
            return None

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    Проверяет, что выход в тупике

    :param grid: Сетка лабиринта
    :param coord: Координаты выхода (x, y)
    :return: True если выход окружен стенами, иначе False
    """

    x, y = coord
    rows, cols = len(grid), len(grid[0])

    if not (x == 0 or x == rows - 1 or y == 0 or y == cols - 1):
        return False

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] != "■":
                return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    Находит кратчайший путь между двумя выходами "X"

    Делает копию grid, превращает проходы в 0, ставит старт = 1,
    запускает волну до второго выхода и потом восстанавливает путь.

    :param grid: Лабиринт (стены "■", проходы " ", два выхода "X")
    :return: исходный grid, путь
    """

    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, None

    start = exits[0]
    end = exits[1]

    if encircled_exit(grid, start) or encircled_exit(grid, end):
        return grid, None

    work = deepcopy(grid)

    # превращаем все проходы в 0
    for i in range(len(work)):
        for j in range(len(work[0])):
            if work[i][j] != "■":
                work[i][j] = 0

    sx, sy = start
    ex, ey = end
    work[sx][sy] = 1

    k = 1
    limit = len(work) * len(work[0]) + 5

    while work[ex][ey] == 0 and k < limit:
        before = deepcopy(work)
        make_step(work, k)
        k += 1
        if work == before:  # волна не продвинулась
            return grid, None

    if work[ex][ey] == 0:
        return grid, None

    path = shortest_path(work, end)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    Рисует путь на лабиринте

    Все клетки из path помечает символом "X"

    :param grid: Сетка лабиринта
    :param path: Путь или None
    :return: Тот же grid с отмеченным путем
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
