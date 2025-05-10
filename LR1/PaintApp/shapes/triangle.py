import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shapes.shape import BaseShape
import math

class TriangleShape(BaseShape):
    def __init__(self, x1, y1, a, b, c, border_char='*', fill_char=None):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.a = a
        self.b = b
        self.c = c
        self.border_char = border_char
        self.fill_char = fill_char
        self._calculate_vertices()

    def _calculate_vertices(self):
        self.x2 = self.x1 + self.a
        self.y2 = self.y1
        
        cos_alpha = (self.b**2 + self.c**2 - self.a**2) / (2 * self.b * self.c)
        alpha = math.acos(max(-1, min(1, cos_alpha)))
        self.x3 = self.x1 + int(self.b * math.cos(alpha))
        self.y3 = self.y1 - int(self.b * math.sin(alpha))

    def get_details(self):
        return f"Triangle with vertices ({self.x1},{self.y1}), ({self.x2},{self.y2}), ({self.x3},{self.y3})"

    def contains_point(self, x, y):
        def sign(a, b, c):
            return (a[0] - c[0])*(b[1] - c[1]) - (b[0] - c[0])*(a[1] - c[1])

        d1 = sign((x,y), (self.x1,self.y1), (self.x2,self.y2))
        d2 = sign((x,y), (self.x2,self.y2), (self.x3,self.y3))
        d3 = sign((x,y), (self.x3,self.y3), (self.x1,self.y1))

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    def _draw_line(self, canvas, x1, y1, x2, y2):
        dx, dy = abs(x2-x1), abs(y2-y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            if 0 <= x1 < canvas.width and 0 <= y1 < canvas.height:
                if canvas.handle_intersections(x1, y1) == self:
                    canvas.canvas[y1][x1] = self.border_char
            if x1 == x2 and y1 == y2:
                break
            e2 = 2*err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw(self, canvas):
        self._draw_line(canvas, self.x1, self.y1, self.x2, self.y2)
        self._draw_line(canvas, self.x2, self.y2, self.x3, self.y3)
        self._draw_line(canvas, self.x3, self.y3, self.x1, self.y1)
        
        if self.fill_char:
            self._fill_triangle(canvas)

    def _fill_triangle(self, canvas):
        min_y = min(self.y1, self.y2, self.y3)
        max_y = max(self.y1, self.y2, self.y3)
        
        for y in range(max(0, min_y), min(canvas.height, max_y + 1)):
            intersections = []
            for (x1, y1, x2, y2) in [
                (self.x1, self.y1, self.x2, self.y2),
                (self.x2, self.y2, self.x3, self.y3),
                (self.x3, self.y3, self.x1, self.y1)
            ]:
                if min(y1, y2) <= y <= max(y1, y2) and y1 != y2:
                    x = int(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
                    intersections.append(x)
            
            if len(intersections) >= 2:
                x_start, x_end = min(intersections), max(intersections)
                for x in range(max(0, x_start), min(canvas.width, x_end + 1)):
                    if canvas.handle_intersections(x, y) == self:
                        canvas.canvas[y][x] = self.fill_char

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.x3 += dx
        self.y3 += dy

    def fill(self, canvas, fill_char):
        self.fill_char = fill_char
        self.draw(canvas)