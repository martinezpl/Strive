import db_interface as dbi
import numpy as np
import pandas as pd

students = pd.DataFrame({
    "name" : ["Larry", "Jack", "Jon", "Hoe", "Kick", "Hugo", "Amon", "Damian", "Jon"],
    "surname" : ["Kozack", "Crack", "Glon", "Loe", "Low", "Jucky", "Van Damme", "Ofempera", "Lolek"],
    "id" : np.arange(9),
    "country" : ["Poland", "Greece", "Finland", "Greece", "USA", "USA", "USA", "Scotland", "Czech"]
})

'''
CREATE TABLE IF NOT EXISTS teachers(
                                       name varchar(20) NOT NULL,
                                       surname varchar(20) NOT NULL,
                                       id int PRIMARY KEY NOT NULL,
                                       country varchar(20),
                                       speciality varchar(20) NOT NULL,
                                       salary int,

                                       FOREIGN KEY(id) REFERENCES projects(st));
'''
teachers = pd.DataFrame({
    "name" : ["Bruno", "Sven", "Ash", "Kendrick"],
    "surname" : ["Golec", "Rampage", "Ketchup", "Lamer"],
    "id" : [0, 1, 2, 4],
    "country" : ["Poland", "Sweden", "Alabastia", "Compton"],
    "speciality" : ["ML", "Krav Maga", "Pokemon", "ML"],
    "salary" : [1200, 5000, 300, 1500]
})
'''
CREATE TABLE IF NOT EXISTS projects(
                                       nameP varchar(20) NOT NULL,
                                       topic varchar(20) NOT NULL,
                                       st int,
                                       grade float,
                                       id int PRIMARY KEY NOT NULL,
                                       tch varchar(20) NOT NULL,

                                       FOREIGN KEY(st) REFERENCES students(id) ON UPDATE RESTRICT,
                                       FOREIGN KEY(tch) REFERENCES teachers(id) ON UPDATE RESTRICT
);
'''
projects = pd.DataFrame({
    "nameP" : ["Kicking ass", "COVID Vaccine", "Classified", "Tracking crypto sentiment", "Chatbot"],
    "topic" : ["Martial Arts", "Biotech", "Pokemon", "NLP", "NLP"],
    "st" : [3, 5, 7, 0, 6],
    "grade" : [5, 3, 4.5, 5, 4],
    "id" : [0, 1, 2, 3, 4],
    "tch" : [1, 2, 2, 0, 0]
})

def fill_tables():
    projects.to_sql("projects", dbi.get_conn(), if_exists = 'replace')
    students.to_sql("students", dbi.get_conn(), if_exists = 'replace')
    teachers.to_sql("teachers", dbi.get_conn(), if_exists = 'replace')

def count_students():
    students_qty = dbi.sql_execute("SELECT COUNT(id) FROM students").fetchone()[0]
    print("\nNUMBER OF STUDENTS:", students_qty)

def students_with_NLP_projects():
    df = pd.read_sql("""SELECT name, surname, s.id, country, nameP, topic, grade, tch
                             FROM students AS s, projects AS p
                             WHERE s.id = p.st
                             AND p.topic = "NLP"
                             """,
                     dbi.get_conn()
                     ).reset_index(drop=True)
    print("\nSTUDENTS WTIH NLP PROJECTS\n", df.to_string())


def ml_teachers_with_salary():
    df = pd.read_sql("""SELECT name, surname, t.id, country, speciality, salary
                             FROM teachers AS t
                             WHERE t.speciality == "ML"
                             AND t.salary > 1200
                             """,
                     dbi.get_conn()
                     ).reset_index(drop=True)
    print("\nML TEACHERS OVERS 1200\n", df.to_string())

def add_field_to_students():
    dbi.sql_execute("""ALTER TABLE students 
                        ADD favTch 
                        DEFAULT 2
                    """)
    print("\nADDED COLUMN, EVERYONE LOVES ASH\n",
          dbi.sql_execute("""SELECT name, favTch                     
                                FROM students""").fetchall())

def delete_jans():
    dbi.sql_execute("""DELETE FROM students
                        WHERE name LIKE 'J%n'""")
    print("\nSTUDENTS AFTER DELETION\n",
          dbi.sql_execute("""SELECT name FROM students""").fetchall())

def count_unique_names():
    students_qty = dbi.sql_execute("SELECT COUNT(DISTINCT name) FROM students").fetchone()[0]
    print("\nNUMBER OF UNIQUE NAMES:", students_qty)

def join_tables():
    df = pd.read_sql("""SELECT * FROM students 
                    INNER JOIN projects 
                    ON students.id = projects.st """,
                dbi.get_conn())
    print(df.to_string())

def best_students():
    print("\n BEST STUDENTS:\n",
        dbi.sql_execute("""SELECT s.name
                            FROM students AS s, projects AS p
                            WHERE s.id = p.st 
                            AND p.grade = (SELECT MAX(grade) FROM projects)""").fetchall())

def wrong_teachers():
    print("\n WRONG TEACHERS:\n",
          pd.read_sql("""SELECT s.name, s.surname, p.topic, t.name, t.surname, t.speciality 
                        FROM students AS s, projects AS p, teachers AS t
                        WHERE s.id = p.st
                        AND p.tch = t.id
                        AND t.speciality != p.topic""",
                      dbi.get_conn()).to_string())
if __name__ == "__main__":
    fill_tables()
    count_students()
    students_with_NLP_projects()
    ml_teachers_with_salary()
    add_field_to_students()
    delete_jans()
    count_unique_names()
    join_tables()
    best_students()
    wrong_teachers()