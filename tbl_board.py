import sqlite3 as sql

def getconn():
    conn = sql.connect("./memberdb.db")
    return conn

def create_table():
    conn = getconn()
    cur = conn.cursor()
    sql = """
    CREATE TABLE board(
        bno INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        create_date TIMESTAMP DATE DEFAULT (datetime('now', 'localtime')),
        hit INTEGER,
        mid CHAR(5) NOT NULL,
        FOREIGN KEY(mid) REFERENCES member(mid) ON DELETE CASCADE
    );    
    """
    #bno - 글번호, title - 글제목, content - 글내용, create_date - 작성일, mid - 회원번호(외래키)
    #mid는 member테이블과 연결시켜주는 역할
    #자동시간 입력을 DATETIME DEFAULT CURRENT_TIMESTAMP에서 현지시간을 불러오는 코드로 수정
    cur.execute(sql)
    conn.commit()
    print("board테이블 생성!")
    conn.close()

def drop_table(): #삭제를 해야 고칠 수 있기 때문
    conn = getconn()
    cur = conn.cursor()
    sql = "DROP TABLE board"
    cur.execute(sql) #sql에서 코드문 실행
    conn.commit() #db에서 실행
    conn.close()

def insert_board():
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO board(title, content, mid) VALUES (?, ?, ?)" #자동생성되는 것들 입력제외 처리
    cur.execute(sql, ('제목1', '내용입니다', 'cloud'))
    conn.commit()
    print("게시글 추가")
    conn.close()

def select_board():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board"
    cur.execute(sql)
    rs = cur.fetchall()
    for i in rs:
        print(i)
    print(rs)
    conn.close()

#create_table()
#drop_table()
#insert_board()
#select_board()