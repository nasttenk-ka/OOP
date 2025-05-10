import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shapes.shape import BaseShape

class RectangleShape(BaseShape):
    def __init__(self, x, y, width, height, border_char='#', fill_char=None):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_char = border_char
        self.fill_char = fill_char

    def get_details(self):
        return f"Rectangle at ({self.x},{self.y}) size {self.width}x{self.height}"

    def contains_point(self, x, y):
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)

    def draw(self, canvas):
        for i in range(max(0, self.y), min(canvas.height, self.y + self.height + 1)):
            for j in range(max(0, self.x), min(canvas.width, self.x + self.width + 1)):
                if canvas.handle_intersections(j, i) == self:
                    if (i == self.y or i == self.y + self.height or 
                        j == self.x or j == self.x + self.width):
                        canvas.canvas[i][j] = self.border_char
                    elif self.fill_char:
                        canvas.canvas[i][j] = self.fill_char

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def fill(self, canvas, fill_char):
        self.fill_char = fill_char
        self.draw(canvas)