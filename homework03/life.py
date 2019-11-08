import pathlib
import random

from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(self, size: Tuple[int, int], randomize: bool = True,
                 max_generations: Optional[float] = float('inf')) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for y in range(self.rows):
                for x in range(self.cols):
                    grid[y][x] = bool(random.randint(0, 1))
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        y0, x0 = cell

        coords = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                x1, y1 = x0 + x, y0 + y
                if (x or y) and 0 <= x1 < self.cols and 0 <= y1 < self.rows:
                    coords.append((y1, x1))

        return [self.curr_generation[y][x] for y, x in coords]

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        next_grid = self.create_grid()
        for y in range(self.rows):
            for x in range(self.cols):
                neighbours_n = self.get_neighbours((y, x)).count(1)
                if not self.curr_generation[y][x] and neighbours_n == 3:
                    next_grid[y][x] = 1
                elif self.curr_generation[y][x] and neighbours_n in [2, 3]:
                    next_grid[y][x] = 1
        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceed and self.is_changing:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.n_generation >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as file:
            grid = [list(map(int, row)) for row in file.readlines()]
        rows, cols = len(grid), len(grid[0])

        game = GameOfLife((rows, cols))
        game.curr_generation = grid

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as file:
            for row in self.curr_generation:
                file.write(''.join(map(str, row)))
