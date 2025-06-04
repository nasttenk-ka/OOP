import unittest
from Domain.Student import Student

class TestStudentValidation(unittest.TestCase):
    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Student("1", "Alice123", 85)

    def test_invalid_grade_low(self):
        with self.assertRaises(ValueError):
            Student("2", "Alice", -5)

    def test_invalid_grade_high(self):
        with self.assertRaises(ValueError):
            Student("3", "Alice", 105)
