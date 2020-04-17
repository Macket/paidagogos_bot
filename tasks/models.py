import abc
from database.db_scripts import execute_database_command
from datetime import datetime, timezone
from enum import Enum


class Task:
    def __init__(self, classroom_id, name, created_utc=None, id=None):
        self.classroom_id = classroom_id
        self.name = name
        self.created_utc = created_utc
        self.id = id

    @abc.abstractmethod
    def get(task_id):
        try:
            id, classroom_id, name, created_utc = execute_database_command('SELECT * FROM tasks WHERE id=%s', (task_id, ))[0][0]
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
        TaskMessage(self.id, message.chat.id, message.message_id, datetime.now(timezone.utc)).save()

    def get_messages(self):
        try:
            task_messages = execute_database_command('''SELECT tm.task_id, tm.teacher_id, tm.message_id, tm.created_utc, tm.id FROM
            tasks t JOIN task_messages tm ON t.id = tm.task_id WHERE t.id=%s''', (self.id, ))[0]
            return [TaskMessage(tm[0], tm[1], tm[2], tm[3], tm[4]) for tm in task_messages]
        except IndexError:
            return None

    messages = property(get_messages)

    def get_submissions_for_review(self):
        try:
            submissions = execute_database_command('''SELECT s.task_id, s.student_id, s.status, s.comment, s.assessment, s.created_utc, s.id FROM
            tasks t JOIN submissions s ON t.id = s.task_id WHERE t.id=%s AND s.status=%s''', (self.id, SubmissionStatus.REVIEW.value))[0]
            return [Submission(s[0], s[1], s[2], s[3], s[4], s[5], s[6]) for s in submissions]
        except IndexError:
            return None

    submissions_for_review = property(get_submissions_for_review)

    def get_submissions_reviewed(self):
        try:
            submissions = execute_database_command('''SELECT s.task_id, s.student_id, s.status, s.comment, s.assessment, s.created_utc, s.id FROM
            tasks t JOIN submissions s ON t.id = s.task_id WHERE t.id=%s AND s.status=%s''', (self.id, SubmissionStatus.REVIEWED.value))[0]
            return [Submission(s[0], s[1], s[2], s[3], s[4], s[5], s[6]) for s in submissions]
        except IndexError:
            return None

    submissions_reviewed = property(get_submissions_reviewed)

    def get_submissions_for_review_count(self):
        try:
            return execute_database_command('''SELECT COUNT(s.id) FROM
            tasks t JOIN submissions s ON t.id = s.task_id WHERE t.id=%s AND s.status=%s''',
                                            (self.id, SubmissionStatus.REVIEW.value))[0][0][0]
        except IndexError:
            return None

    submissions_for_review_count = property(get_submissions_for_review_count)

    def get_submissions_reviewed_count(self):
        try:
            return execute_database_command('''SELECT COUNT(s.id) FROM
            tasks t JOIN submissions s ON t.id = s.task_id WHERE t.id=%s AND s.status=%s''',
                                            (self.id, SubmissionStatus.REVIEWED.value))[0][0][0]
        except IndexError:
            return None

    submissions_reviewed_count = property(get_submissions_reviewed_count)

    def __str__(self):
        return f'{self.name} (id: {self.id})'


class TaskMessage:
    def __init__(self, task_id, teacher_id, message_id, created_utc=None, id=None):
        self.task_id = task_id
        self.teacher_id = teacher_id
        self.message_id = message_id
        self.created_utc = created_utc
        self.id = id

    @abc.abstractmethod
    def get(task_message_id):
        try:
            id, teacher_id, task_id, message_id, created_utc = execute_database_command('SELECT * FROM task_messages WHERE id=%s', (task_message_id, ))[0][0]
            return TaskMessage(task_id, teacher_id, message_id, created_utc, id)
        except IndexError:
            return None

    def save(self):
        if TaskMessage.get(self.id):
            execute_database_command(
                'UPDATE task_messages SET '
                'task_id = %s, '
                'teacher_id = %s, '
                'message_id = %s, '
                f'''created_utc = '{self.created_utc}' '''
                'WHERE id = %s',
                (self.task_id, self.teacher_id, self.message_id, self.id)
            )
        else:
            task_message_id = execute_database_command(
                'INSERT INTO task_messages (task_id, teacher_id, message_id, created_utc) '
                f'''VALUES (%s, %s, %s, '{self.created_utc}') RETURNING id''',
                (self.task_id, self.teacher_id, self.message_id)
            )[0][0][0]
            return TaskMessage(self.task_id, self.teacher_id, self.message_id, self.created_utc, task_message_id)

    def __str__(self):
        return f'Task: {self.task_id} (Message: {self.message_id})'


