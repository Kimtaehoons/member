import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "KIMTAEHOON" #세션에 따른 암호키 설정

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/') #127.0.0.1:/5000
def index():
    if 'userID' in session: #session에 userID가 존재하면(로그인 현상 유지 확인을 위해 로그인 id보이게 하기)
        ssid = session.get('userID') #session을 가져와서
        return render_template('index.html', ssid=ssid) #index페이지로 보내준다(navbar연동 포함)
    else:
        return render_template('index.html') #GET방식으로 session이 없으면 index페이지로

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall() #db에서 검색한 데이터
    conn.close()
    if 'userID' in session:
        ssid = session.get('userID')
        return render_template('memberlist.html', ssid=ssid, rs=rs)
    else:
        return render_template('memberlist.html') #가져온 데이터를 웹으로 보내줌

@app.route('/member_view/<string:id>/')
def member_view(id): #mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    if 'userID' in session:
        ssid = session.get('userID')
        return render_template('member_view.html', ssid=ssid, rs=rs)
    else:
        return render_template('member_view.html')

@app.route('/register/', methods = ['GET', 'POST']) #url경로
def register():
    if request.method == 'POST': #POST방식(자료를 받아서 sql언어로 db연결), 반드시 대문자로 작성
        id = request.form['mid'] #자료 수집(register에 mid를 받아서 변수 id에 담음)
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['regDate']

        conn = getconn() #담은 것을 db에 연결
        cur = conn.cursor()
        sql = "INSERT INTO member VALUES ('%s', '%s', '%s', '%s', '%s')" \
              % (id, pwd, name, age, date)

        cur.execute(sql) #실행
        conn.commit() #커밋 완료
        conn.close()
        return redirect(url_for('memberlist')) #회원목록으로 넘어가도록 url경로 지정(확장자 제외)
    else:
        return render_template('register.html') #GET방식으로 요청(회원가입 페이지 노출)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        id = request.form['mid'] #자료 전달 받음
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s' " % (id, pwd) #db자료 확인 여부 확인, 조건에 맞는 한 개가 검색되면
        cur.execute(sql)
        rs = cur.fetchone() #db에서 찾은 그 데이터 한 개
        conn.close()
        if rs:
            session['userID'] = id #session권한 발급(로그인이 되면 자유롭게 이동할 수 있는 권리 부여)
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout(): #페이지 생성하지 않음
    session.pop('userID') #세션 권한 삭제
    return redirect(url_for('index'))

@app.route('/member_del/<string:id>/') #삭제 url생성
def member_del(id): #(m)id를 매개변수로 넘겨줌
    conn = getconn() #db와 연동
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s' " % (id) #member_view에서 수행 것을 넘겨받은 후
    cur.execute(sql) #삭제 수행
    conn.commit() #수행 완료
    conn.close()
    return redirect(url_for('memberlist'))

@app.route('/member_edit/<string:id>/', methods = ['GET', 'POST'])
def member_edit(id):
    if request.method == "POST":
        #회원정보에서 수정된 자료 넘겨 받음
        id = request.form['mid']  # 자료 수집(register에 mid를 받아서 변수 id에 담음)
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['regDate']
        #db 연결
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd = '%s', name = '%s', age = '%s', regDate = '%s' " \
              "WHERE mid = '%s' " % (pwd, name, age, date, id)
        cur.execute(sql)  # 실행
        conn.commit()  # 커밋 완료
        conn.close()
        return redirect(url_for('member_view', id=id)) #register와 달리 수정은 id를 통해서 들어갔기 때문에 즉, member_edit에서 수정해서 저장하면 member_view로 페이지가 넘어가기 때문에 id=id입력 필요
    else:
        conn = getconn() #회원 자료 가져오기
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if 'userID' in session:
            ssid = session.get('userID')
            return render_template('member_edit.html', rs=rs, ssid=ssid) #정보를 rs로 받아서 가져옴
        else:
            return render_template('member_edit.html')

app.run(debug=True)