from django.shortcuts import render
from django.http import HttpResponse
from matplotlib import pyplot as plt
from .model_pandas import like_lib
from .model_pandas import lib_list
from .model_pandas import register
from .model_pandas import login
from django.core.paginator import Paginator

# Create your views here.

def lib_like(request):
    return render(
    request,
    'libapp/list.html',
    {}
)
    
def createTable(request):
    like_lib.createTableSurvey()
    
    return HttpResponse('Create OK!')


# # 설문 전체 조회하기 
# # 데이터 프레임으로 받은내용을 html로 전환한후 출력 
# def view_Survey_List(request):
    
#     df =  like_lib.getSurveyList()
    
#     # return HttpResponse(df.to_html())
#     context = {'df' : df.to_html()}
#     return render(
#     request,
#     'chi2app/list.html',
#     context
#     )
    
# 설문 참여하기 페이지 view
def view_Survey(request):
        return render(
    request,
    'libapp/survey.html',
    {}
    )
        
# 설문 데이터 입력 (html에서 전달 된 값)
def set_Survey_Insert(request):
    pgender    = request.POST.get('gender')
    page       = request.POST.get('age')
    plib_survey = request.POST.get('lib_survey')
    pfood_survey = request.POST.get('food_survey')
    pvisit_survey = request.POST.get('visit_survey')
    ppurpose_survey = request.POST.get('purpose_survey')
    pprogram_survey = request.POST.get('program_survey')    
    
    rs = like_lib.setSurveyInsert(pgender,page,plib_survey,pfood_survey,pvisit_survey,ppurpose_survey,pprogram_survey)
    
    msg = ''
    if rs=='ok' :
        msg =  '''<script>
                    alert('설문조사에 응답해 주셔서 감사합니다.')
                    location.href = '/libapp/index/'
                </script>s
                '''
        
    
    return HttpResponse(msg)


# -----------------------------------------설문조사 분석 결과 -------------------------------------

# 설문 분석결과 보기
def survey_Analysis(request):
    # 설문 데이터 조회하기
    df =like_lib.getSurveyList()
    
    # 설문 분석하기(함수로 처리)
    # rs_df : 분석에 사용된 컬럼 추가된 최종본
    # rs_ct : 교차표(crossTable)데이터
    # rs_msg : 해석 결과
    rs_df, rs_ct , rs_msg = get_Analysis(df)
    
    # 시각화 및 저장하기( 함수로 처리 )
    view_Visualization(rs_df)
    
    context = {
        # 교차표를 html로 전환하여 키 생성 
        'crossTab' : rs_ct.to_html(),
        # 해석내용
        'results' : rs_msg
    }
    return render(request,
                    'libapp/analysis_new.html', # 링크 libapp/analysis.html 로 바꿔주면 이전 으로 작동 
                    context)


import pandas as pd
import scipy.stats as stats
import seaborn as sns 
import matplotlib.pyplot as plt    
# 설문 분석하기
def get_Analysis (df) :
    # 성별을 숫자로 (람다 방식 사용)
    df['genNum'] = df['gender'].apply(lambda g:1 if g=='남' else 2) # if 문 부터 시작 g == 남자 > g =1 
    
    # 커피숍 이름을 숫자로
    df['purposeNum'] = df['purpose_survey'].apply(lambda c:1 if c =='독서'\
                                        else 2 if c == '휴식' \
                                        else 3 if c=='공부' else 4 ) 
    # 교차표(빈도표) 작성하기
    crossTab = pd.crosstab(index = df['gender'], columns=df['purpose_survey'])
    
    # 검증하기 
    chi, pv , _,_ = stats.chi2_contingency(crossTab) # 뒤에 두개의 값은 받을 필요없어서 _ 로 할당 
    
    # 검증결과
    results = ''
    
    if pv > 0.05 :
        results='p-value 값이 유의수준 <b>{:.3f} > 0.05</b>  이므로,'\
                '<br> 성별에 따라 도서관 방문목적에는 '\
                '<b>차이가 없다.(귀무가설 채택) </b>'.format(pv)
    else : 
        results='p-value 값이 유의수준 <b>{:.3f} <= 0.05</b>  이므로,'\
                '<br> 성별에 따라 도서관 방문 목적에는'\
                '<b>차이가 있다.(대립가설 채택) </b>'.format(pv)
    return df, crossTab, results


