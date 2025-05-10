from abc import ABC, abstractmethod

class BaseShape(ABC):
    shape_count = 0

    def __init__(self):
        BaseShape.shape_count += 1
        self.shape_id = BaseShape.shape_count
        self.z_index = 0

    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def contains_point(self, x, y):
        pass

    @abstractmethod
    def move(self, dx, dy):
        pass

    @abstractmethod
    def fill(self, canvas, fill_char):
        pass