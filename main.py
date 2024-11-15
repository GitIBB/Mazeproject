from src.classes import Window, Point, Line, Cell, Maze
from tkinter import Tk, Canvas

if __name__ == "__main__":
    win = Window(800, 600)

    # Initialize the Maze
    maze = Maze(x1=50, y1=50, num_rows=12, num_cols=12, cell_size_x=40, cell_size_y=40, win=win)
    maze.draw()
    maze.solve()
    # Test Maze creation or any specific functionality

    win.wait_for_close()