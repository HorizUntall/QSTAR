#student_database.py

import sqlite3

class StudentDatabase:

    def __init__(self) -> None:
        self.con = sqlite3.connect('web/database/main database.db')
        self.cursor = self.con.cursor()
        self.create_student_database()

    def create_student_database(self):
        """Create database table for all registered students"""

        self.cursor.execute("CREATE TABLE IF NOT EXISTS registeredStudents\
                            (student_id VARCHAR(20) NOT NULL, \
                            student_firstName TEXT NOT NULL, \
                            student_lastName TEXT NOT NULL, \
                            student_batch INTEGER NOT NULL, \
                            student_sex VARCHAR(10))")
        self.con.commit()

    def update_student_database(self, studentID, firstName, lastName, batch, sex):    
        """Updates database table for all registered students"""

        #Make sure that all student id is unique and not repeating
        if (self.cursor.execute("SELECT student_id FROM registeredStudents WHERE student_id = ?", (studentID,)).fetchone()) == None:

            self.cursor.execute("INSERT INTO registeredStudents\
                                (student_id, student_firstName, student_lastName, student_batch, student_sex)\
                                VALUES (?,?,?,?,?)", (studentID, firstName, lastName, batch, sex))
            self.con.commit()
            return "DONE"
        else:
            return "NONE"
        
    def get_student_database(self, studentID):

        student = self.cursor.execute("SELECT student_id, student_firstName, student_lastName, student_batch, student_sex\
                                      FROM registeredStudents WHERE student_id = ?", (studentID,)).fetchone()
       
        if student == None:
            return False
        else:
            return student

    def getAll_student_database(self):
        registered_students = self.cursor.execute("SELECT student_id, student_firstName, student_lastName, student_batch, student_sex\
                                                  FROM registeredStudents").fetchall()
        return registered_students


    def delete_everything(self):
        self.cursor.execute("DELETE FROM registeredStudents")
        print("deleted all data from student database")
        self.con.commit()

    def n_remover(self):
        self.cursor.execute("UPDATE registeredStudents\
                            SET student_id = REPLACE(student_id, '\n', '')\
                            WHERE student_id LIKE '%\n%'")
        self.con.commit()
        
    def close_db_connection(self):
        self.con.close()

# for student in StudentDatabase().getAll_student_database():
#     print(student)
