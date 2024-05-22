#config.py
import sqlite3

class Config:

    def __init__(self) -> None:
        self.con = sqlite3.connect('web/database/config/program config.db')
        self.cursor = self.con.cursor()
        self.create_config_table()

    def create_config_table(self):
        """Create configurations table"""

        self.cursor.execute("CREATE TABLE IF NOT EXISTS configs\
                            (setting_name TEXT NOT NULL, \
                            setting_value TEXT NOT NULL)")
        
        self.con.commit()

    def add_setting(self, name, value):
        """Adds a setting"""

        self.cursor.execute("INSERT INTO configs \
                            (setting_name, setting_value)\
                            VALUES (?,?)", (name, value))
        self.con.commit()

    def get_value(self, name):
        """Gets a Value of a Setting"""

        setting = self.cursor.execute("SELECT setting_value FROM configs\
                                      WHERE setting_name = ?", (name,)).fetchone()
        
        return setting
    
    def update_setting(self, name, new_value):
        """Changes a Setting"""

        self.cursor.execute("UPDATE configs SET setting_value = ? \
                            WHERE setting_name = ?", (new_value, name))
        
        self.con.commit()
    
    def printAll(self):
        settings = self.cursor.execute("SELECT setting_name, setting_value FROM configs").fetchall()

        for setting in settings:
            print(setting)


# Config().update_setting("anti_spam_minutes", 10)

"""
Lists of Settings and their Values:

anti_spam_minutes = 10

"""