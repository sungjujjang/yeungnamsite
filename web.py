from flask import Flask # type: ignore
from flask import request, jsonify, Response, render_template, redirect, url_for , session # type: ignore
import db.module_db as module_db
import config.settings as settings
import sqlite3, datetime

def start_db():
    con = sqlite3.connect(settings.db_path)
    cur = con.cursor()    
    return con, cur

app = Flask(__name__)
app.secret_key = "Sungjujjang0702!!"

@app.route('/')
def home():
    if session.get('id') is None:
        lg = False
        id = ""
    else:
        lg = True
        id = session['id']
    notices = module_db.get_notices(10)
    datelast1week = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y%m%d%H%M%S')
    upposts = module_db.get_up_posts(10, int(datelast1week))
    print(upposts, notices)
    ip = request.remote_addr
    return render_template('index.html', notices=notices, upposts=upposts, lg=lg, id=id, ip=ip)

@app.route('/apiweb/login', methods=['POST'])
def login():
    print(request.form)
    id = request.form['id']
    password = request.form['pw']
    print(id, password)
    user = module_db.select_user(id)
    if user is None:
        return """<script>alert("No such user");location.href="/";</script>"""
    if user[1] != password:
        return """<script>alert("Wrong password");location.href="/";</script>"""
    td = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    module_db.insert_log(id, "login", td)
    module_db.insert_iplog(id, request.remote_addr, td)
    session['id'] = id
    return redirect(url_for('home'))

@app.route('/apiweb/logout', methods=['POST', 'GET'])
def logout():
    td = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    module_db.insert_iplog(session['id'], request.remote_addr, td)
    module_db.insert_log(session['id'], "logout", td)
    session.pop('id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)