import sqlite3
from datetime import datetime

from constants import *

class DbInstance:

    def __init__(self, file):
        self.db = sqlite3.connect(file)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def __del__(self):
        self.close()

class Database:

    def __init__(self, file):
        self.file = file
        self.setup()

    def get_instance(self):
        return DbInstance(self.file)

    def setup(self):
        instance = self.get_instance()
        instance.cursor.execute(USERS_TABLE)
        instance.cursor.execute(BLOGS_TABLE)
        instance.cursor.execute(ENTRIES_TABLE)
        instance.db.commit()

    def has_username(self, username):
        instance = self.get_instance()
        data = instance.cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,)).fetchone()
        exist = data[0] != 0
        return exist

    def check_credentials(self, username, password):
        instance = self.get_instance()
        exist = False
        for row in instance.cursor.execute("SELECT * FROM users"):
            exist = exist or (username == row[0] and password == row[1])
        return exist

    def register_user(self, username, password, title, description):
        instance = self.get_instance()
        c = instance.cursor
        db = instance.db
        current = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        c.execute("INSERT INTO blogs (user, name, description, time) VALUES (?, ?, ?, ?)", (username, title, description, current))
        ofBlog = c.execute("SELECT MAX(blogId) FROM blogs").fetchone()[0]
        c.execute("INSERT INTO entries (body, time, ofBlog) VALUES (?, ? , ?)", ("Hello World", current, ofBlog))
        db.commit()

    def get_blogs(self, username):
        instance = self.get_instance()
        tmp = list(instance.cursor.execute("SELECT blogId, name FROM blogs WHERE user=?", (username,)))
        return tmp

    def get_blog(self, blogID):
        instance = self.get_instance()
        raw_blog = list(instance.cursor.execute("SELECT * FROM blogs WHERE blogId=?", (blogID,)))[0]
        blog = {
            "title": raw_blog[2],
            "author": raw_blog[1],
            "description": raw_blog[3],
            "time": raw_blog[4],
            "entries": [],
            "id": blogID
        }
        entries = instance.cursor.execute("SELECT * FROM entries WHERE ofBlog=?", (blogID,))
        for entry in entries:
            blog['entries'].append(entry)
        return blog

    def insert_entry(self, input, ofBlog):
        instance = self.get_instance()
        db = instance.db
        instance.cursor.execute("INSERT into entries (body, time, ofBlog) VALUES (?, ?, ?)", (input, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ofBlog))
        db.commit()

    def display(self, table):
        instance = self.get_instance()
        out = list(instance.cursor.execute("SELECT * FROM " + table))
        return out