
# Prerequisites
import eel 
from prettytable import PrettyTable
import csv
from datetime import datetime, date, timedelta

# QR Scanner Imports
import cv2
import re
from datetime import datetime
from pyzbar.pyzbar import decode
from screeninfo import get_monitors
import threading
import base64
import json

# Database Imports

from web.database.student_database import StudentDatabase as sdb
from web.database.attendance_database import AttendanceDatabase as adb
from web.database.faculty_database import FacultyDatabase as fdb
from web.report.reportmaker import ReportMaker
from web.modules.QSTARemailer import QSTARemailer

report = ReportMaker()

import sys
logfile = open('program_output.txt', 'w')
sys.stdout = logfile
sys.stderr = logfile

# Initializing the Primary Monitor for Sizings and Positionings
primary_monitor = get_monitors()[0]

# Remember last QR code scanned
last_code = ''
# RegisteredStudents()

# FUNCTIONS FOR QR SCANNING
    
def attendance(a):
    status = a[0] #student or teacher or invalid
    code = a[1]
    global last_code

    if status == 'student': # if the user is a student
        student = sdb().get_student_database(studentID=code)

        if student: #if registered
            action = adb().create_attendance(*student,datetime.now())
            update_table(action)

        else: #if not registered
            """Add code here about registration"""
            last_code = code
            not_registered()


    elif status == 'faculty': #if the user is a faculty
        faculty = fdb().get_faculty_database(facultyID=code)

        if faculty: #if registered
            action = adb().create_attendance(*faculty, datetime.now())
            update_table(action)
        
        else: #if not registered
            """Add code here about registration"""
            last_code = code
            not_registered()

    else:
        invalid_code()

    return #goes back to scanner()

class QRCodeScanner:

    def __init__(self) -> None:
        self.running = False
        self.qr_thread = None
        self.last_scanned_qr = None
        self.timer_thread = None
        self.scan_interval = 10  # Seconds
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #change the value depending on the camera, default webcam i think is 0

    @eel.expose
    def capture_frames(self):
        while True:

            success, img = self.cap.read()
            try:
                _, buffer = cv2.imencode('.jpg', cv2.flip(img, 1))
                frame_bytes = base64.b64encode(buffer)
                eel.updateFrame(frame_bytes.decode('utf-8'))()

                for code in decode(img):
                    decoded_data = code.data.decode("utf-8")

                    if decoded_data and decoded_data != self.last_scanned_qr:
                        self.last_scanned_qr = decoded_data
                        self.start_timer()
                        attendance(verifier(decoded_data)) 

            except Exception:
                continue

    def start_scanning(self):
        if not self.running:
            self.running = True
            self.capture_thread = threading.Thread(target = self.capture_frames)
            self.capture_thread.daemon = True            
            self.capture_thread.start()
    
    def stop_scanning(self):
        if self.running:
            self.running = False
            self.qr_thread.join()

    def start_timer(self):
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.cancel()
        self.timer_thread = threading.Timer(self.scan_interval, self.clear_last_scanned_qr)
        self.timer_thread.start()

    def clear_last_scanned_qr(self):
        self.last_scanned_qr = None

# Initializing a QRCodeScanner Object
scanner = QRCodeScanner()

""" START OF EEL INITIALIZATION """
eel.init("web") 

# QR SCANNER Functions
@eel.expose
def verifier(code):
    student_pattern = re.compile(r'^\d{2}-\d{4}-\d{3}$')
    # faculty_pattern = re.compile(r'^[A-Z0-9]+-\d{2}-\d{4}$')
    faculty_pattern = re.compile(r'^[A-Z0-9]+-[A-Z0-9]+-\d{4}$')

    #remove http if there is
    if code[0:7] == 'http://':
        code = code[7:]

    code = code.strip()

    #checks if it's a student
    student = student_pattern.match(code)
    faculty = faculty_pattern.match(code)
    if student: 
        return 'student', code
    elif faculty:
        return 'faculty', code
    else:
        return 'invalid', code

@eel.expose
def register(studentID, firstName, lastName, batch, sex, position):
    """ Registers a new entry to the student database """
    if position == "student":
        return sdb().update_student_database(studentID, firstName, lastName, batch, sex)
    else:
        return fdb().update_faculty_database(studentID, firstName, lastName, batch, sex)

@eel.expose
def start_scanning_please(): 
    scanner.start_scanning()

@eel.expose
def stop_scanning_please(): 
    scanner.stop_scanning()

# Homepage Functions
def not_registered():
    eel.display_error()

def invalid_code():
    eel.invalid_code()

def update_table(action):
    """ Updates the attendance table in homepage;
        Triggers animation upon attendance action """
    content = convert_htmlTable_today()
    eel.update_table(content)
    if action == "IN":
        eel.animateDivGreen()
    else:
        eel.animateDivRed()