#시각화 및 저장하기
def view_Visualization(df):
    # 한글처리
    plt.rc('font', family='Malgun Gothic')
    # 그래프 사이즈
    plt.figure(figsize=(10,10))
    
    # fig 객체 얻기 : gcf => figure와 같음
    fig = plt.gcf()
    
    # 그룹화하기
    gen_group = df['purpose_survey'].groupby(df['purposeNum']).count()
    
    # 그룹에 인덱스 이름 정의하기 (인덱스 번호를  한글 이름으로)
    gen_group.index = ['독서','휴식','공부','기타']
    
    # 막대그래프 그리기 
    # width = 막대 너비 
    gen_group.plot.bar(color = ['pink','lightgreen','wheat','lightblue'],
                        width = 0.4)
    
    # 제목정의 
    plt.title('도서관 방문목적별 방문자수', fontsize=30)
    plt.xlabel('방문목적', fontsize = 20)
    plt.ylabel('방문목적 건수', fontsize=20)
    
    # x축 y축에 들어가는 값들에 대한 폰트 사이즈 조정
    # rotation : 기울기 각도 
    plt.xticks(fontsize=20, rotation = 90)
    
    plt.yticks(fontsize=20)
    
    # 그래프 저장하기
    fig.savefig('libapp/static/libapp/images/libapp2.png')

# ------------------------------------ css 적용된 html ------------------------------------------
    
    
def index(request):
    #코드 구현
    return render(request, "libapp/index.html")

def survey_new(request):
    #코드 구현
    return render(request, "libapp/survey_new.html")

def analysis_new(request):
    #코드 구현
    return render(request, "libapp/analysis_new.html")

def lib_insert_form_new(request):
    #코드 구현
    return render(request, "libapp/lib_insert_form_new.html")

def about(request):
    #코드 구현
    return render(request, "libapp/about.html")


# ------------------------------- 도서관 리스트 화면 -----------------------------------------
#페이지 처리 라이브러리
from django.shortcuts import render
from django.http import HttpResponse
from .model_pandas import lib_list


#페이지 처리 라이브러리
from django.core.paginator import Paginator

# Create your views here.
# 주문전체 조회
def view_lib_List(request):
    
    df = lib_list.get_Lib_List()
    # return HttpResponse(df)
    
    context = {'df' : df } # 여러개 넣을때는 {'키' : value, '키' : value , '키' : value}
    
    
    return render(
        request,
        'libapp/lib_list.html',
        context
    )
    
    
    
# 도서관 리스트 전체 조회 - 2 
def view_lib_List_dict(request):
    
    df_list= lib_list.getLib_List # 리스트라 딕셔너리로 변환 해줘야 html이 인식 
    # return HttpResponse(df)
    
    context = {'df_list' : df_list } # 여러개 넣을때는 {'키' : value, '키' : value , '키' : value}
    
    
    return render(
        request,
        'libapp/lib_list.html',
        context
    )
    
## 도서관전체리스트
### 리스트의 selected 처리하기..
def selected_Control(sel, sh) :
    
    if len(sh) <= 0 :        
        return "selected", "", ""
    
    if sel == "lib_name" :
        sel_name = "selected"
        sel_loc = ""
        sel_year = ""
        
    elif sel == "loc" : 
        sel_name = ""
        sel_loc = "selected"
        sel_year = ""
        
    elif sel == "year" : 
        sel_name = ""
        sel_loc = ""
        sel_year = "selected"
    
    return sel_name, sel_loc, sel_year
            
                
