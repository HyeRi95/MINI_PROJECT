import pandas as pd 
# djagno 가상환경에서 cx_Oracel 설치해야 합니다
# 설치 : 가상환경 프롬프트(cmd) > pip install cx_oracle
import cx_Oracle as ora

import os
# 64bit Oracle client 미설치시 사용
LOCATION = r"C:\Users\82102\Desktop\oracle_client\instantclient_12_2"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]


# 오라클 연결 및 접속하기
def getConnection() :
    # 오라클 연결하기
    dsn = ora.makedsn('localhost',1521,'orcl')
    #오라클 접속하기
    conn =  ora.connect('project_2','dbdb',dsn)
    return conn 

# 커서 받기
def getCursor(conn):
    cursor = conn.cursor()
    return cursor

# 접속 정보 및 커서 반납하기
def dbClose(cursor, conn):
    # 커서 반납 먼저
    cursor.close()
    # 마지막에 접속정보 반납
    conn.close()


## survey 테이블 생성하기
def createTableSurvey() :
    conn = getConnection()
    cursor = getCursor(conn)

    sql = ''' CREATE table survey
            (
                rnum number(15) not null,
                gender varchar2(20) not null,
                age number(15) not null,
                lib_survey varchar2(50) not null,
                food_survey varchar2(50) not null,
                visit_survey varchar2(50) not null,
                purpose_survey varchar2(50) not null,
                program_survey varchar2(50) not null,
                Constraint pk_rnum Primary key (rnum)
            )'''
    
    cursor.execute(sql)
    dbClose(cursor, conn)
    
# 설문 입력하기
# - 함수  :  NVL("값", "지정값") : oracle 
def setSurveyInsert(pgender, page, plib_survey,pfood_survey,pvisit_survey,ppurpose_survey,pprogram_survey) : # gender ,age , co_survey는 받아오는 값 
    conn = getConnection()
    cursor = getCursor(conn)
    
    # rnum 자동 생성하기 
    sql = '''SELECT nvl(max(rnum)+1,1) as max_no 
                FROM survey'''
    cursor.execute(sql)
    rs_max_no = cursor.fetchone()
    no=rs_max_no[0]
    
    # 저장하기
    sql = '''INSERT INTO survey(
                rnum, gender, age, lib_survey,food_survey,visit_survey,purpose_survey,program_survey)
                values(
                    :rnum, :gender, :age, :lib_survey, :food_survey, :visit_survey,:purpose_survey,:program_survey)'''
    cursor.execute(sql,
                    rnum= no,
                    gender=pgender,
                    age=page,
                    lib_survey=plib_survey,
                    food_survey = pfood_survey,
                    visit_survey = pvisit_survey,
                    purpose_survey = ppurpose_survey,
                    program_survey= pprogram_survey)
    conn.commit()
    dbClose(cursor, conn)
    return 'ok'

# 
def getSurveyList():
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """SELECT * FROM survey"""
    cursor.execute(sql)
    
    row = cursor.fetchall()
    
    # 컬럼명 조회하기
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0].lower()) 
    dbClose(cursor,conn)
    
    # 데이터 프레임에 조회 결과 넣기 
    df = pd.DataFrame(row, columns = col)
    
    return df 
    
