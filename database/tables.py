DROP_USERS_TABLE = """
       DROP TABLE users;
"""

# id == telegram_id
CREATE_USERS_TABLE = """
       CREATE TABLE users (
           id BIGINT PRIMARY KEY,
           fullname VARCHAR(255),
           role VARCHAR(15),
           language_code VARCHAR(15)
       )
       """

DROP_CLASSROOMS_TABLE = """
       DROP TABLE classrooms;
"""

CREATE_CLASSROOMS_TABLE = """
       CREATE TABLE classrooms (
           id BIGSERIAL PRIMARY KEY,
           teacher_id BIGINT,
           name VARCHAR(255),
           slug VARCHAR(63),
           FOREIGN KEY (teacher_id) REFERENCES users (id) ON DELETE CASCADE 
       )
       """

DROP_STUDENTS_TABLE = """
       DROP TABLE students;
"""

# id == telegram_id
CREATE_STUDENTS_TABLE = """
       CREATE TABLE students (
           id BIGINT PRIMARY KEY,
           classroom_id BIGINT,
           fullname VARCHAR(255),
           language_code VARCHAR(15),
           FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE
       )
       """


DROP_PHOTOS_TABLE = """
       DROP TABLE photos;
"""

# id == telegram_id
CREATE_PHOTOS_TABLE = """
       CREATE TABLE photos (
           id VARCHAR(255) PRIMARY KEY,
           student_id BIGINT,
           teacher_id BIGINT,
           FOREIGN KEY (teacher_id) REFERENCES users (id) ON DELETE CASCADE,
           FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
       )
       """


# DROP_TASKS_TABLE = """
#        DROP TABLE tasks;
# """
#
# CREATE_TASKS_TABLE = """
#        CREATE TABLE tasks (
#            id BIGSERIAL PRIMARY KEY,
#            classroom_id BIGINT,
#            message_ids VARCHAR(1023),
#            FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE
#        )
#        """
#
#
# DROP_CLASSROOM_STUDENTS_TABLE = """
#        DROP TABLE classroom_students;
# """
#
# CREATE_CLASSROOM_STUDENTS_TABLE = """
#        CREATE TABLE classroom_students (
#            id BIGSERIAL PRIMARY KEY,
#            classroom_id BIGINT,
#            student_id BIGINT,
#            FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
#            FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE
#        )
#        """
#
#
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