## 도서관전체리스트
def view_lib_list_Page(request):
    
    # 페이지 처리 시작
    # page = request.GET.get("page","1")
    
    now_page = 1
    sel = ""
    sh = ""
    
    sel_name = "selected"
    sel_loc = ""
    sel_year = ""
    
    try :
        
        if request.method == "GET" :
            now_page = request.GET.get("page")
            now_page = int(now_page)
            
            sel = request.GET.get("sel", "")
            sh = request.GET.get("sh", "")
            
            sel_name, sel_loc, sel_year = selected_Control(sel, sh)
        
        if request.method == "POST" :
            now_page = 1
            
            sel = request.POST.get("sel", "")
            sh = request.POST.get("sh", "")
            
            sel_name, sel_loc, sel_year = selected_Control(sel, sh)
    # 페이지 처리 끝 
    except :
        now_page = 1
    
    # 모델 조회
    df_list, sql = lib_list.getLib_List(sel,sh) # 리스트라 딕셔너리로 변환 해줘야 html이 인식 
    # return HttpResponse(df)
    # 페이지 처리 ㅣ작 
    p =Paginator (df_list,30)
    #첫번째값 : 모델 조회할 페이지
    #두번째값 : 한페이지에 보열줄 행의 갯수
    
    #사용할  데이터 추출
    info = p.get_page(now_page)
    
    #시작 페이지 번호 
    start_page = (now_page - 1) // 10*10+1
    #마지막 페이지 번호
    end_page = start_page +9

    
    
    # p.num_pages : 전체 페이지 수
    # end_page : 계산에 의한 페이지 수 (10단위 계산)
    # 전체 페이지 수보다 크다면 ,
    if end_page > p.num_pages :
        end_page =p.num_pages
    
    # 이전 페이지 가기
    is_prev = False
    # 다음 페이지 가기
    is_next = False
    
    ## 이전/다음 체크하기
    if start_page > 1 :
        is_prev = True
    if end_page < p.num_pages :
        is_next = True
    

    # 페이지 처리 처리끝
    
    #context = {'df_list' : df_list } # 여러개 넣을때는 {'키' : value, '키' : value , '키' : value}
    context ={"info" : info,
                "page_range" : range(start_page, end_page+1),
                "is_prev": is_prev,
                "is_next": is_next,
                "start_page" : start_page,
                "end_page" : end_page,
                "now_page" : now_page,
                "sel" : sel,
                "sh" : sh,
                "sel_name" : sel_name,
                "sel_loc" : sel_loc,
                "sel_year" : sel_year,
                "sql" : sql
    }
    #return HttpResponse(df_list)
    return render(
        request,
        'libapp/page_control/lib_list_page_new.html',
        context
    )
    
    
    
    
    
# 주문 상세 조회 
def view_lib(request):
    plib_name = request.GET['plib_name']
    ploc = request.GET['ploc']
    df_dict = lib_list.getlib(plib_name,ploc) # 주문번호와 상품코드 
    # context = {'df' : df}
    return render(
        request,
        'libapp/lib.html',
        df_dict # 자체가 딕셔너리라 context 사용안하고 바로 넣어줘도 된다 
    )
    
# 입력 폼(form)  
def view_lib_Insert(request):
    plib_name= '논골도서관'
    ploc = '경기'
    
    return render(
        request,
        'libapp/lib_insert_form.html',
        {'plib_name' : plib_name , 
            'ploc':ploc}
        )

# 입력 함수 (직접 우리가 여기서 입력)
def set_lib_Insert(request):
    plib_name = request.POST.get('lib_name')
    ploc = request.POST.get('loc')
    ploc2 = request.POST.get('loc2')
    pyear = request.POST.get('year')
    paddrr = request.POST.get('addrr')
    pnum = request.POST.get('num')
    phomep = request.POST.get('homep')
    popen_time = request.POST.get('open_time')
    prest_day = request.POST.get('rest_day')
    
    msg = lib_list.setlibInsert(plib_name,ploc,ploc2,pyear,paddrr,pnum,phomep,popen_time,prest_day) # 삽입 함수 
    pageControl = ''
    
    if msg == 'Y' : 
        pageControl = '''<script>
                            alert('수정 되었습니다!!')
                            location.href='/libapp/page_control/lib_list_page/'
                        </script>
                        '''
    else : 
        pageControl = '''<script>
                            alert('수정실패')
                            history.go(-1)
                        </script>
                        '''
    return HttpResponse(pageControl)

