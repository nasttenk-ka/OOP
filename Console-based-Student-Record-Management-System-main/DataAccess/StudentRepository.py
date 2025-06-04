from Domain.Student import Student
import json
import os

FILE_NAME = "students.json"

def load_students():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as f:
        return json.load(f)

def save_students(data):
    with open(FILE_NAME, 'w') as f:
        json.dump(data, f, indent=4)

def add_student_to_file(student: Student):
    data = load_students()
    data.append(student.__dict__)
    save_students(data)

def update_student_in_file(student_id: str, name: str, grade: int):
    data = load_students()
    for student in data:
        if student['student_id'] == student_id:
            student['name'] = name
            student['grade'] = grade
    save_students(data)

def get_all_students():
    return [Student(s['student_id'], s['name'], s['grade']) for s in load_students()]