def normalize_time(datetime_str, full=False):
    try:
        format_str = "%Y-%m-%d %H:%M:%S.%f"
        datetime_obj = datetime.strptime(datetime_str, format_str)

        if full:
            return datetime_obj.strftime("%B %d, %Y - %I:%M %p")
        else:
            return datetime_obj.strftime("%I:%M %p")
    except Exception:
        return ""
    


@eel.expose
def add_attendance(id):
    """ Adds attendance to the attendance database """

    student = sdb().get_student_database(studentID=id)
    if student:
        adb().create_attendance(*student, datetime.now())

@eel.expose
def convert_htmlTable_today():
    """ Retrieves the current day attendance and converts it to HTML Table """

    array = adb().getAll_attendance()
    html_table = PrettyTable()
    counter = 1
    yesterday = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")
    today = (date.today()).strftime("%Y-%m-%d")
    if array != "NONE":
        html_table.field_names = ["No.", "Name", "Time-In", "Time-Out"]
        for entry in array:
            if entry[4][:10] == str(today):
                html_table.add_row([counter, f"{entry[0]} {entry[1]}", normalize_time(entry[4]), normalize_time(entry[5]) ])
                counter += 1
        return (html_table.get_html_string())
    else:
        html_table.field_names = ['Seems pretty quite today.']
        return (html_table.get_html_string())

@eel.expose
def convert_htmlTable_filters(lista):
    """ Converts a given (filtered) list into an HTML Table """
    html_table = PrettyTable()
    html_table.field_names = ["No.", "First Name", "Last Name", "Batch", "Sex", "Time-In", "Time-Out"]
    counter = 1
    for entry in lista:
        html_table.add_row([counter, entry[0], entry[1],  entry[2], entry[3], normalize_time(entry[4], True), normalize_time(entry[5], True)])
        counter += 1
    return (html_table.get_html_string())

@eel.expose
def convert_htmlTable_filters_registered(lista):
    """ Converts a given (filtered) list into an HTML Table for REGISTERED"""
    html_table = PrettyTable()
    html_table.field_names = ["No.", "ID No.","First Name", "Last Name", "Batch", "Sex"]
    counter = 1
    for entry in lista:
        html_table.add_row([counter, entry[0], entry[1],  entry[2], entry[3], entry[4]])
        counter += 1
    return (html_table.get_html_string())

@eel.expose
def get_last_code():
    global last_code
    return last_code

def sort_by_third(list_of_lists):
  """ What is this for?? """
  return sorted(list_of_lists, key=lambda x: x[2])

