import sqlite3


SCHEMA = """create table jobs (
id integer primary key autoincrement,
name string not null,
script string not null
);"""


def connect_db(url):
    return sqlite3.connect(url)


def init_db(url):
    from contextlib import closing

    with closing(connect_db(url)) as db:
        db.cursor().executescript(SCHEMA)
        db.commit()
