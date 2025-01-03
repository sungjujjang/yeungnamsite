from flask import Flask # type: ignore
from flask import request, jsonify, Response, render_template, redirect, url_for , session # type: ignore
import db.module_db as module_db
import config.settings as settings
import sqlite3, datetime
import modules.date as date

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
    if session.get('id'):
        return redirect(url_for('home'))
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

@app.route('/register', methods=['GET'])
def register_page():
    if session.get('id'):
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/apiweb/checkgung', methods=['POST'])
def checkgung():
    params = request.get_json()
    _id = params['id']
    print(type(_id), _id)
    if module_db.checkgung(_id):
        return jsonify(message="사용 불가능한 아이디 입니다. 이미 사용 중 입니다.")
    else:
        return jsonify(message ="사용 가능한 아이디 입니다.")

@app.route('/apiweb/register', methods=['POST'])
def register():
    if session.get('id'):
        return redirect(url_for('home'))
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    passwordconfirm = request.form['confirmPassword']
    try:
        email = request.form['email']
    except:
        email = "no"
    try:
        tel = request.form['tel']
    except:
        tel = "no"
    if password != passwordconfirm:
        return """<script>alert("비밀번호가 일치하지 않습니다");location.href="/register";</script>"""
    else:
        try:
            data = module_db.insert_user(username, password, name, email, tel)
        except:
            return """<script>alert("이미 있는 아이디입니다.");location.href="/register";</script>"""
        else:
            session['id'] = username
            td = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            module_db.insert_log(username, "register", td)
            module_db.insert_iplog(username, request.remote_addr, td)
            return """<script>alert("가입에 성공했습니다. 축하합니다!");location.href="/";</script>"""
    
@app.route('/introduction')
def introduction_page():
    return render_template('introduction.html')

@app.route('/admin')
def admin_page():
    if session.get('id') is None:
        return redirect(url_for('home'))
    if not module_db.check_admin(session['id']):
        return redirect(url_for('home'))
    logs = module_db.getip_all_logs()
    # print(logs)
    return render_template('admin.html', logs=logs)

@app.route('/admin/post')
def admin_post_page():
    if session.get('id') is None:
        return redirect(url_for('home'))
    if not module_db.check_admin(session['id']):
        return redirect(url_for('home'))
    return render_template('admin_post.html')

@app.route('/webapi/add/notice', methods=['POST'])
def webapi_notice():
    if session.get('id') is None:
        return redirect(url_for('home'))
    if not module_db.check_admin(session['id']):
        return redirect(url_for('home'))
    data = request.form
    title = data['title']
    content = data['content']
    td = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    module_db.insert_notice(title, content, td, session['id'])
    return """<script>alert("공지사항이 등록되었습니다.");location.href="/";</script>"""

@app.route('/notice')
def notice_page():
    # get query page
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    all_notices = module_db.get_all_notices()
    notices = all_notices[(page-1)*10:page*10]
    o_lenpage = int(len(all_notices) / 10 + 1)
    lenpage = range(1, o_lenpage+1)
    if o_lenpage > 6:
        if page < 4:
            r_lenpage = lenpage[:6]
        else:
            r_lenpage = lenpage[int(page)-3:int(page)+3]
    else:
        r_lenpage = lenpage
    print(lenpage)
    if module_db.check_admin(session.get('id')):
        return render_template('notice.html', notices=notices, lenpage=r_lenpage, page=page, admin=True)
    else:
        return render_template('notice.html', notices=notices, lenpage=r_lenpage, page=page, admin=False)

@app.route('/post', methods=['GET'])
def post_page():
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    all_posts = module_db.get_all_posts()
    posts = all_posts[(page-1)*10:page*10]
    o_lenpage = int(len(all_posts) / 10 + 1)
    print(o_lenpage)
    lenpage = range(1, o_lenpage+1)
    if o_lenpage > 6:
        if page < 4:
            r_lenpage = lenpage[:6]
        else:
            r_lenpage = lenpage[int(page)-3:int(page)+3]
    else:
        r_lenpage = lenpage
    print(lenpage)
    if session.get('id'):
        username = session['id']
        if module_db.check_admin(session['id']):
            admin = True
        else:
            admin = False
    else:
        admin = False
        username = '.'.join(request.remote_addr.split('.')[2:4])
    return render_template('post.html', posts=posts, lenpage=r_lenpage, page=page, username=username, admin=admin)

@app.route('/post/<int:id>')
def post_detail(id):
    post = module_db.select_post(id)
    post = list(post)
    post[2] = post[2].split('\n')
    comments = module_db.select_comment_post(id)
    try:
        lencom = len(comments)
    except:
        lencom = 0
    if comments is None:
        comments = []
    datetext = date.make_date_text(date.date_sliser(post[3]))
    module_db.add_post_view(id)
    for i in range(len(comments)):
        comments[i] = list(comments[i])
        comments[i][2] = date.make_date_text(date.date_sliser(comments[i][2]))
    return render_template('post_detail.html', post=post, comments=comments, lencom=lencom, datetext=datetext)

