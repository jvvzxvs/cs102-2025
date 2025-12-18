import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    r, _ = pos
    return list(grid[r])


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    _, c = pos
    return [row[c] for row in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    n = len(grid)
    if n == 0:
        return []
    block = int(n**0.5)
    r, c = pos
    r0 = (r // block) * block
    c0 = (c // block) * block
    out: tp.List[str] = []
    for rr in range(r0, r0 + block):
        for cc in range(c0, c0 + block):
            out.append(grid[rr][cc])
    return out


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v == ".":
                return (r, c)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    n = len(grid)
    if n == 0:
        return set()

    r, c = pos
    if grid[r][c] != ".":
        return set()

    allowed = {str(i) for i in range(1, n + 1)}

    used = set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos))
    used.discard(".")
    return allowed - used


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    board = [row[:] for row in grid]
    n = len(board)
    if n == 0:
        return board

    def pick_mrv_position() -> tp.Tuple[tp.Optional[tp.Tuple[int, int]], tp.Optional[tp.Set[str]]]:
        best_pos: tp.Optional[tp.Tuple[int, int]] = None
        best_vals: tp.Optional[tp.Set[str]] = None
        for rr in range(n):
            for cc in range(n):
                if board[rr][cc] == ".":
                    vals = find_possible_values(board, (rr, cc))
                    if not vals:
                        return (rr, cc), set()
                    if best_vals is None or len(vals) < len(best_vals):
                        best_pos, best_vals = (rr, cc), vals
                        if len(best_vals) == 1:
                            return best_pos, best_vals
        return best_pos, best_vals

    def backtrack() -> bool:
        pos, vals = pick_mrv_position()
        if pos is None:
            return True  # нет пустых клеток
        if vals is None or len(vals) == 0:
            return False

        r, c = pos
        for v in sorted(vals):
            board[r][c] = v
            if backtrack():
                return True
            board[r][c] = "."
        return False

    return board if backtrack() else None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles
    if solution is None:
        return False
    n = len(solution)
    if n == 0:
        return True
    if any(len(row) != n for row in solution):
        return False

    required = {str(i) for i in range(1, n + 1)}
    block = int(n**0.5)
    if block * block != n:
        return False
    # строки
    for r in range(n):
        row = solution[r]
        if "." in row:
            return False
        if set(row) != required:
            return False

    # столбцы
    for c in range(n):
        col = [solution[r][c] for r in range(n)]
        if "." in col:
            return False
        if set(col) != required:
            return False

    # блоки
    for r0 in range(0, n, block):
        for c0 in range(0, n, block):
            blk: tp.List[str] = []
            for rr in range(r0, r0 + block):
                for cc in range(c0, c0 + block):
                    blk.append(solution[rr][cc])
            if "." in blk:
                return False
            if set(blk) != required:
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    import random

    N = max(0, N)
    size = 9
    block = 3
    filled = min(N, size * size)

    # базовое корректное решение
    def pattern(r: int, c: int) -> int:
        return (block * (r % block) + r // block + c) % size

    rows = [g * block + r for g in random.sample(range(block), block) for r in random.sample(range(block), block)]
    cols = [g * block + c for g in random.sample(range(block), block) for c in random.sample(range(block), block)]
    nums = random.sample(range(1, size + 1), size)

    solved = [[str(nums[pattern(r, c)]) for c in cols] for r in rows]

    # выкидываем клетки до нужного числа заполненных
    positions = [(r, c) for r in range(size) for c in range(size)]
    random.shuffle(positions)
    to_blank = size * size - filled
    for i in range(to_blank):
        r, c = positions[i]
        solved[r][c] = "."

    return solved


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
