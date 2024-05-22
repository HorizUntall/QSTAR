import sqlite3 

class FacultyDatabase:

    def __init__(self) -> None:
        self.con = sqlite3.connect('web/database/main database.db')
        self.cursor = self.con.cursor()
        self.create_faculty_database()

    def create_faculty_database(self):
        """Create database table for all registered faculties"""

        self.cursor.execute("CREATE TABLE IF NOT EXISTS registeredFaculties\
                            (faculty_id VARCHAR(20) NOT NULL, \
                            faculty_firstName TEXT NOT NULL, \
                            faculty_lastName TEXT NOT NULL, \
                            faculty_batch INTEGER NOT NULL, \
                            faculty_sex VARCHAR(10))")
        self.con.commit()

    def update_faculty_database(self, facultyID, firstName, lastName, batch, sex):
        """Updates database table for all registered faculties"""

        if (self.cursor.execute("SELECT faculty_id FROM registeredFaculties WHERE faculty_id = ?", (facultyID,)).fetchone()) == None:

            self.cursor.execute("INSERT INTO registeredFaculties\
                                (faculty_id, faculty_firstName, faculty_lastName, faculty_batch, faculty_sex)\
                                VALUES (?,?,?,?,?)", (facultyID, firstName, lastName, batch, sex))
            self.con.commit()
            return "DONE"
        else:
            return "NONE"

    def get_faculty_database(self, facultyID):

        faculty = self.cursor.execute("SELECT faculty_id, faculty_firstName, faculty_lastName, faculty_batch, faculty_sex\
                                      FROM registeredFaculties WHERE faculty_id = ?", (facultyID,)).fetchone()
        
        if faculty == None:
            return False
        else:
            return faculty
    
    def getAll_faculty_database(self):
        registered_faculty = self.cursor.execute("SELECT faculty_id, faculty_firstName, faculty_lastName, faculty_batch, faculty_sex\
                                                FROM registeredFaculties").fetchall()
        return registered_faculty
        
    def delete_everything(self):
        self.cursor.execute("DELETE FROM registeredFaculties")
        print("deleted all data from faculty database")
        self.con.commit()

    def close_db_connection(self):
        self.con.close()