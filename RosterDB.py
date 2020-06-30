import sqlite3
import json

conn = sqlite3.connect('rosterdb.sqlite')
cur  = conn.cursor()

cur.executescript('''DROP TABLE IF EXISTS User;
                  DROP TABLE IF EXISTS Course;
                  DROP TABLE IF EXISTS Role;

                  CREATE TABLE User(
                  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  name TEXT UNIQUE);

                  CREATE TABLE Course(
                  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  title TEXT UNIQUE);

                  CREATE TABLE Member(
                  user_id INTEGER,
                  course_id INTEGER,
                  role INTEGER,
                  PRIMARY KEY(user_id, course_id)
                  )''')

fname = input('Enter File Name to be read:')
if len(fname) < 1:  fname = 'roster_data.json'
fh = open(fname, 'r')
strdata = fh.read()

json = json.loads(strdata)

for entry in json:

    name = entry[0];
    title = entry[1];

    print((name, title))

    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (entry[0],))
    cur.execute('SELECT id FROM User WHERE name = ?', (entry[0],))
    user_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (entry[1],))
    cur.execute('SELECT id FROM Course WHERE title = ?', (entry[1],))
    course_id = cur.fetchone()[0]
    cur.execute('INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?,?,?)', (user_id,course_id, entry[2]))

    conn.commit()
