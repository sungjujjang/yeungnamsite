import sqlite3

import sys
sys.path.append("..")
import config.settings as settings
sys.path.append("../..")

def create_table():
    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE user
                        (id text PRIMARY KEY, password text, name text, email text, phone text, admin integer)''') # admin: 0 - 일반 사용자, 1 - 관리자
    cursor.execute('''CREATE TABLE notice
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, content text, date text, writerid text, views integer)''')
    cursor.execute('''CREATE TABLE post
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, content text, date text, writerid text, up integer, down integer, views integer)''')
    cursor.execute('''CREATE TABLE comment 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, content text, date text, writerid text, postid integer)''')
    cursor.execute('''CREATE TABLE iplogs
                        (userid text, ip text, date text)''')
    cursor.execute('''CREATE TABLE logs
                        (userid text, date text, action text)''')
    # all date is in format 'YYYYMMDDHHMMSS'
    conn.commit()
    conn.close()

def insert_admin():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    adminid = settings.admin_id
    adminpw = settings.admin_pw
    cursor.execute("INSERT INTO user VALUES (?, ?, '관리자', 'no', 'no', 1)", (adminid, adminpw))
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    create_table()
    insert_admin()