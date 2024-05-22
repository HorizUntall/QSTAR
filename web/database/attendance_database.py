#attendance_database.py

import sqlite3
import csv
from datetime import datetime, timedelta

try: #when running from main.py
    from web.database.config.config import Config
except: #when running from attendance_database.py itself
    from config.config import Config
    
# minimum_minutes = 10

class AttendanceDatabase:

    def __init__(self) -> None:
        self.con = sqlite3.connect('web/database/main database.db')
        self.cursor = self.con.cursor()
        self.create_attendance_table()
        self.minimum_minutes = int(Config().get_value("anti_spam_minutes")[0])

    def create_attendance_table(self):
        """Create attendance table"""

        self.cursor.execute("CREATE TABLE IF NOT EXISTS attendance\
                            (id VARCHAR(20) NOT NULL, \
                            firstName TEXT NOT NULL, \
                            lastName TEXT NOT NULL, \
                            batch INTEGER NOT NULL, \
                            sex VARCHAR(10), \
                            time_in VARCHAR(50), \
                            time_out VARCHAR(50))")
        self.con.commit()

    def create_attendance(self, id, firstName, lastName, batch, sex, time):
        """Make an attendance"""

        empty = ""
        return_value = ""

        previous_timeIn = (self.cursor.execute("SELECT time_in FROM attendance  WHERE id = ? \
                                              ORDER BY time_in DESC LIMIT 1", (id,)).fetchone())
        
        previous_timeIn = previous_timeIn[0] if previous_timeIn != None else None
        
        print("previous time: ", previous_timeIn)

        #timeIn is True if there is no empty time_out
        timeIn = (self.cursor.execute("SELECT time_out FROM attendance \
                                     WHERE id = ? AND time_out = ?", 
                                     (id, empty)).fetchone()) == None
        if timeIn:

            if previous_timeIn and self.calc_time_difference(previous_timeIn, str(time)) < 10:
                self.cursor.execute("UPDATE attendance SET time_out = ? WHERE id = ? and time_in = ?", (empty, id, previous_timeIn))

            else:
                self.cursor.execute("INSERT INTO attendance \
                                    (id, firstName, lastName, batch, sex, time_in, time_out) \
                                    VALUES (?,?,?,?,?,?,?)",
                                    (id, firstName, lastName, batch, sex, time, empty))
                
            return_value = "IN"
            
            #there's no id because the csv file has no id column
            # self.csv_transfer((firstName, lastName, batch, sex, time.strftime("%Y-%m-%d %H:%M:%S"), '')) 
        else: 
            self.cursor.execute("UPDATE attendance SET time_out = ? WHERE id = ? AND time_out = ?",
                                (time, id, empty))
            return_value = "OUT"
            # self.csv_update(firstName, lastName, time)
        self.con.commit()
        return return_value
    
    def calc_time_difference(self, date1, date2):
        datetime1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        datetime2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')

        time_difference = datetime2 - datetime1

        return (time_difference.total_seconds()/60)
    
    #automatically sets the time out to 5pm for time-ins from yesterday with empty time-outs
    def auto_timeOut(self):
        empty = ""
        yesterday_date = datetime.now() - timedelta(days=1)

        #Updates time_out to the 5pm version of time_in
        self.cursor.execute("UPDATE attendance set time_out = substr(time_in, 1, 10) || ' 17:00:00.000000' \
                            WHERE time_out = ? AND time_in < ?",
                            (empty, yesterday_date.strftime('%Y-%m-%d 23:59:59')))
        
        self.con.commit()

    def getAll_attendance(self):
        users = self.cursor.execute("SELECT firstName, lastName, batch, sex, time_in, time_out\
                                   FROM attendance").fetchall()
        
        if len(users) > 0:
            return users
        else:
            return "NONE"
        
    def printAll(self):
        users = self.cursor.execute("SELECT firstName, lastName, batch, sex, time_in, time_out\
                                   FROM attendance").fetchall()
        
        for user in users:
            print(user)

    def deleteAttendance(self, id, date):
        self.cursor.execute("DELETE FROM attendance WHERE id = ? AND time_in = ?", (id,date))
        self.con.commit()

    def tester(self, id, firstName, lastName, batch, sex, time):
        empty = ""
        timeIn = (self.cursor.execute("SELECT time_out FROM attendance \
                                     WHERE id = ? AND time_out = ?", 
                                     (id, empty)).fetchone()) == None
        if timeIn:
            self.cursor.execute("INSERT INTO attendance \
                                (id, firstName, lastName, batch, sex, time_in, time_out) \
                                VALUES (?,?,?,?,?,?,?)",
                                (id, firstName, lastName, batch, sex, time, empty))
        else:
            self.cursor.execute("UPDATE attendance SET time_out = ? WHERE id = ? AND time_out = ?",
                                (time, id, empty))
        self.con.commit()


# print (AttendanceDatabase().minimum_minutes)
# AttendanceDatabase().auto_timeOut()
# AttendanceDatabase().deleteAttendance('16-2018-082', '2024-03-24 08:02:58.303760')
# AttendanceDatabase().tester(id='16-2018-082', firstName="Ray Emanuele", lastName="Untal", batch=2024, sex="Male", time = (datetime.now() - timedelta(days=3)))
# AttendanceDatabase().printAll()