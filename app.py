import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "KIMTAEHOON" #세션에 따른 암호키 설정

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/') #127.0.0.1:/5000
def index():
    return render_template('index.html')

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall() #db에서 검색한 데이터
    conn.close()
    return render_template('memberlist.html', rs=rs) #가져온 데이터를 웹으로 보내줌

@app.route('/member_view/<string:id>/')
def member_view(id): #mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('member_view.html', rs=rs)

@app.route('/register/', methods = ['GET', 'POST']) #url경로
def register():
    if request.method == 'POST': #POST방식, 반드시 대문자로 작성
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
        id = request.form['mid']#자료 전달 받음
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s' " % (id, pwd)#db자료 확인 여부 확인, 조건에 맞는 한 개가 검색되면
        cur.execute(sql)
        rs = cur.fetchone()#db에서 찾은 그 데이터 한 개
        conn.close()
        if rs:
            session['userID'] = id #세션 권한 발급(로그인이 되면 자유롭게 이동할 수 있는 권리 부여)
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('userID') #세션 권한 삭제
    return redirect(url_for('index'))

app.run(debug=True)