#-----------------------------------------로그인 & 회원가입 -----------------------------------
## http://127.0.0.1:8000/libapp/insertTable/ << 테이블 먼저 만들기 
# 메인
def main(request):
    return render(
        request,
        "libapp/01_main.html",
        {}
    )

# ---------------------------------------------------------------회원가입 파트 
# survey 테이블 생성하기
def createTable(request):
    register.createTableMember()
    
    return HttpResponse("Create OK.....")


# 회원가입 화면
def register_lib(request):
    return render(
        request,
        "libapp/register.html",
        {}
    )

# 회원 데이터 입력
def set_Member_Insert(request):
    pmemname = request.POST.get("name")
    pmemid = request.POST.get("id")
    pmempass = request.POST.get("pass")
    
    pageControl = ""
    
    if pmemname == '' or pmemid =='' or pmempass=='':
        pageControl = """<script>
                    alert('정보를 입력해주세요')
                    location.href='/libapp/register/'
                </script>
                """
        
    else  : 
        ms = register.setMemberInsert(pmemname, pmemid, pmempass)
        
        if ms=='':
            pageControl = """<script>
                                alert('정보를 입력해주세요')
                                location.href='/libapp/register/'
                            </script>
            """
        else: 
            
            # return HttpResponse("Insert OK")
            
            if ms == "OK" :
                pageControl = """<script>
                                    alert('회원가입 완료')
                                    location.href='/libapp/login/'
                                </script>
                """
            else:
                pageControl = """<script>
                                    alert('가입 실패!')
                                    history.go(-1)
                                </script>
                """
        
    return HttpResponse(pageControl)



# ---------------------------------------------------------------로그인 파트 
# 로그인 화면
def login_lib(request):
    return render(
        request,
        "libapp/login.html",
        {}
    )

def getlogin(request):
    try:
        pmem_id = request.POST["mem_id"]
        pmem_pass = request.POST["mem_pass"]
    
    except:
        context = """<script>
                        alert('직접 접근 하시면 안됩니다..@@ 로그인 페이지로 이동')
                        location.href = '/libapp/login/'
                    </script>"""
        return HttpResponse(context)
    
    # 아이디 패스워드 확인 모델 호출(한건 조회)
    df_dict = login.getLogin(pmem_id, pmem_pass)
    
    # 로그인 실패 시 처리
    if df_dict["ms"] == "no":
        context = """
        <script>
            alert('아이디 또는 패스워드를 확인하여 주세요!')
            history.go(-1)
        </script>
        """
        return HttpResponse(context)
    
    # Session 처리 (회원 정보를 서버에 저장해 놓고 있는 상태)
    #   - 로그아웃 하기 전까지 회원 정보는 어느 페이지를 가든 살아 있습니다.
    #   - request.session[]을 통해서 사용합니다
    #   - session에 저장되는 값들을 딕셔너리 형태로 저장됨
    
    # session 등록하기
    request.session["sMem_id"] = pmem_id
    request.session["sMem_name"] = df_dict["mem_name"]
    
    # 세션에 저장된 값 불러오기
    if request.session.get("sMem_id"):
        # 세션에 값이 있는 경우
        df_dict["sMem_id"] = request.session["sMem_id"]
        df_dict["sMem_name"] = request.session["sMem_name"]
    else :
        # 세션에 값이 없는 경우
        df_dict["sMem_id"] = None
        
    
    df_dict["pmem_id"] = pmem_id
    df_dict["pmem_pass"] = pmem_pass
    
    return render(
        request,
        "libapp/index.html",
        {}
    )
    
    # return render(
    #     request,
    #     "libapp/login.html",
    #     df_dict
    # )

# 로그아웃
def set_Logout(request):
    
    # 세션정보 확인하기
    if request.session.get("sMem_id"):
        # 세션정보 삭제하기
        request.session.flush()
        
        context = """<script>
                        alert('로그아웃 되었습니다.')
                        location.href = '/libapp/login/'
                    </script>"""
    else :
        context = """<script>
                        alert('직접 접근 하시면 안됩니다')
                        location.href = '/libapp/login/'
                    </script>"""
                    
    return HttpResponse(context)
