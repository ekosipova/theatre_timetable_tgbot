import sqlite3
import parse

connection = sqlite3.connect('bolshoi_theatre.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Timetable (
        data TEXT,
        name TEXT,
        time TEXT,
        stage INTEGER,
        info TEXT)''')

database = parse.timetable

connection.commit()