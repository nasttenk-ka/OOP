import re

class Student:
    def __init__(self, student_id: str, name: str, grade: int):
        if not re.match("^[A-Za-z ]+$", name):
            raise ValueError("Name must only contain letters and spaces")
        if not (0 <= grade <= 100):
            raise ValueError("Grade must be between 0 and 100")
        
        self.student_id = student_id
        self.name = name
        self.grade = grade
    
    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Grade: {self.grade}"