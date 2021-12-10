#미리 안 만들고 여기서 db 만들기
import sqlite3

def getconn():
    conn = sqlite3.connect('./memberdb.db') #같은 곳에 db생성
    return conn

def create_table():
    conn = getconn()
    cur = conn.cursor()
    sql = """
    CREATE TABLE member(
        mid CHAR(5) PRIMARY KEY,
        passwd CHAR(8) NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        regDate DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    #regDate는 파이참의 현재날짜와 같이 자동생성되는 것
    cur.execute(sql)
    conn.commit()
    print("member테이블 생성") #호출 하기 전에 생성해서 파이참 콘솔창에서 확인 용도
    conn.close()

def insert_member():
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO member (mid, passwd, name, age) VALUES (?, ?, ?, ?)" #regDate는 자동생성되는 것으로 입력제외 처리(나머지 것만 입력되도록 설정), 예외사항 없을 시 칼럼명 생략 가능
    cur.execute(sql, ('20001', 'm1234', '흥부', 35)) #id는 문자로 하는 것이 처리하는데 오류가 줄어듦
    conn.commit()
    print("멤버 추가") #호출 하기 전에 생성해서 파이참 콘솔창에서 확인 용도
    conn.close()

def select_member(): #db브라우저에서 확인 안 하고자
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall() #db에서 반환된 자료
    #print(rs) #리스트형태로 출력
    for i in rs:
        #print(i[0]) #인덱싱을 통한 자료 정렬
        print(i)
    conn.close() #commit이 필요없음

def delete_member(): #db전체 데이터 삭제
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member"
    cur.execute(sql)
    conn.commit()
    conn.close()

#create_table() #호출, 테이블 생성된 것을 db브라우저에서 확인 가능, 처음할 때만 열고 다음부터는 막아준다
#insert_member()
select_member()
delete_member()