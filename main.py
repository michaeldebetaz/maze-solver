from figures import Window
from maze import Maze


def main():
    win = Window(800, 600)
    num_rows, num_cols = 4, 6
    cell_size_x, cell_size_y = 20, 20
    maze = Maze(100, 100, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=0)
    maze.break_entrance_and_exit()
    maze.break_walls()
    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