@eel.expose
def clean_data_registered(name=None, batch=None, sex=None, headers=True):
    student_list = sdb().getAll_student_database()
    faculty_list = fdb().getAll_faculty_database()
    file_list = student_list + faculty_list

    try:
         # remove headers
        if not headers:
            file_list.pop(0)

        # to filter NAME
        if name != 'NONE':
            name_filtered = []
            for entry in file_list:
                full_name = entry[1] + " " + entry[2]
                if name.lower() in full_name.lower():
                    name_filtered.append(entry)
            file_list = name_filtered

        # to filter BATCH
        if batch != 'NONE':
            batch_filtered = []
            for entry in file_list:
                if str(entry[3]) == str(batch):
                    batch_filtered.append(entry)
            file_list = batch_filtered

        # to filter SEX
        if sex != 'None':
            sex_filtered = []
            for entry in file_list:
                if entry[4] == sex:
                    sex_filtered.append(entry)
            file_list = sex_filtered
    

        return sort_by_third(file_list) # sort_by_third sorts the data by the last name

    except Exception as error:
        with open("web/report/processed_data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        data['Registered_Clean_Error'] = error

        with open("web/report/processed_data.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)

        return []

def update_json(processed_list, category):
    # to handle the error associated with empty json file
    try:
        with open("web/report/processed_data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        data[category] = processed_list
        
        with open("web/report/processed_data.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
    except:
        with open("web/report/processed_data.json", "w") as jsonFile:
            json.dump({}, jsonFile, indent=4)

@eel.expose
def clean_data2(start_date=None, end_date=None, name=None, batch=None, sex=None, headers=True):
    """ Cleans the attendance data according to the set parameters """
    file_list = adb().getAll_attendance()
        
    try:
        # remove headers
        if not headers:
            file_list.pop(0)

        # to filter NAME
        if name != 'NONE':
            name_filtered = []
            for entry in file_list:
                full_name = entry[0] + " " + entry[1]
                if name.lower() in full_name.lower():
                    name_filtered.append(entry)
            file_list = name_filtered

        # to filter BATCH
        if batch != 'NONE':
            batch_filtered = []
            for entry in file_list:
                if str(entry[2]) == str(batch):
                    batch_filtered.append(entry)
            file_list = batch_filtered

        # to filter SEX
        if sex != 'None':
            sex_filtered = []
            for entry in file_list:
                if entry[3] == sex:
                    sex_filtered.append(entry)
            file_list = sex_filtered


        # to filter DATE
        if start_date != 'NONE' and end_date != 'NONE': # If start and end dates are specified
            date_filtered = []
            for entry in file_list:
                if entry[-2][:10] >= start_date and entry[-1][:10] <= end_date:
                    date_filtered.append(entry)
            file_list = date_filtered

        elif start_date != 'NONE' and end_date == 'NONE': # if start date is only specified
            date_filtered = []
            for entry in file_list:
                if entry[-2] >= start_date:
                    date_filtered.append(entry)

            file_list = date_filtered

        elif start_date == "NONE" and end_date != "NONE": # if end date is only specified
            date_filtered = []
            for entry in file_list:
                if entry[-1] <= end_date:
                    date_filtered.append(entry)
            file_list = date_filtered

        if len(file_list) != 0:
            update_json([start_date, end_date], 'time_range')
            return file_list
        else:
            update_json([start_date, end_date], 'time_range')
            return []
    except Exception:
        update_json([start_date, end_date], 'time_range')
        return []

@eel.expose
def visitsVStime(listahan):
    """ Prepares the needed input for ChartJS LineChart, according to the filtered data -> list """
    output = [] # [[independent/simplified date], [dependent/frequency], [complete date]]

    dates_complete = []
    independent = []

    for entry in listahan:
        dates_complete.append(entry[4][:10])
    
    # counting frequency each date using complete dates
    dates_count = {i:dates_complete.count(i) for i in dates_complete}
    dates_count = dict(sorted(dates_count.items()))

    # transforming unique complete dates to simplified dates
    unique_dates = list(dates_count.keys())
    for _ in unique_dates:
        independent.append((datetime.strptime(_, "%Y-%m-%d")).strftime("%b. %d"))

    # getting frequency for each date
    dependent = list(dates_count.values())
    
    output.append(independent)
    output.append(dependent)
    output.append(unique_dates)

    try:
        avg_visits_perDay = round(sum(dependent)/len(independent),2)
        output.append(avg_visits_perDay)
    except Exception:
        output.append('0')

    total_visits = sum(dependent)
    if total_visits == 0:
        output.append('0')
    else:
        output.append(total_visits)
    
    update_json(output, "visitsTime")
    return output

@eel.expose
def visitsVSbatch(listahan):
    """ Prepares the needed input for ChartJS BarChart, according to the filtered data -> list """
    output = [] # [[independent], [dependent]]
    visits = []
    for entry in listahan:
        visits.append(entry[2])
    
    batch_count = {i:visits.count(i) for i in visits}

    batches = [str(x) for x in batch_count.keys()]
    
    output.append(batches)
    output.append(list(batch_count.values()))

    update_json(output, "visitsBatch")
    return output

@eel.expose
def average_time(listahan):
    """ Calculates the average time of visits """
    date_format = "%Y-%m-%d %H:%M"
    duration_count = 0
    for entry in listahan:
        time_in = datetime.strptime(entry[4][:16], date_format)
        time_out = datetime.strptime(entry[5][:16], date_format)
        duration = (time_out - time_in).total_seconds()
        duration_count += duration
    try:
        average_time = round(((duration_count/(len(listahan)))/60)/60,2)
        update_json(average_time, "average_time")
        return str(average_time)
    except Exception:
        update_json([0], "average_time")
        return "0"

@eel.expose    
def gad_stats2(listahan):
    """ Calculates the basic GAD statistics """
    female_count = 0
    not_female_count = 0
    for entry in listahan:
        if entry[3] == 'Female':
            female_count+=1
        else:
            not_female_count+=1
    length = len(listahan)
    try:
        update_json([female_count, not_female_count, length], "GAD")
        return [str(female_count), str(not_female_count), length]
    except Exception:
        return ["0", "0"]

@eel.expose
def rank_students(listahan):
    """ Prepares the needed input for ChartJS BarChart, according to the filtered data -> list """
    output = [] # [[independent], [dependent]]
    people = []
    for person in listahan:
        full_name = person[0] + " " + person[1]
        people.append(full_name)

    ppl_count = {i:people.count(i) for i in people}

    sorted_dict = dict(sorted(ppl_count.items(), key=lambda item: item[1], reverse=True))
    first_five = dict(list(sorted_dict.items())[:5])
    output.append(list(first_five.keys()))
    output.append(list(first_five.values()))
    update_json(output, 'rankstudents')
    return output

@eel.expose
def create_report(receiver):
    report.create_report()
    subject = "QSTAR Report"
    body = """
    Greetings!

    This is QSTAR Reporter and I bring you the library report.

    See attached file for the report.

    See ya,
    QSTAR Reporter
    """

    emailer = QSTARemailer()
    emailer.send_email(filepath='web/report/QSTAR-Report.pdf', send_to=receiver, subject=subject, body=body)

adb().auto_timeOut()
eel.start("homepage.html")