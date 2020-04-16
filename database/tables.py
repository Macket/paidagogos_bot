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

# DROP_PHOTOS_TABLE = """
#        DROP TABLE photos;
# """


# CREATE_PHOTOS_TABLE = """
#        CREATE TABLE photos (
#            id VARCHAR(255) PRIMARY KEY,
#            student_id BIGINT,
#            teacher_id BIGINT,
#            FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE,
#            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
#        )
#        """


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
           message_id BIGINT,
           created_utc TIMESTAMP,
           FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
       )
       """


DROP_TASK_MESSAGES_TABLE = """
       DROP TABLE task_messages;
"""



# DROP_SUBMISSIONS_TABLE = """
#        DROP TABLE submissions;
# """
#
# CREATE_SUBMISSIONS_TABLE = """
#        CREATE TABLE submissions (
#            id BIGSERIAL PRIMARY KEY,
#            task_id BIGINT,
#            message_ids VARCHAR(1023),
#            assessment VARCHAR(63) DEFAULT NULL,
#            FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
#        )
#        """
