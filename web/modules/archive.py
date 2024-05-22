import sqlite3

source = 'web/database/main database.db'
archive = 'web/database/archive database.db'
con_source = sqlite3.connect(source)
cursor_source = con_source.cursor()

con_archive = sqlite3.connect(archive)
cursor_archive = con_archive.cursor()

def archiveAttendance():
    cursor_archive.execute("CREATE TABLE IF NOT EXISTS attendance\
                            (id VARCHAR(20), \
                            firstName TEXT NOT NULL, \
                            lastName TEXT NOT NULL, \
                            batch INTEGER NOT NULL, \
                            sex VARCHAR(10), \
                            time_in VARCHAR(50), \
                            time_out VARCHAR(50))")
    
    rows = cursor_source.execute('SELECT * FROM attendance').fetchall()
    for row in rows:
        cursor_archive.execute('INSERT INTO attendance \
                              (id, firstName, lastName, batch, sex, time_in, time_out) \
                               VALUES (?,?,?,?,?,?,?)', row)
    
    # cursor_source.execute('ATTACH DATABASE ? AS source_db', (source,))
    # cursor_archive.execute('ATTACH DATABASE ? AS archive_db', (archive,))
    # cursor_archive.execute('INSERT INTO archive_db.attendance SELECT * \
    #                        FROM source_db.attendance')

    con_archive.commit()
    con_archive.close()
    con_source.close()

archiveAttendance()