import random
import time

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

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]

        if self._win is not None:
            self._win.draw_cell(cell, "black")
            self._animate()

    def _animate(self):
        if self._win is not None:
            self._win.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        top_left_cell.has_left_wall = False

        bottom_right_cell = self._cells[-1][-1]
        bottom_right_cell.has_right_wall = False

        if self._win is not None:
            self._win.draw_cell(top_left_cell, "black")
            self._win.draw_cell(bottom_right_cell, "black")

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True

        while True:
            adjacents: list[list[int]] = []
            if i > 0:
                adjacents.append([i - 1, j])
            if i < self._num_cols - 1:
                adjacents.append([i + 1, j])
            if j > 0:
                adjacents.append([i, j - 1])
            if j < self._num_rows - 1:
                adjacents.append([i, j + 1])

            to_visit: list[list[int]] = []
            for adj_i, adj_j in adjacents:
                adj_cell = self._cells[adj_i][adj_j]
                if not adj_cell.visited:
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
                self._win.draw_cell(cell, "black")
                self._win.draw_cell(next_cell, "black")

            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
