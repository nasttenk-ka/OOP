from DTOs.StudentDTO import StudentDTO
from Application.Command import AddStudentCommand, EditStudentCommand, ViewStudentsCommand
import re
from DataAccess.StudentRepository import load_students


def validate_name(name):
    return re.match("^[A-Za-z ]+$", name)

def validate_grade(grade):
    return grade.isdigit() and 0 <= int(grade) <= 100

def main():
    while True:
        print("\n-----------------------------------------------STUDENT MANAGEMENT SYSTEM-----------------------------------------------")
        print("1. Add Student")
        print("2. Edit Student")
        print("3. View Students")
        print("4. Exit")

        choice = input("\033[33mChoose option: \033[0m")

        if choice == '1':
            name = input("Enter Name: ")
            while not validate_name(name):
                name = input("\033[31mInvalid. Enter Name: \033[0m")
            grade = input("Enter Grade: ")
            while not validate_grade(grade):
                grade = input("\033[31mInvalid. Enter Grade: \033[0m")
        
            dto = StudentDTO(None, name, int(grade))
            AddStudentCommand(dto).execute()

        elif choice == '2':
            student_id = input("Enter ID to edit: ")
            students = load_students()
            if not any(s['student_id'] == student_id for s in students):
                print(f"\033[31mNo student found with ID {student_id}.\033[0m")
                continue
            name = input("New Name: ")
            grade = input("New Grade: ")
            EditStudentCommand(student_id, name, int(grade)).execute()

        elif choice == '3':
            ViewStudentsCommand().execute()

        elif choice == '4':
            print("\033[32mGoodbye!\033[0m")
            break
        else:
            print("\033[31mInvalid choice\033[0m")

