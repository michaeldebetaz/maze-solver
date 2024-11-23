from tkinter import BOTH, Canvas, Tk

from colors import Colors


class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._root = Tk()
        self._root.title("Maze Solver")
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(width=width, height=height)
        self.canvas.pack(fill=BOTH)
        self.running = False

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def draw_line(self, line: "Line", fill_color: Colors):
        line.draw(self.canvas, fill_color)

    def draw_cell(self, cell: "Cell", fill_color: Colors):
        cell.draw(self.canvas, fill_color)

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: Colors):
        p1, p2 = self.p1, self.p2
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=fill_color, width=2)


class Cell:
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        win: Window | None = None,
        has_left_wall: bool = True,
        has_right_wall: bool = True,
        has_top_wall: bool = True,
        has_bottom_wall: bool = True,
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self.visited = False

    def draw(self, canvas: Canvas, fill_color: Colors):
        fill_color_left = fill_color if self.has_left_wall else Colors.BLANK
        canvas.create_line(
            self._x1, self._y1, self._x1, self._y2, fill=fill_color_left, width=2
        )

        fill_color_right = fill_color if self.has_right_wall else Colors.BLANK
        canvas.create_line(
            self._x2, self._y1, self._x2, self._y2, fill=fill_color_right, width=2
        )

        fill_color_top = fill_color if self.has_top_wall else Colors.BLANK
        canvas.create_line(
            self._x1, self._y1, self._x2, self._y1, fill=fill_color_top, width=2
        )

        fill_color_bottom = fill_color if self.has_bottom_wall else Colors.BLANK
        canvas.create_line(
            self._x1, self._y2, self._x2, self._y2, fill=fill_color_bottom, width=2
        )

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        color = Colors.BLANK
        if not undo:
            color = Colors.RED
        x1 = self._x1 + (self._x2 - self._x1) // 2
        y1 = self._y1 + (self._y2 - self._y1) // 2
        x2 = to_cell._x1 + (to_cell._x2 - to_cell._x1) // 2
        y2 = to_cell._y1 + (to_cell._y2 - to_cell._y1) // 2
        line = Line(Point(x1, y1), Point(x2, y2))

        if self._win is not None:
            self._win.draw_line(line, color)