@app.route('/apiweb/post/commit', methods=['POST'])
def post_commit():
    if session.get('id'):
        id = session['id']
    else:
        id = '.'.join(request.remote_addr.split('.')[2:4])
    data = request.get_json()
    comment = data['comment']
    postid = data['postid']
    td = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    module_db.insert_comment_post(comment, td, id, postid)
    return jsonify(message="댓글이 등록되었습니다.")

@app.route('/notice/<int:id>')
def notice_detail(id):
    notice = module_db.select_notice(id)
    notice = list(notice)
    notice[2] = notice[2].split('\n')
    comments = module_db.select_comment(id)
    try:
        lencom = len(comments)
    except:
        lencom = 0
    if comments is None:
        comments = []
    datetext = date.make_date_text(date.date_sliser(notice[3]))
    module_db.add_notice_view(id)
    for i in range(len(comments)):
        comments[i] = list(comments[i])
        comments[i][2] = date.make_date_text(date.date_sliser(comments[i][2]))
    return render_template('notice_detail.html', notice=notice, comments=comments, lencom=lencom, datetext=datetext)

@app.route('/apiweb/notice/commit', methods=['POST'])
def notice_commit():
    if session.get('id'):
        id = session['id']
    else:
        id = '.'.join(request.remote_addr.split('.')[2:4])
    data = request.get_json()
    comment = data['comment']
    noticeid = data['noticeid']
    td = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    module_db.insert_comment(comment, td, id, noticeid)
    return jsonify(message="댓글이 등록되었습니다.")

# session['uplist']
@app.route('/apiweb/post_up/<int:id>', methods=['GET'])
def post_up(id):
    if session.get('uplist') is None:
        session['uplist'] = []
    if id in session['uplist']:
        return f'<script>alert("이미 개추하셨습니다.");location.href="/post/{id}";</script>'
    else:
        session['uplist'].append(id)
        session.modified = True
        module_db.up_post(id)
        return f'<script>alert("개추했습니다.");location.href="/post/{id}";</script>'

# session['downlist']
@app.route('/apiweb/post_down/<int:id>', methods=['GET'])
def post_down(id):
    if session.get('downlist') is None:
        session['downlist'] = []
    if id in session['downlist']:
        return f'<script>alert("이미 비추를 눌렀습니다.");location.href="/post/{id}";</script>'
    else:
        session['downlist'].append(id)
        session.modified = True
        module_db.down_post(id)
        return f'<script>alert("비추되었습니다.");location.href="/post/{id}";</script>'
    
@app.route('/post/add', methods=['GET'])
def post_add_page():
    return render_template('add_post.html')

@app.route('/apiweb/post/delete/<int:id>', methods=['GET'])
def post_delete(id):
    if session.get('id') is None:
        pid = '.'.join(request.remote_addr.split('.')[2:4])
    else:
        pid = session['id']
    post = module_db.select_post(id)
    print(post)
    if post[4] != pid:
        if module_db.check_admin(pid):
            pass
        else:
            return """<script>alert("작성자만 삭제할 수 있습니다.");location.href="/post";</script>"""
    module_db.delete_post(id)
    return """<script>alert("게시글이 삭제되었습니다.");location.href="/post";</script>"""

@app.route('/post/edit/<int:id>', methods=['GET'])
def post_edit_page(id):
    post = module_db.select_post(id)
    if session.get('id') is None:
        pid = '.'.join(request.remote_addr.split('.')[2:4])
    else:
        pid = session['id']
    if post[4] != pid:
        if module_db.check_admin(pid):
            pass
        else:
            return """<script>alert("작성자만 수정할 수 있습니다.");location.href="/post";</script>"""
    return render_template('edit_post.html', post=post)

@app.route('/apiweb/post/edit', methods=['POST'])
def edit_post():
    data = request.form
    pid = data['id']
    post = module_db.select_post(pid)
    if session.get('id') is None:
        id = '.'.join(request.remote_addr.split('.')[2:4])
    else:
        id = session['id']
    if post[4] != id:
        if module_db.check_admin(id):
            pass
        else:
            return """<script>alert("작성자만 수정할 수 있습니다.");location.href="/post";</script>"""
    title = data['title']
    content = data['content']
    module_db.edit_post(pid, title, content)
    return """<script>alert("게시글이 수정되었습니다.");location.href="/post";</script>"""

@app.route('/apiweb/post/add', methods=['POST'])
def post_add():
    if session.get('id') is None:
        id = '.'.join(request.remote_addr.split('.')[2:4])
    else:
        id = session['id']
    data = request.form
    title = data['title']
    content = data['content']
    td = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    module_db.insert_post(title, content, td, id)
    return """<script>alert("게시글이 등록되었습니다.");location.href="/post";</script>"""
        
@app.route('/apiweb/notice/delete/<int:id>', methods=['GET'])
def notice_delete(id):
    if session.get('id') is None:
        return redirect(url_for('home'))
    if not module_db.check_admin(session['id']):
        return redirect(url_for('home'))
    module_db.delete_notice(id)
    return """<script>alert("공지사항이 삭제되었습니다.");location.href="/notice";</script>"""
    

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80, debug=True)