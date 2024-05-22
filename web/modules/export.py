#export.py
import csv
import sqlite3

con = sqlite3.connect('web/database/main database.db')
cursor = con.cursor()
x = 10
def exportall(tableName, csv_file_path = "exported data.csv"):
    sql_query = f"SELECT * FROM {tableName}"
    rows = cursor.execute(sql_query).fetchall()

    match tableName:
        case "attendance":
            headers = ["ID", "First Name", "Last Name", "Batch", "Sex", "Time-In", "Time-Out"]
        case "registeredStudents":
            headers = ["ID", "First Name", "Last Name", "Batch", "Sex"]
        case "registeredFaculties":
            headers = ["ID", "First Name", "Last Name", "----", "Sex"]

    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(rows)
    
    close_db_connection()

def close_db_connection():
    con.close()