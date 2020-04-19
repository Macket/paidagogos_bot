from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from tasks.models import Task
from tasks.views import task_detail_view_, submission_list_view_, submission_review_result_view_


def new_task_notification(task):
    classroom = Classroom.get(task.classroom_id)
    teacher = Teacher.get(classroom.teacher_id)
    students = Student.get_classroom_students(classroom.id)

    ru_text = f"🔔 Новое задание: *{task.name}*\n\n*{classroom.name}*. Учитель: _{teacher.fullname}_"
    en_text = None

    for student in students:
        text = ru_text if student.language_code == 'ru' else en_text
        bot.send_message(student.id, text, parse_mode='MarkDown')
        task_detail_view_(student.id, task.id)


def new_submission_notification(submission):
    task = Task.get(submission.task_id)
    classroom = Classroom.get(task.classroom_id)
    student = Student.get(submission.student_id)
    teacher = Teacher.get(classroom.teacher_id)

    ru_text = f"🔔 Новое задание на проверку: *{task.name}*\n\n*{classroom.name}*. Ученик: _{student.fullname}_"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(classroom.teacher_id, text, parse_mode='MarkDown')
    submission_list_view_(teacher.id, task.id)


def new_submission_review_result_notification(submission):
    task = Task.get(submission.task_id)
    classroom = Classroom.get(task.classroom_id)
    student = Student.get(submission.student_id)
    teacher = Teacher.get(classroom.teacher_id)

    ru_text = f"🔔 Ваше задание проверено: *{task.name}*\n\n*{classroom.name}*. Учитель: _{teacher.fullname}_"
    en_text = None
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(student.id, text, parse_mode='MarkDown')
    submission_review_result_view_(student.id, submission.id)
    task_detail_view_(student.id, task.id)
