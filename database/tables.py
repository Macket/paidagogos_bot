# id == telegram_id
CREATE_TEACHERS_TABLE = """
       CREATE TABLE teachers (
           id BIGINT PRIMARY KEY,
           fullname VARCHAR(255),
           language_code VARCHAR(15),
           registered_utc TIMESTAMP
       )
       """

DROP_TEACHERS_TABLE = """
       DROP TABLE teachers;
"""


# id == telegram_id
CREATE_STUDENTS_TABLE = """
       CREATE TABLE students (
           id BIGINT PRIMARY KEY,
           fullname VARCHAR(255),
           language_code VARCHAR(15),
           registered_utc TIMESTAMP
       )
       """

DROP_STUDENTS_TABLE = """
       DROP TABLE students;
"""

CREATE_CLASSROOMS_TABLE = """
       CREATE TABLE classrooms (
           id BIGSERIAL PRIMARY KEY,
           teacher_id BIGINT,
           name VARCHAR(255),
           slug VARCHAR(63),
           created_utc TIMESTAMP,
           FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE 
       )
       """

DROP_CLASSROOMS_TABLE = """
       DROP TABLE classrooms;
"""


CREATE_CLASSROOM_STUDENTS_TABLE = """
       CREATE TABLE classroom_students (
           id BIGSERIAL PRIMARY KEY,
           classroom_id BIGINT,
           student_id BIGINT,
           joined_utc TIMESTAMP,
           FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
           FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
       )
       """

DROP_CLASSROOM_STUDENTS_TABLE = """
       DROP TABLE classroom_students;
"""

CREATE_TASKS_TABLE = """
       CREATE TABLE tasks (
           id BIGSERIAL PRIMARY KEY,
           classroom_id BIGINT,
           name VARCHAR(255),
           created_utc TIMESTAMP,
           FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE
       )
       """


DROP_TASKS_TABLE = """
       DROP TABLE tasks;
"""

CREATE_TASK_MESSAGES_TABLE = """
       CREATE TABLE task_messages (
           id BIGSERIAL PRIMARY KEY,
           task_id BIGINT,
           teacher_id BIGINT,
           message_id BIGINT,
           created_utc TIMESTAMP,
           FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
           FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE
       )
       """


DROP_TASK_MESSAGES_TABLE = """
       DROP TABLE task_messages;
"""



CREATE_SUBMISSIONS_TABLE = """
       CREATE TABLE submissions (
           id BIGSERIAL PRIMARY KEY,
           task_id BIGINT,
           assessment VARCHAR(63) DEFAULT NULL,
           created_utc TIMESTAMP,
           FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
       )
       """

DROP_SUBMISSIONS_TABLE = """
       DROP TABLE submissions;
"""


CREATE_SUBMISSION_MESSAGES_TABLE = """
       CREATE TABLE submission_messages (
           id BIGSERIAL PRIMARY KEY,
           submission_id BIGINT,
           student_id BIGINT,
           message_id BIGINT,
           created_utc TIMESTAMP,
           FOREIGN KEY (submission_id) REFERENCES submissions (id) ON DELETE CASCADE,
           FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
       )
       """


DROP_SUBMISSION_MESSAGES_TABLE = """
       DROP TABLE submission_messages;
"""
