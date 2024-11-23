import random
import time

from colors import Colors
from figures import Cell, Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window | None = None,
        seed: int | None = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = random.seed(seed) if seed is not None else None

        self._cells: list[list[Cell]] = []

        self._create_cells()

    def _create_cells(self):
        self._cells: list[list[Cell]] = []
        for i in range(self._num_cols):
            row: list[Cell] = []
            for j in range(self._num_rows):
                x1 = self._x1 + i * self._cell_size_x
                y1 = self._y1 + j * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                cell = Cell(x1, y1, x2, y2, self._win)
                row.append(cell)
            self._cells.append(row)

        for i, col in enumerate(self._cells):
            for j in range(len(col)):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        cell = self._cells[i][j]

        if self._win is not None:
            self._win.draw_cell(cell, Colors.BLACK)
            self._animate()

    def _animate(self):
        if self._win is not None:
            self._win.redraw()
            time.sleep(0.005)

    def break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        top_left_cell.has_left_wall = False

        bottom_right_cell = self._cells[-1][-1]
        bottom_right_cell.has_right_wall = False

        if self._win is not None:
            self._win.draw_cell(top_left_cell, Colors.BLACK)
            self._win.draw_cell(bottom_right_cell, Colors.BLACK)

    def break_walls(self):
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _break_walls_r(self, i: int, j: int):
        cell = self._cells[i][j]
        cell.visited = True

        while True:
            to_visit: list[list[int]] = []
            for adj_i, adj_j in self._get_adjacent_positions(i, j):
                adjacent_cell = self._cells[adj_i][adj_j]
                if not adjacent_cell.visited:
                    to_visit.append([adj_i, adj_j])

            if len(to_visit) == 0:
                return

            next_i, next_j = random.choice(to_visit)
            next_cell = self._cells[next_i][next_j]

            if cell._x1 == next_cell._x1:
                if cell._y1 < next_cell._y1:
                    cell.has_bottom_wall = False
                    next_cell.has_top_wall = False
                else:
                    cell.has_top_wall = False
                    next_cell.has_bottom_wall = False

            elif cell._y1 == next_cell._y1:
                if cell._x1 < next_cell._x1:
                    cell.has_right_wall = False
                    next_cell.has_left_wall = False
                else:
                    cell.has_left_wall = False
                    next_cell.has_right_wall = False

            if self._win is not None:
                self._win.draw_cell(cell, Colors.BLACK)
                self._win.draw_cell(next_cell, Colors.BLACK)

            self._break_walls_r(next_i, next_j)

    def _get_adjacent_positions(self, i: int, j: int) -> list[list[int]]:
        adjacent_cells: list[list[int]] = []
        if i > 0:
            adjacent_cells.append([i - 1, j])
        if i < self._num_cols - 1:
            adjacent_cells.append([i + 1, j])
        if j > 0:
            adjacent_cells.append([i, j - 1])
        if j < self._num_rows - 1:
            adjacent_cells.append([i, j + 1])

        return adjacent_cells

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int) -> bool:
        self._animate()
        cell = self._cells[i][j]

        cell.visited = True

        end_i = self._num_cols - 1
        end_j = self._num_rows - 1
        if cell == self._cells[end_i][end_j]:
            return True

        for adj_i, adj_j in self._get_adjacent_positions(i, j):
            if self._is_valid_move([i, j], [adj_i, adj_j]):
                next_cell = self._cells[adj_i][adj_j]
                cell.draw_move(next_cell)

                if self._solve_r(adj_i, adj_j):
                    return True

                cell.draw_move(next_cell, undo=True)

        return False

    def _is_valid_move(self, from_position: list[int], to_position: list[int]) -> bool:
        from_i, from_j = from_position
        from_cell = self._cells[from_i][from_j]
        to_i, to_j = to_position
        to_cell = self._cells[to_i][to_j]

        # Check if to_cell has already been visited
        if to_cell.visited:
            return False

        # Check if to_cell is adjacent to from_cell
        if to_position not in self._get_adjacent_positions(from_i, from_j):
            return False

        # Check if there is a wall between to_cell and from_cell
        # Same column
        if from_i == to_i:
            if from_j < to_j:
                # From top to bottom
                if from_cell.has_bottom_wall or to_cell.has_top_wall:
                    return False
            else:
                # From bottom to top
                if from_cell.has_top_wall or to_cell.has_bottom_wall:
                    return False
        # Same row
        if from_j == to_j:
            if from_i < to_i:
                # From top to bottom
                if from_cell.has_right_wall or to_cell.has_left_wall:
                    return False
            else:
                # From bottom to top
                if from_cell.has_left_wall or to_cell.has_right_wall:
                    return False

        return True
