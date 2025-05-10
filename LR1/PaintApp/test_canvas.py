import unittest
import os
import tempfile
from canvas import DrawingCanvas
from shapes.rectangle import RectangleShape
from shapes.triangle import TriangleShape
from shapes.circle import CircleShape

class TestDrawingCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = DrawingCanvas(width=20, height=10, background='.')
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, 'test_canvas.json')

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_canvas_initialization(self):
        self.assertEqual(len(self.canvas.canvas), 10)
        self.assertEqual(len(self.canvas.canvas[0]), 20)

    def test_add_shape(self):
        rect = RectangleShape(1, 1, 3, 2, border_char='*')
        self.canvas.add_shape(rect)
        self.assertIn(rect.shape_id, self.canvas.shapes)

    def test_move_shape(self):
        rect = RectangleShape(1, 1, 3, 2, border_char='*')
        self.canvas.add_shape(rect)
        self.canvas.move_shape(rect.shape_id, 2, 1)
        self.assertEqual(rect.x, 3)
        self.assertEqual(rect.y, 2)

    def test_save_and_load(self):
        rect = RectangleShape(1, 1, 3, 2, border_char='*')
        self.canvas.add_shape(rect)
        self.canvas.save_to_file(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

class TestRectangleShape(unittest.TestCase):
    def setUp(self):
        self.rect = RectangleShape(1, 1, 3, 2, border_char='*')

    def test_move(self):
        self.rect.move(2, 1)
        self.assertEqual(self.rect.x, 3)
        self.assertEqual(self.rect.y, 2)

class TestTriangleShape(unittest.TestCase):
    def setUp(self):
        self.tri = TriangleShape(1, 1, 3, 2, 5, border_char='*')

    def test_move(self):
        self.tri.move(2, 1)
        self.assertEqual(self.tri.x1, 3)
        self.assertEqual(self.tri.y1, 2)

class TestCircleShape(unittest.TestCase):
    def setUp(self):
        self.circle = CircleShape(5, 5, 3, border_char='@')

    def test_move(self):
        self.circle.move(2, 1)
        self.assertEqual(self.circle.x, 7)
        self.assertEqual(self.circle.y, 6)

class TestTriangleShape(unittest.TestCase):
    def setUp(self):
        self.tri = TriangleShape(2, 3, 3, 4, 5)

    def test_triangle_initialization(self):
        """Test triangle initialization with valid sides"""
        self.assertEqual(self.tri.x1, 2)
        self.assertEqual(self.tri.y1, 3)
        self.assertEqual(self.tri.a, 3)
        self.assertEqual(self.tri.b, 4)
        self.assertEqual(self.tri.c, 5)


    def test_triangle_move(self):
        """Test moving triangle updates all vertices"""
        self.tri.move(1, -1)
        self.assertEqual(self.tri.x1, 3)
        self.assertEqual(self.tri.y1, 2)
        self.assertEqual(self.tri.x2, 6)  # x1 + a после перемещения (3 + 3)
        self.assertEqual(self.tri.y2, 2)
        
        # Проверяем что все вершины переместились одинаково
        dx = self.tri.x1 - 2
        dy = self.tri.y1 - 3
        self.assertEqual(self.tri.x2, 5 + dx)
        self.assertEqual(self.tri.y2, 3 + dy)

    def test_triangle_border_fill_chars(self):
        """Test border and fill characters are set correctly"""
        tri = TriangleShape(1, 1, 2, 2, 2, border_char='@', fill_char='#')
        self.assertEqual(tri.border_char, '@')
        self.assertEqual(tri.fill_char, '#')

    def test_triangle_get_details(self):
        """Test get_details returns correct string representation"""
        details = self.tri.get_details()
        self.assertIn("Triangle with vertices", details)
        self.assertIn("(2,3)", details)
        self.assertIn(f"({self.tri.x2},{self.tri.y2})", details)
        self.assertIn(f"({self.tri.x3},{self.tri.y3})", details)

    def test_triangle_contains_point(self):
        """Test point containment in triangle"""
        # Центр тяжести треугольника
        center_x = (self.tri.x1 + self.tri.x2 + self.tri.x3) / 3
        center_y = (self.tri.y1 + self.tri.y2 + self.tri.y3) / 3
        self.assertTrue(self.tri.contains_point(center_x, center_y))
        
        # Точка вне треугольника
        self.assertFalse(self.tri.contains_point(0, 0))

if __name__ == '__main__':
    unittest.main()