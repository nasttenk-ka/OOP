from DTOs import StudentDTO
from Domain.Student import Student

class StudentFactory:
    @staticmethod
    def create(dto: StudentDTO) -> Student:
        return Student(dto.student_id, dto.name, dto.grade)