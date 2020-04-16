import abc
from database.db_scripts import execute_database_command
from datetime import datetime, timezone


class Task:
    def __init__(self, classroom_id, name, created_utc=None, id=None):
        self.classroom_id = classroom_id
        self.name = name
        self.created_utc = created_utc
        self.id = id

    @abc.abstractmethod
    def get(task_id):
        try:
            id, classroom_id, name, created_utc = execute_database_command('SELECT * FROM classrooms WHERE id=%s', (task_id, ))[0][0]
            return Task(classroom_id, name, created_utc, id)
        except IndexError:
            return None

    def save(self):
        if Task.get(self.id):
            execute_database_command(
                'UPDATE tasks SET '
                'classroom_id = %s, '
                'name = %s, '
                f'''created_utc = '{self.created_utc}' '''
                'WHERE id = %s',
                (self.classroom_id, self.name, self.id)
            )
        else:
            task_id = execute_database_command(
                'INSERT INTO tasks (classroom_id, name, created_utc) '
                f'''VALUES (%s, %s, '{self.created_utc}') RETURNING id''',
                (self.classroom_id, self.name)
            )[0][0][0]
            return Task(self.classroom_id, self.name, self.created_utc, task_id)

    def add(self, message):
        TaskMessages(self.id, message.message_id, datetime.now(timezone.utc)).save()

    def __str__(self):
        return f'{self.name} (id: {self.id})'


class TaskMessages:
    def __init__(self, task_id, message_id, created_utc=None, id=None):
        self.task_id = task_id
        self.message_id = message_id
        self.created_utc = created_utc
        self.id = id

    @abc.abstractmethod
    def get(task_message_id):
        try:
            id, task_id, message_id, created_utc = execute_database_command('SELECT * FROM task_messages WHERE id=%s', (task_message_id, ))[0][0]
            return TaskMessages(task_id, message_id, created_utc, id)
        except IndexError:
            return None

    def save(self):
        if TaskMessages.get(self.id):
            execute_database_command(
                'UPDATE task_messages SET '
                'task_id = %s, '
                'message_id = %s, '
                f'''created_utc = '{self.created_utc}' '''
                'WHERE id = %s',
                (self.task_id, self.message_id, self.id)
            )
        else:
            task_message_id = execute_database_command(
                'INSERT INTO task_messages (task_id, message_id, created_utc) '
                f'''VALUES (%s, %s, '{self.created_utc}') RETURNING id''',
                (self.task_id, self.message_id)
            )[0][0][0]
            return TaskMessages(self.task_id, self.message_id, self.created_utc, task_message_id)

    def __str__(self):
        return f'Task: {self.task_id} (Message: {self.message_id})'
