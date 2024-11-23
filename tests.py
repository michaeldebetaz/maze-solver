import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 10
        num_cols = 12
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(len(maze._cells), num_cols)
        self.assertEqual(len(maze._cells[0]), num_rows)

        self.assertEqual(maze._cells[0][0]._x1, 0)
        self.assertEqual(maze._cells[0][1]._y1, 10)

        self.assertEqual(maze._cells[-1][-1]._x2, 120)
        self.assertEqual(maze._cells[-1][-1]._y2, 100)

    def test_maze_add_break_entrance_and_exit(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        maze.break_entrance_and_exit()
        self.assertEqual(maze._cells[0][0].has_left_wall, False)
        self.assertEqual(maze._cells[-1][-1].has_right_wall, False)

    def test_maze_break_walls(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        maze.break_entrance_and_exit()
        maze.break_walls()

        for cell in maze._cells:
            for c in cell:
                self.assertEqual(c.visited, False)

    def test_is_valid_move(self):
        maze = Maze(0, 0, 3, 3, 10, 10)
        i, j = from_pos = [0, 0]
        from_cell = maze._cells[i][j]
        from_cell.has_bottom_wall = False
        from_cell.visited = True

        self.assertEqual(maze._is_valid_move(from_pos, [1, 1]), False)

        to_i, to_j = to_pos = [0, 1]
        to_cell = maze._cells[to_i][to_j]
        to_cell.has_top_wall = False
        self.assertEqual(maze._is_valid_move(from_pos, to_pos), True)
        self.assertEqual(maze._is_valid_move(from_pos, [1, 0]), False)

        to_cell.visited = True
        self.assertEqual(maze._is_valid_move(from_pos, to_pos), False)

        from_cell.has_right_wall = False
        to_i, to_j = to_pos = [1, 0]
        to_cell = maze._cells[to_i][to_j]
        to_cell.has_left_wall = False
        self.assertEqual(maze._is_valid_move(from_pos, to_pos), True)


if __name__ == "__main__":
    unittest.main()
