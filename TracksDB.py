import sqlite3
import xml.etree.ElementTree as ET

fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'

tree = ET.parse(fname)

conn = sqlite3.connect('tracksdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Track' )
cur.execute('DROP TABLE IF EXISTS Genre')
cur.execute('DROP TABLE IF EXISTS Artist')
cur.execute('DROP TABLE IF EXISTS Album')

cur.execute('''CREATE TABLE Track(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT UNIQUE,
album_id INTEGER,
artist_id INTEGER,
genre_id INTEGER,
len INTEGER,
rating INTEGER,
count INTEGER
)''')
cur.execute(''' CREATE TABLE Genre(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT UNIQUE
)''')

cur.execute(''' CREATE TABLE Artist(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT UNIQUE
)''')

cur.execute('''CREATE TABLE Album(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT UNIQUE,
artist_id INTEGER
) ''')

def lookup(d , key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

all = tree.findall('dict/dict/dict')
print('Dict Count:', len(all))

for stuff in all:
    if (lookup(stuff, 'Track ID') is None): continue


    artist_name = lookup(stuff, 'Artist')
    album_name = lookup(stuff, 'Album')
    genre_name = lookup(stuff, 'Genre')
    track_name = lookup(stuff, 'Name')
    length = lookup(stuff, 'Total Time')
    rating = lookup(stuff, 'Rating')
    count  = lookup(stuff, 'Play Count')

    if track_name is None or artist_name is None or album_name is None or genre_name is None: continue

    print(track_name, album_name, artist_name, genre_name)


    cur.execute(''' INSERT OR IGNORE INTO Artist (name)
    VALUES (?)''', (artist_name,))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist_name,))
    artist_id = cur.fetchone()[0]

    cur.execute(''' INSERT OR IGNORE INTO Album (title , artist_id)
    VALUES (?,?)''', (album_name, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album_name,))
    album_id = cur.fetchone()[0]


    cur.execute(''' INSERT OR IGNORE INTO Genre (name)
    VALUES (?)''', (genre_name,))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre_name,))
    genre_id = cur.fetchone()[0]

    track_name = lookup(stuff, 'Name')
    length = lookup(stuff, 'Total Time')
    rating = lookup(stuff, 'Rating')
    count  = lookup(stuff, 'Play Count')



    cur.execute(''' INSERT OR REPLACE INTO Track (title, album_id, artist_id, genre_id, len, rating, count)
    VALUES (?,?,?,?,?,?,?)''', (track_name, album_id, artist_id, genre_id, length, rating, count ))

# For Testing

sqlstr = '''SELECT Track.title, Artist.name, Album.title, Genre.name
FROM Track JOIN Genre JOIN Album JOIN Artist
ON Track.genre_id = Genre.id and Track.album_id = Album.id
AND Album.artist_id = Artist.id
ORDER BY Artist.name LIMIT 3'''

for row in cur.execute(sqlstr):
    print(row)


conn.commit()
cur.close()
