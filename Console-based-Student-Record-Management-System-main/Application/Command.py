from DTOs.StudentDTO import StudentDTO
from Domain.StudentFactory import StudentFactory
from DataAccess.QuoteAPIAdapter import QuoteAPIAdapter
from DataAccess.StudentRepository import add_student_to_file, update_student_in_file, get_all_students, load_students


class Command:
    def execute(self):
        pass

class AddStudentCommand(Command):
    def __init__(self, dto: StudentDTO):
        self.dto = dto

    def execute(self):
        students = load_students()
        if self.dto.student_id is None:
            max_id = max((int(s['student_id']) for s in students), default=0)
            self.dto.student_id = str(max_id + 1)
        student = StudentFactory.create(self.dto)
        add_student_to_file(student)
        print("\033[32mStudent Added Successfully:\033[0m", student)
        quote = QuoteAPIAdapter().get_quote()
        print("\033[35mMotivational Quote:\033[0m", quote)


class EditStudentCommand(Command):
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def execute(self):
        update_student_in_file(self.student_id, self.name, self.grade)
        print("\033[32mStudent Updated Successfully!\033[0m")

class ViewStudentsCommand(Command):
    def execute(self):
        students = get_all_students()
        print("\033[35mAll Students:\033[0m")
        for s in students:
            print(s)