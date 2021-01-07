import sqlite3
from datetime import datetime

db_file = "fruit_for_blogs.db"
text_factory = str

def setup():
    db = sqlite3.connect(db_file)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS blogs (user TEXT NOT NULL, blog TEXT NOT NULL)")
    db.commit()
    db.close()

def entry_exists(entry, table, n):
    db = sqlite3.connect(db_file)
    db.text_factory = text_factory
    c = db.cursor()
    exist = False
    for row in c.execute("SELECT * FROM " + table):
        exist = exist or (entry == row[n])
    db.close()
    return exist

def check_credentials(username, password):
    db = sqlite3.connect(db_file)
    db.text_factory = text_factory
    c = db.cursor()
    exist = False
    for row in c.execute("SELECT * FROM users"):
        exist = exist or (username == row[0] and password == row[1])
    db.close()
    return exist

def register_user(username, password, title, description):
    db = sqlite3.connect(db_file)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("INSERT INTO users VALUES ('" + username + "' ,'" + password + "')")
    c.execute("INSERT INTO blogs VALUES ('" + username + "' ,'" + title + "')")
    c.execute("CREATE TABLE " + username + "_" + title +  " (title TEXT, body TEXT, time TEXT)")
    c.execute("INSERT INTO " + username + "_" + title + " VALUES ('" + title + "' ,'" + description + "' ,'" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "')")
    db.commit()
    db.close()

def return_blogs(username):
    db = sqlite3.connect(db_file)
    db.text_factory = text_factory
    c = db.cursor()
    return c.execute("SELECT * FROM blogs WHERE user = '" + username + "'")

def return_blog_information(blog):
    db = sqlite3.connect(db_file)
    db.text_factory = text_factory
    c = db.cursor()
    info = []
    i = 0
    for row in c.execute("SELECT * FROM " + blog):
        if(i == 0):
            info.append(row[0])
            info.append(row[1])
            info.append(row[2])
        else:
            info.append(row)
        i += 1
    return info


def display(table):
    db = sqlite3.connect(db_file)
    db.text_factory = text_factory
    c = db.cursor()
    return c.execute("SELECT * FROM " + table)
    db.close()