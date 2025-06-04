import unittest
import os
import json
from DTOs.StudentDTO import StudentDTO
from Application.Command import AddStudentCommand
from DataAccess.StudentRepository import get_all_students, save_students

class AddStudentTest(unittest.TestCase):
    def setUp(self):
        self.file_path = "students.json"
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.original_data = f.read()
        else:
            self.original_data = None
        save_students([])  

    def tearDown(self):
        if self.original_data is not None:
            with open(self.file_path, 'w') as f:
                f.write(self.original_data)
        else:
            os.remove(self.file_path)

    def test_add_student(self):
        dto = StudentDTO("1", "Alice Johnson", 90)
        AddStudentCommand(dto).execute()

        students = get_all_students()

        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].student_id, "1")
        self.assertEqual(students[0].name, "Alice Johnson")
        self.assertEqual(students[0].grade, 90)

