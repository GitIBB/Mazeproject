from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
            time.sleep(0.01)

    def close(self):
        self.running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color):
        print(f"Drawing line from ({self.p1.x}, {self.p1.y}) to ({self.p2.x}, {self.p2.y}) with color {fill_color}")

        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
            )
            
        

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        # Wall Defaults
        self.north = True
        self.south= True
        self.east = True
        self.west = True
        # Visited
        self.visited = False
        # Coordinates
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        print(f"Cell corners: ({self._x1}, {self._y1}) to ({self._x2}, {self._y2})")

        self._top_left = Point(self._x1, self._y1)
        self._top_right = Point(self._x2, self._y1)
        self._bottom_left = Point(self._x1, self._y2)
        self._bottom_right = Point(self._x2, self._y2)
        print("Points created:")
        print(f"Top left: ({self._top_left.x}, {self._top_left.y})")
        print(f"Top right: ({self._top_right.x}, {self._top_right.y})")
        print(f"Bottom left: ({self._bottom_left.x}, {self._bottom_left.y})")
        print(f"Bottom right: ({self._bottom_right.x}, {self._bottom_right.y})")
    
    # Create Line objects for walls
        self.top_line = Line(self._top_left, self._top_right)
        self.right_line = Line(self._top_right, self._bottom_right)
        self.left_line = Line(self._top_left, self._bottom_left)
        self.bottom_line = Line(self._bottom_left, self._bottom_right)
        print(f"Top line created: ({self.top_line.p1.x}, {self.top_line.p1.y}) to ({self.top_line.p2.x}, {self.top_line.p2.y})")
        print("\nLines created:")
        print(f"Top line: ({self.top_line.p1.x}, {self.top_line.p1.y}) to ({self.top_line.p2.x}, {self.top_line.p2.y})")
        print(f"Left line: ({self.left_line.p1.x}, {self.left_line.p1.y}) to ({self.left_line.p2.x}, {self.left_line.p2.y})")

        if self._win is not None:
            self.draw()

    def draw(self):
        if self._win is None:
            return
        if self.north:
            self._win.draw_line(self.top_line, "black")
        else:
            self._win.draw_line(self.top_line, "white")

        if self.west:
            self._win.draw_line(self.left_line, "black")
        else:
            self._win.draw_line(self.left_line, "white")
        
        if self.east:
            self._win.draw_line(self.right_line, "black")
        else:
            self._win.draw_line(self.right_line, "white")
        
        if self.south:
            self._win.draw_line(self.bottom_line, "black")
        else:
            self._win.draw_line(self.bottom_line, "white")

    def draw_move(self, to_cell, undo=False):
        if undo == False:
            line_color = "red"
        else:
            line_color = "gray"
            
        self_center_x = (self._x1 + self._x2) / 2
        self_center_y = (self._y1 + self._y2) / 2
        to_cell_center_x = (to_cell._x1 + to_cell._x2) / 2
        to_cell_center_y = (to_cell._y1 + to_cell._y2) / 2

    # Create points for the line
        start_point = Point(self_center_x, self_center_y)
        end_point = Point(to_cell_center_x, to_cell_center_y)
        move_line = Line(start_point, end_point)

        self._win.draw_line(move_line, line_color)

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                # Calculate Position
                x1 = self.x1 + (i * self.cell_size_x)
                y1 = self.y1 + (j * self.cell_size_y)
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                # Create a new cell and set its position attributes
                new_cell = Cell(x1, y1, x2, y2, self._win)

                col.append(new_cell)
            self._cells.append(col)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):

        cell = self._cells[i][j]
        
        if self._win is not None:
            cell.draw()

        self._animate()

        return cell

    def _animate(self):
        if self._win is not None:
            self._win.redraw()
        time.sleep(0.05)

    def draw(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cell = self._cells[i][j]
                if self._win is not None:
                    cell.draw()
        if self._win is not None:
            self._win.redraw()

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.north = False
        self._draw_cell(0, 0)
        time.sleep(0.1)

        last_idx = len(self._cells) - 1
        self.exit_cell = self._cells[last_idx][last_idx]
        self.exit_cell.south = False
        self._draw_cell(last_idx, last_idx)
        time.sleep(0.1)

    def _break_walls_r(self, i, j):
        print(f"Breaking walls at cell: ({i}, {j})")
        # Mark current cell as visited
        self._cells[i][j].visited = True
        # In an infinite loop:
        while True:
        # Create a new empty list to hold the i and j values
            next_index_list = []
            # Iterate through each possible direction
            # west
            if i > 0 and not self._cells[i-1][j].visited:
                next_index_list.append((i - 1, j))
            # east
            if i < self.num_cols - 1 and not self._cells[i+1][j].visited:
                next_index_list.append((i + 1, j))
            # north
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # south
            if  j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
                
            # Return statement to break loop
            if len(next_index_list) == 0:
                print(f"No unvisited neighbors for ({i}, {j})")
                return
            
            r_direction_index = random.randrange(0, len(next_index_list))
            next_index = next_index_list[r_direction_index]

            # Break East
            if next_index[0] == i + 1:
                self._cells[i][j].east = False
                self._cells[i + 1][j].west = False
            # Break West
            if next_index[0] == i - 1:
                self._cells[i][j].west = False
                self._cells[i - 1][j].east = False
            # Break South
            if next_index[1] == j + 1:
                self._cells[i][j].south = False
                self._cells[i][j + 1].north = False
            # Break North
            if next_index[1] == j - 1:
                self._cells[i][j].north = False
                self._cells[i][j - 1].south = False

            # Recurse to next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
       return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self.exit_cell:
            return True
        next_index_list = []
        # Move west
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i][j].west and not self._cells[i-1][j].east:
            next_index_list.append((i - 1, j))
        # Move east
        if i < self.num_cols - 1 and not self._cells[i+1][j].visited and not self._cells[i][j].east and not self._cells[i+1][j].west:
            next_index_list.append((i + 1, j))
        # Move north
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].north and not self._cells[i][j-1].south:
            next_index_list.append((i, j - 1))
        # Move south
        if j < self.num_rows - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].south and not self._cells[i][j+1].north:
            next_index_list.append((i, j + 1))


        for new_i, new_j in next_index_list:
            # Access cell object for current and next cell
            current_cell = self._cells[i][j]
            next_cell = self._cells[new_i][new_j]
            # Draw a move between current i/j and new i/j
            current_cell.draw_move(next_cell)
            if self._solve_r(new_i, new_j):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True)

        return False
                
        

    

