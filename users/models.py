import abc
from database.db_scripts import execute_database_command


class User:
    def __init__(self, telegram_id, fullname=None, role=None, language_code=None):
        self.id = telegram_id
        self.fullname = fullname
        self.role = role
        self.language_code = language_code

    @abc.abstractmethod
    def get(telegram_id):
        try:
            id, fullname, role, language_code = execute_database_command('SELECT * FROM users WHERE id=%s', (telegram_id, ))[0][0]
            return User(id, fullname, role, language_code)
        except IndexError:
            return None

    def save(self):
        if User.get(self.id):
            execute_database_command(
                'UPDATE users SET fullname = %s, role = %s, language_code = %s WHERE id = %s',
                (self.fullname, self.role, self.language_code, self.id)
            )
        else:
            execute_database_command(
                'INSERT INTO users (id, fullname, role, language_code)  VALUES (%s, %s, %s, %s)',
                (self.id, self.fullname, self.role, self.language_code)
            )
        return self

    def __str__(self):
        return f'{self.fullname if self.fullname else "No name"} (id: {self.id}, role: {self.role})'


class Student:
    def __init__(self, telegram_id, classroom_id, fullname=None, language_code=None):
        self.id = telegram_id
        self.classroom_id = classroom_id
        self.fullname = fullname
        self.language_code = language_code

    @abc.abstractmethod
    def get(telegram_id):
        try:
            id, classroom_id, fullname, language_code = execute_database_command('SELECT * FROM students WHERE id=%s', (telegram_id, ))[0][0]
            return Student(id, classroom_id, fullname, language_code)
        except IndexError:
            return None

    def save(self):
        if Student.get(self.id):
            execute_database_command(
                'UPDATE students SET classroom_id = %s, fullname = %s, language_code = %s WHERE id = %s',
                (self.classroom_id, self.fullname, self.language_code, self.id)
            )
        else:
            execute_database_command(
                'INSERT INTO students (id, classroom_id, fullname, language_code)  VALUES (%s, %s, %s, %s)',
                (self.id, self.classroom_id, self.fullname, self.language_code)
            )
        return self

    def __str__(self):
        return f'{self.fullname if self.fullname else "No name"} (id: {self.id})'
