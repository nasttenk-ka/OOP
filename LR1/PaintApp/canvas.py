import os
import json
from copy import deepcopy

class DrawingCanvas:
    def __init__(self, width=60, height=20, background=' '):
        self.width = width
        self.height = height
        self.background = background
        self.clear_canvas()
        self.action_history = []
        self.shapes = {}
        self.current_z_index = 0

    def clear_canvas(self):
        self.canvas = [[self.background for _ in range(self.width)] for _ in range(self.height)]

    def add_shape(self, shape):
        self.current_z_index += 1
        shape.z_index = self.current_z_index
        self.shapes[shape.shape_id] = shape
        self._redraw()
        self._save_state()

    def _redraw(self):
        self.clear_canvas()
        for shape in sorted(self.shapes.values(), key=lambda x: x.z_index):
            shape.draw(self)

    def _save_state(self):
        state = {
            'canvas': deepcopy(self.canvas),
            'shapes': {k: {'params': v.get_details(), 'z_index': v.z_index} 
                      for k, v in self.shapes.items()}
        }
        self.action_history.append(state)

    def handle_intersections(self, x, y):
        shapes_at_point = []
        for shape in self.shapes.values():
            if shape.contains_point(x, y):
                shapes_at_point.append(shape)
        return max(shapes_at_point, key=lambda s: s.z_index) if shapes_at_point else None

    def save_to_file(self, filename):
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        with open(filepath, 'w') as f:
            json.dump({
                'width': self.width,
                'height': self.height,
                'background': self.background,
                'shapes': {k: v.__dict__ for k, v in self.shapes.items()}
            }, f)

    def load_from_file(self, filename):
        filepath = os.path.join('data', filename)
        if not os.path.exists(filepath):
            print(f"File {filename} not found!")
            return

        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.width = data['width']
        self.height = data['height']
        self.background = data['background']
        self.shapes = {}
        self._redraw()

    def display(self):
        print("+" + "-" * self.width + "+")
        for row in self.canvas:
            print("|" + "".join(row) + "|")
        print("+" + "-" * self.width + "+")

    def move_shape(self, shape_id, dx, dy):
        if shape_id in self.shapes:
            self.shapes[shape_id].move(dx, dy)
            self._redraw()
            self._save_state()

    def fill_shape(self, shape_id, fill_char):
        if shape_id in self.shapes:
            self.shapes[shape_id].fill(self, fill_char)
            self._save_state()

    def delete_shape(self, shape_id):
        if shape_id in self.shapes:
            del self.shapes[shape_id]
            self._redraw()
            self._save_state()

    def undo(self):
        if len(self.action_history) > 1:
            self.action_history.pop()
            prev_state = self.action_history[-1]
            self.canvas = deepcopy(prev_state['canvas'])
            return True
        return False