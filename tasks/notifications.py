from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from tasks.models import Task
from tasks.views import task_detail_view, submission_review_result_view


def new_task_notification(task):
    classroom = Classroom.get(task.classroom_id)
    teacher = Teacher.get(classroom.teacher_id)
    students = Student.get_classroom_students(classroom.id)

    ru_text = f"🔔 Новое задание: *{task.name}*\n\n*{classroom.name}*. Учитель: _{teacher.fullname}_"
    en_text = f"🔔 New task: *{task.name}*\n\n*{classroom.name}*. Teacher: _{teacher.fullname}_"

    for student in students:
        text = ru_text if student.language_code == 'ru' else en_text
        bot.send_message(student.id, text, parse_mode='MarkDown')
        task_detail_view(student, task)


def new_submission_review_result_notification(submission):
    task = Task.get(submission.task_id)
    classroom = Classroom.get(task.classroom_id)
    student = Student.get(submission.student_id)
    teacher = Teacher.get(classroom.teacher_id)

    ru_text = f"🔔 Ваше задание проверено\n\n*{classroom.name}*\n_{teacher.fullname}_"
    en_text = f"🔔 New submission review\n\n*{classroom.name}*\n_{teacher.fullname}_"
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(student.id, text, parse_mode='MarkDown')
    submission_review_result_view(student, submission, task)
    task_detail_view(student, task)
