import sqlite3
import datetime
import sys
sys.path.append("..")
import config.settings as settings
sys.path.append("../..")

db_path = settings.db_path

def insert_user(id, password, name, email, phone, admin=False):
    admin = 1 if admin else 0
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", (id, password, name, email, phone, admin))
    try:
        cursor.execute("SELECT * FROM user WHERE id=? AND password=? AND name=? AND email=? AND phone=? AND admin=?", (id, password, name, email, phone, admin))
        result = cursor.fetchone()
    except:
        result = None
    conn.commit()
    conn.close()
    return result

def select_user(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id=?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def insert_notice(title, content, date, writerid):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notice VALUES (NULL, ?, ?, ?, ?, 0)", (title, content, date, writerid))
    try:
        cursor.execute("SELECT * FROM notice WHERE title=? AND content=? AND date=? AND writerid=?", (title, content, date, writerid))
        result = cursor.fetchone()
    except:
        result = None
    conn.commit()
    conn.close()
    return result

def select_notice(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notice WHERE id=?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_notices(number):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM notice ORDER BY id DESC LIMIT ?", (number,))
    result = cur.fetchall()
    con.close()
    return result

def insert_post(title, content, date, writerid):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO post VALUES (NULL, ?, ?, ?, ?, 0, 0, 0)", (title, content, date, writerid))
    try:
        cursor.execute("SELECT * FROM post WHERE title=? AND content=? AND date=? AND writerid=?", (title, content, date, writerid))
        result = cursor.fetchone()
    except:
        result = None
    conn.commit()
    conn.close()
    return result

def select_post(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post WHERE id=?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_posts(number):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM post ORDER BY id DESC LIMIT ?", (number,))
    result = cur.fetchall()
    con.close()
    return result

def get_up_posts(number, date): # 숫자, date 이후의 up 높은 순서대로
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM post WHERE (cast(date as integer) > ?) ORDER BY up DESC LIMIT ? ", (date, number))
    result = cur.fetchall()
    con.close()
    return result

def insert_comment(content, date, writerid, postid):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comment VALUES (NULL, ?, ?, ?, ?)", (content, date, writerid, postid))
    try:
        cursor.execute("SELECT * FROM comment WHERE content=? AND date=? AND writerid=? AND postid=?", (content, date, writerid, postid))
        result = cursor.fetchone()
    except:
        result = None
    conn.commit()
    conn.close()
    return result

def select_comment(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comment WHERE postid=?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_logs(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE userid=?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_ips(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM iplogs WHERE userid=?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result



