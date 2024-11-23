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

    def test_maze_add_break_entrance_and_exit(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        maze._break_entrance_and_exit()
        self.assertEqual(maze._cells[0][0].has_left_wall, False)
        self.assertEqual(maze._cells[-1][-1].has_right_wall, False)

    def test_maze_reset_visited(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        maze._break_entrance_and_exit()
        maze._break_walls_r(0, 0)
        maze._reset_cells_visited()
        for cell in maze._cells:
            for c in cell:
                self.assertEqual(c.visited, False)


if __name__ == "__main__":
    unittest.main()
