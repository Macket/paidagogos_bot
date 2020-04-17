import abc
from classrooms.models import Classroom
from tasks.models import Submission
from database.db_scripts import execute_database_command


class Teacher:
    def __init__(self, telegram_id, fullname=None, language_code=None, registered_utc=None):
        self.id = telegram_id
        self.fullname = fullname
        self.language_code = language_code
        self.registered_utc = registered_utc

    @abc.abstractmethod
    def get(telegram_id):
        try:
            id, fullname, language_code, registered_utc = execute_database_command('SELECT * FROM teachers WHERE id=%s', (telegram_id, ))[0][0]
            return Teacher(id, fullname, language_code, registered_utc)
        except IndexError:
            return None

    def save(self):
        if Teacher.get(self.id):
            execute_database_command(
                'UPDATE teachers SET '
                'fullname = %s, '
                'language_code = %s, '
                f'''registered_utc = '{self.registered_utc}' '''
                'WHERE id = %s',
                (self.fullname, self.language_code, self.id)
            )
        else:
            execute_database_command(
                'INSERT INTO teachers (id, fullname, language_code, registered_utc) '
                f'''VALUES (%s, %s, %s, '{self.registered_utc}')''',
                (self.id, self.fullname, self.language_code)
            )
        return self

    def get_classrooms(self):
        try:
            classrooms = execute_database_command('''SELECT cl.teacher_id, cl.name, cl.slug, cl.created_utc, cl.id FROM
            teachers t JOIN classrooms cl ON t.id = cl.teacher_id WHERE t.id=%s''', (self.id, ))[0]
            return [Classroom(cl[0], cl[1], cl[2], cl[3], cl[4]) for cl in classrooms]
        except IndexError:
            return None

    classrooms = property(get_classrooms)

    def __str__(self):
        return f'{self.fullname if self.fullname else "No name"} (id: {self.id})'


class Student:
    def __init__(self, telegram_id, fullname=None, language_code=None, registered_utc=None):
        self.id = telegram_id
        self.fullname = fullname
        self.language_code = language_code
        self.registered_utc = registered_utc

    @abc.abstractmethod
    def get(telegram_id):
        try:
            id, fullname, language_code, registered_utc = execute_database_command('SELECT * FROM students WHERE id=%s', (telegram_id, ))[0][0]
            return Student(id, fullname, language_code, registered_utc)
        except IndexError:
            return None

    def save(self):
        if Student.get(self.id):
            execute_database_command(
                'UPDATE students SET '
                'fullname = %s, '
                'language_code = %s, '
                f'''registered_utc = '{self.registered_utc}' '''
                'WHERE id = %s',
                (self.fullname, self.language_code, self.id)
            )
        else:
            execute_database_command(
                'INSERT INTO students (id, fullname, language_code, registered_utc) '
                f'''VALUES (%s, %s, %s, '{self.registered_utc}')''',
                (self.id, self.fullname, self.language_code)
            )
        return self

    def get_classrooms(self):
        try:
            classrooms = execute_database_command('''SELECT cl.teacher_id, cl.name, cl.slug, cl.created_utc, cl.id FROM
            students s JOIN classroom_students cl_s ON s.id = cl_s.student_id JOIN classrooms cl ON
            cl_s.classroom_id = cl.id WHERE s.id=%s''', (self.id, ))[0]
            return [Classroom(cl[0], cl[1], cl[2], cl[3], cl[4]) for cl in classrooms]
        except IndexError:
            return None

    classrooms = property(get_classrooms)

    def get_submission_for_task(self, task_id):
        try:
            s = execute_database_command('''SELECT s.task_id, s.student_id, s.status, s.comment, s.assessment, s.created_utc, s.id FROM
                        tasks t JOIN submissions s ON t.id = s.task_id WHERE s.student_id=%s AND t.id=%s''',
                                                   (self.id, task_id))[0][0]
            return Submission(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        except IndexError:
            return None

    def get_task_status(self, task_id):
        try:
            return execute_database_command('''SELECT s.status FROM
            tasks t JOIN submissions s ON t.id = s.task_id WHERE s.student_id=%s AND t.id=%s''',
                                              (self.id, task_id))[0][0][0]
        except IndexError:
            return 'NONE'

    def __str__(self):
        return f'{self.fullname if self.fullname else "No name"} (id: {self.id})'
