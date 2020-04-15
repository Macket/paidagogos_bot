import abc
from database.db_scripts import execute_database_command
import string
import random


class Classroom:
    def __init__(self, teacher_id, name, slug=None, created_utc=None, id=None):
        self.teacher_id = teacher_id
        self.name = name
        self.slug = slug
        self.created_utc = created_utc
        self.id = id

    @abc.abstractmethod
    def get(classroom_id):
        try:
            id, teacher_id, name, slug, created_utc = execute_database_command('SELECT * FROM classrooms WHERE id=%s', (classroom_id, ))[0][0]
            return Classroom(teacher_id, name, slug, created_utc, id)
        except IndexError:
            return None

    @abc.abstractmethod
    def get_by_slug(classroom_slug):
        try:
            id, teacher_id, name, slug, created_utc = execute_database_command('SELECT * FROM classrooms WHERE slug=%s', (classroom_slug,))[0][0]
            return Classroom(teacher_id, name, slug, created_utc, id)
        except IndexError:
            return None

    def save(self):
        if Classroom.get(self.id):
            execute_database_command(
                'UPDATE classrooms SET '
                'teacher_id = %s, '
                'name = %s, '
                'slug = %s, '
                f'''created_utc = '{self.created_utc}' '''
                'WHERE id = %s',
                (self.teacher_id, self.name, self.slug, self.id)
            )
        else:
            generated_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            classroom_id = execute_database_command(
                'INSERT INTO classrooms (teacher_id, name, slug, created_utc) '
                f'''VALUES (%s, %s, %s, '{self.created_utc}') RETURNING id''',
                (self.teacher_id, self.name, generated_slug)
            )
            return Classroom(self.teacher_id, self.name, generated_slug, classroom_id)

    def __str__(self):
        return f'{self.name} (id: {self.id})'


class ClassroomStudent:
    def __init__(self, classroom_id, student_id, joined_utc=None, id=None):
        self.classroom_id = classroom_id
        self.student_id = student_id
        self.joined_utc = joined_utc
        self.id = id

    @abc.abstractmethod
    def get(classroom_student_id):
        try:
            id, classroom_id, student_id, joined_utc = execute_database_command('SELECT * FROM classrooms WHERE id=%s', (classroom_student_id, ))[0][0]
            return Classroom(classroom_id, student_id, joined_utc, id)
        except IndexError:
            return None

    def save(self):
        if ClassroomStudent.get(self.id):
            execute_database_command(
                'UPDATE classroom_students SET '
                'classroom_id = %s, '
                'student_id = %s, '
                f'''joined_utc = '{self.joined_utc}' '''
                'WHERE id = %s',
                (self.classroom_id, self.student_id, self.id)
            )
        else:
            classroom_student_id = execute_database_command(
                'INSERT INTO classroom_students (classroom_id, student_id, joined_utc) '
                f'''VALUES (%s, %s, '{self.joined_utc}') RETURNING id''',
                (self.classroom_id, self.student_id)
            )
            return Classroom(self.classroom_id, self.student_id, classroom_student_id)

    def __str__(self):
        return f'Classroom: {self.classroom_id} (Student: {self.student_id})'


# class Photo:
#     def __init__(self, telegram_id, student_id, teacher_id):
#         self.id = telegram_id
#         self.student_id = student_id
#         self.teacher_id = teacher_id
#
#     @abc.abstractmethod
#     def get(telegram_id):
#         try:
#             id, student_id, teacher_id = execute_database_command('SELECT * FROM photos WHERE id=%s', (telegram_id,))[0][0]
#             return Photo(id, student_id, teacher_id)
#         except IndexError:
#             return None
#
#     def save(self):
#         if Photo.get(self.id):
#             execute_database_command(
#                 'UPDATE photos SET student_id = %s, teacher_id = %s WHERE id = %s',
#                 (self.student_id, self.teacher_id, self.id)
#             )
#         else:
#             execute_database_command(
#                 'INSERT INTO photos (id, student_id, teacher_id)  VALUES (%s, %s, %s)',
#                 (self.id, self.student_id, self.teacher_id,)
#             )
#         return self
#
#     def __str__(self):
#         return f'{self.id}'
