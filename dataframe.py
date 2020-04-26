import json
import sqlite3

conn = sqlite3.connect('dbmedia.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Time;
DROP TABLE IF EXISTS Source;
DROP TABLE IF EXISTS News;

CREATE TABLE Time (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    time_created TEXT UNIQUE 
);

CREATE TABLE Source (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT,
    time_id INTEGER 
);

CREATE TABLE News (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    content TEXT  UNIQUE,
    url TEXT UNIQUE,
    time_id  INTEGER,
    source_id INTEGER
)
''')

str_data = open('gb.json').read()
json_data = json.loads(str_data)
if json_data['status'] != 'ok':
    raise AssertionError

for entry in json_data['articles']:

    source = entry['source']['name']
    title = entry['title']
    url = entry['url']
    content = entry['content']
    time = entry['publishedAt']

    print((source, title, url, content, time))

    cur.execute('''INSERT OR IGNORE INTO Time (time_created)
           VALUES ( ? )''', (time,))
    cur.execute('SELECT id FROM Time WHERE time_created = ? ', (time,))
    time_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Source (name)
               VALUES ( ? )''', (source,))
    cur.execute('SELECT id FROM Source WHERE name = ? ', (source,))
    source_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO News (title, content)
               VALUES ( ?, ? )''', (title, content))