class Submission:
    def __init__(self, task_id, student_id, status, comment=None, assessment=None, created_utc=None, id=None):
        self.task_id = task_id
        self.student_id = student_id
        self.status = status
        self.comment = comment
        self.assessment = assessment
        self.created_utc = created_utc
        self.id = id

    @abc.abstractmethod
    def get(submission_id):
        try:
            id, task_id, student_id, status, comment, assessment, created_utc = execute_database_command('SELECT * FROM submissions WHERE id=%s', (submission_id, ))[0][0]
            return Submission(task_id, student_id, status, comment, assessment, created_utc, id)
        except IndexError:
            return None

    def save(self):
        if Submission.get(self.id):
            execute_database_command(
                'UPDATE submissions SET '
                'task_id = %s, '
                'student_id = %s, '
                'status = %s, '
                'comment = %s, '
                'assessment = %s, '
                f'''created_utc = '{self.created_utc}' '''
                'WHERE id = %s',
                (self.task_id, self.student_id, self.status, self.comment, self.assessment, self.id)
            )
        else:
            submission_id = execute_database_command(
                'INSERT INTO submissions (task_id, student_id, status, comment, assessment, created_utc) '
                f'''VALUES (%s, %s, %s, %s, %s, '{self.created_utc}') RETURNING id''',
                (self.task_id, self.student_id, self.status, self.comment, self.assessment)
            )[0][0][0]
            return Submission(self.task_id, self.student_id, self.status, self.comment, self.assessment, self.created_utc, submission_id)

    def add(self, message):
        SubmissionMessage(self.id, message.chat.id, message.message_id, datetime.now(timezone.utc)).save()

    def get_messages(self):
        try:
            submission_messages = execute_database_command('''SELECT sm.submission_id, sm.student_id, sm.message_id, sm.created_utc, sm.id FROM
            submissions s JOIN submission_messages sm ON s.id = sm.submission_id WHERE s.id=%s''', (self.id, ))[0]
            return [SubmissionMessage(sm[0], sm[1], sm[2], sm[3], sm[4]) for sm in submission_messages]
        except IndexError:
            return None

    messages = property(get_messages)

    def __str__(self):
        return f'{self.id} (task: {self.task_id}, status: {self.status})'


class SubmissionMessage:
    def __init__(self, submission_id, student_id, message_id, created_utc=None, id=None):
        self.submission_id = submission_id
        self.student_id = student_id
        self.message_id = message_id
        self.created_utc = created_utc
        self.id = id

    @abc.abstractmethod
    def get(submission_message_id):
        try:
            id, student_id, submission_id, message_id, created_utc = execute_database_command('SELECT * FROM submission_messages WHERE id=%s', (submission_message_id, ))[0][0]
            return SubmissionMessage(submission_id, student_id, message_id, created_utc, id)
        except IndexError:
            return None

    def save(self):
        if SubmissionMessage.get(self.id):
            execute_database_command(
                'UPDATE submission_messages SET '
                'submission_id = %s, '
                'student_id = %s, '
                'message_id = %s, '
                f'''created_utc = '{self.created_utc}' '''
                'WHERE id = %s',
                (self.submission_id, self.student_id, self.message_id, self.id)
            )
        else:
            submission_message_id = execute_database_command(
                'INSERT INTO submission_messages (submission_id, student_id, message_id, created_utc) '
                f'''VALUES (%s, %s, %s, '{self.created_utc}') RETURNING id''',
                (self.submission_id, self.student_id, self.message_id)
            )[0][0][0]
            return SubmissionMessage(self.submission_id, self.student_id, self.message_id, self.created_utc, submission_message_id)

    def __str__(self):
        return f'Submission: {self.submission_id} (Message: {self.message_id})'


class SubmissionStatus(Enum):
    DRAFT = 'DRAFT'
    REVIEW = 'REVIEW'
    REVIEWED = 'REVIEWED'


# TODO add English
STATUS_ICONS = {
    'NONE': '🔔',
    'DRAFT': '✍️',
    'REVIEW': '⏳',
    'REVIEWED': '✅',
}

# TODO add English
STATUS_BADGES = {
    'NONE': '🔔 Не сдано',
    'DRAFT': '✍️ Черновик',
    'REVIEW': '⏳ На проверке',
    'REVIEWED': '✅ Проверено',
}
