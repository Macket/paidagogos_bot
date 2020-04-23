import abc
import string
import random
from database.db_scripts import execute_database_command
from tasks.models import Task


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
            )[0][0][0]
            return Classroom(self.teacher_id, self.name, generated_slug, self.created_utc, classroom_id)

    def delete(self):
        execute_database_command('DELETE from classrooms WHERE id=%s', (self.id, ))

    def get_tasks(self):
        try:
            tasks = execute_database_command('''SELECT t.classroom_id, t.name, t.created_utc, t.id FROM
            classrooms cl JOIN tasks t ON cl.id = t.classroom_id WHERE cl.id=%s ORDER BY t.created_utc DESC''', (self.id, ))[0]
            return [Task(t[0], t[1], t[2], t[3]) for t in tasks]
        except IndexError:
            return None

    tasks = property(get_tasks)

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
            id, classroom_id, student_id, joined_utc = execute_database_command('SELECT * FROM classroom_students WHERE id=%s', (classroom_student_id, ))[0][0]
            return ClassroomStudent(classroom_id, student_id, joined_utc, id)
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
            )[0][0][0]
            return ClassroomStudent(self.classroom_id, self.student_id, self.joined_utc, classroom_student_id)

    def __str__(self):
        return f'Classroom: {self.classroom_id} (Student: {self.student_id})'
