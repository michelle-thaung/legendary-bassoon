USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY, 
        password TEXT NOT NULL
    )
"""

BLOGS_TABLE = """
    CREATE TABLE IF NOT EXISTS blogs (
        blogId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user TEXT NOT NULL, 
        name TEXT NOT NULL, 
        description TEXT NOT NULL, 
        time TEXT NOT NULL
    )
"""

ENTRIES_TABLE = """
    CREATE TABLE IF NOT EXISTS entries (  
        entryId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        body TEXT NOT NULL,
        time TEXT NOT NULL,
        ofBlog INTEGER, 
        FOREIGN KEY (ofBlog) REFERENCES blogs (blogId)
    )
"""