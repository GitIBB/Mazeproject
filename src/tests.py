import unittest
from classes import Maze

class Tests(unittest.TestCase):

    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_even_numbers(self):
        num_cols = 8
        num_rows = 8
        m1 = Maze(0, 0, num_rows, num_cols, 8, 8)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_odd_numbers(self):
        num_cols = 9
        num_rows = 11
        m1 = Maze(0, 0, num_rows, num_cols, 11, 11)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        # Create a small test maze (maybe 3x3)
        num_cols = 3
        num_rows = 3
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
    
        # Break entrance and exit
        maze._break_entrance_and_exit()
    
        # Assert entrance (top-left) has no top wall
        entrance = maze._cells[0][0]
        self.assertEqual(entrance.has_top_wall, False)  # or self.assertFalse(entrance.has_top_wall)

        exit = maze._cells[2][2]
        self.assertEqual(exit.has_bottom_wall, False)
    
if __name__ == "__main__":
    unittest.main()