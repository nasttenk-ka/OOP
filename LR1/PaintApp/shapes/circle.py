import math
from shapes.shape import BaseShape

class CircleShape(BaseShape):
    def __init__(self, x, y, radius, border_char='@', fill_char=None):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.border_char = border_char
        self.fill_char = fill_char

    def get_details(self):
        return f"Circle at ({self.x},{self.y}) radius {self.radius}"
    
    def fill(self, canvas, fill_char):
     self.fill_char = fill_char
     self.draw(canvas)
 
    def contains_point(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.radius

    def draw(self, canvas):
        for i in range(max(0, self.y - self.radius), min(canvas.height, self.y + self.radius + 1)):
            for j in range(max(0, self.x - self.radius), min(canvas.width, self.x + self.radius + 1)):
                distance = math.sqrt((j - self.x)**2 + (i - self.y)**2)
                if distance <= self.radius:
                    if canvas.handle_intersections(j, i) == self:
                        if abs(distance - self.radius) < 1 or not self.fill_char:
                            canvas.canvas[i][j] = self.border_char
                        elif self.fill_char:
                            canvas.canvas[i][j] = self.fill_char

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def fill(self, canvas, fill_char):
        self.fill_char = fill_char
        self.draw(canvas)