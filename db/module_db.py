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

def edit_post(id, title, content):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE post SET title=?, content=? WHERE id=?", (title, content, id))
    conn.commit()
    conn.close()

def delete_post(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM post WHERE id=?", (id,))
    conn.commit()
    conn.close()

def up_post(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE post SET up=up+1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
def down_post(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE post SET down=down+1 WHERE id=?", (id,))
    conn.commit()
    conn.close()

def select_comment_post(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comment WHERE postid=? ORDER BY id DESC", (id,))
    result = cursor.fetchall()
    conn.close()
    return result

def insert_comment_post(content, date, writerid, postid):
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

def check_admin(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id=?", (id,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    if result[5] == 1:
        return True
    else:
        return False

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

def get_all_notices():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM notice ORDER BY id DESC")
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

def add_post_view(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE post SET views=views+1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
def add_notice_view(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE notice SET views=views+1 WHERE id=?", (id,))
    conn.commit()
    conn.close()

def delete_notice(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notice WHERE id=?", (id,))
    conn.commit()
    conn.close()

def select_comment(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # date 순으로 정렬
    cursor.execute("SELECT * FROM comment WHERE postid=? ORDER BY id DESC", (id,))
    result = cursor.fetchall()
    conn.close()
    return result

def insert_iplog(userid, ip, date):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO iplogs VALUES (?, ?, ?)", (userid, ip, date))
    try:
        cursor.execute("SELECT * FROM iplogs WHERE userid=? AND ip=? AND date=?", (userid, ip, date))
        result = cursor.fetchone()
    except:
        result = None
    conn.commit()
    conn.close()
    return result

def insert_log(userid, action, date):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs VALUES (?, ?, ?)", (userid, date, action))
    try:
        cursor.execute("SELECT * FROM logs WHERE userid=? AND date=? AND action=?", (userid, date, action))
        result = cursor.fetchone()
    except:
        result = None
    conn.commit()
    conn.close()
    return result

def checkgung(userid):
    print(userid)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id=?", (userid,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False

def get_logs(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE userid=?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_logs():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_posts():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post ORDER BY id DESC")
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

def getip_all_logs():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM iplogs")
    result = cursor.fetchall()
    conn.close()
    return result



