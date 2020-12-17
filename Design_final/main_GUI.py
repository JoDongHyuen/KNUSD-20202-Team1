
import sys, threading, requests, json, re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from setting_depart import *
from setting_lms import *
from Alarm_depart import *
from Alarm_lms import *

#call by reference의 형태로 변수를 넘겨주기 위해, 리스트형태

depart_alarm_on = [] #학부의 현재 알람 on/off 상태 디폴트는 off인 0
lms_alarm_on = [] #lms의 현재 알람 on/off 상태 디폴트는 off인 0
set_depart = [] #setting_depart 파일의 클래스
set_lms = [] #setting_lms 파일의 클래스

set_d = setting_depart()
set_d.load()
set_l = setting_lms()
set_l.load()

lms_alarm_on.append(0)
set_lms.append(set_l)
depart_alarm_on.append(0)
set_depart.append(set_d)


# id / pwd에 본인 lms 아이디 비번 입력
LOGIN_INFO = {
    'usr_id': '',
    'usr_pwd': ''
}
login_check = 0

class depart_set(QWidget): #학부 설정창

    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        self.setUI()

    def setUI(self) :
        global set_depart

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # 레이블 및 버튼 추가
        self.label1 = QLabel('알림 키워드 입력')
        font1 = self.label1.font()
        font1.setPointSize(40)
        self.grid_layout.addWidget(self.label1, 00, 0)

        self.addkeyword = QLineEdit()
        self.grid_layout.addWidget(self.addkeyword, 10, 0)

        self.deletekeyword = QLineEdit()
        self.grid_layout.addWidget(self.deletekeyword, 20, 0)

        self.btnadd = QPushButton('추가')
        self.grid_layout.addWidget(self.btnadd, 10, 10)
        self.btnadd.released.connect(self.add_action)#추가버튼에 기능 연결

        self.btndelete = QPushButton('삭제')
        self.grid_layout.addWidget(self.btndelete, 20, 10)
        self.btndelete.released.connect(self.delete_action)#삭제버튼에 기능 연결

        self.label2 = QLabel('학부 선택')
        font1 = self.label2.font()
        font1.setPointSize(40)
        self.grid_layout.addWidget(self.label2, 30, 0)

        self.depart_com = QCheckBox('컴퓨터학부', self)
        self.depart_com.move(100,160)
        if len(set_depart[0].depart) == 0 :
            print(len(set_depart[0].depart))
            self.depart_com.toggle()
        if '컴퓨터학부' in set_depart[0].depart:#현재 학부 선택 상태 반영
            self.depart_com.toggle()
        self.depart_com.stateChanged.connect(self.select_computer)#컴퓨터학부 체크박스 누를때 실행

        self.depart_electronic = QCheckBox('전자공학부', self)
        self.depart_electronic.move(200,160)
        if '전자공학부' in set_depart[0].depart:#현재 학부 선택 상태 반영
            self.depart_electronic.toggle()
        self.depart_electronic.stateChanged.connect(self.select_electronic)#전자공학부 체크박스 누를때 실행

        self.depart_electricity = QCheckBox('전기공학과', self)
        self.depart_electricity.move(300,160)
        if '전기공학과' in set_depart[0].depart:#현재 학부 선택 상태 반영
            self.depart_electricity.toggle()
        self.depart_electricity.stateChanged.connect(self.select_electricity)#전기공학과 체크박스 누를때 실행

        self.label3 = QLabel('현재 설정된 키워드')#현재 설정된 키워드 정보 제목
        font1 = self.label3.font()
        font1.setPointSize(30)
        self.grid_layout.addWidget(self.label3, 0, 10)

        self.label4 = QLabel('')#현재 설정된 키워드 정보
        font1 = self.label4.font()
        font1.setPointSize(20)
        self.grid_layout.addWidget(self.label4, 1, 10)
        self.print_keyword() 

        # 학부홈페이지 설정 창 세팅
        self.setWindowTitle('학부홈페이지 설정')
        self.resize(400,200)

    #추가버튼 클릭시 동작
    def add_action(self) :
        global set_depart

        for k in set_depart[0].keyword:
            if(k == self.addkeyword.text() and len(self.addkeyword.text()) < 1) : #입력한 키워드가 이미 존재할 경우
                return
        set_depart[0].append_keyword(self.addkeyword.text())#설정의 keyword에 키워드값 넣기
        self.print_keyword() 

    #삭제버튼 클릭시 동작
    def delete_action(self) :
        global set_depart

        for k in set_depart[0].keyword:
            if(k == self.deletekeyword.text()) : #삭제할 키워드가 존재
                set_depart[0].delete_keyword(self.deletekeyword.text())#설정의 keyword에 키워드값 삭제
        self.print_keyword()    
        
    #현재 키워드 리스트 출력
    def print_keyword(self):
        global set_depart

        now_keyword = ",".join(set_depart[0].keyword)
        self.label4.setText(now_keyword)

    #컴퓨터학부 체크박스 상태변화시 동작
    def select_computer(self):
        global set_depart           
        if '컴퓨터학부' in set_depart[0].depart:#이미 있는 학부면 삭제
            set_depart[0].delete_depart("컴퓨터학부")
            return     
        set_depart[0].append_depart("컴퓨터학부")#아니면 학부 추가
    
    #전자공학부 체크박스 상태변화시 동작
    def select_electronic(self):
        global set_depart
        if '전자공학부' in set_depart[0].depart:#이미 있는 학부면 삭제
            set_depart[0].delete_depart("전자공학부")
            return
        set_depart[0].append_depart("전자공학부")

    #전기공학과 체크박스 상태변화시 동작
    def select_electricity(self):
        global set_depart
        if '전기공학과' in set_depart[0].depart:#이미 있는 학부면 삭제
            set_depart[0].delete_depart("전기공학과")
            return
        set_depart[0].append_depart("전기공학과")

class lms_login(QWidget): #lms 로그인창
    def __init__(self):
        self.id = ''
        self.pw = ''

        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        la1 = QLabel('ID')
        grid_layout.addWidget(la1)
        self.text1 = QLineEdit()
        grid_layout.addWidget(self.text1)

        la2 = QLabel('PW')
        grid_layout.addWidget(la2)
        self.text2 = QLineEdit()
        self.text2.setEchoMode(QLineEdit.Password)
        grid_layout.addWidget(self.text2)

        btn=QPushButton('Login')
        btn.clicked.connect(self.pushButtonClicked)
        grid_layout.addWidget(btn)

        self.setWindowTitle('LMS Login')
        self.setGeometry(300,300,300,100)

        #자동로그인 먼저시도
        if(len(set_lms[0].ID) > 0 and len(set_lms[0].PW ) > 0) :
            LOGIN_INFO['usr_id'] = set_lms[0].ID
            LOGIN_INFO['usr_pwd'] = set_lms[0].PW 
            self.try_login(2)

    def pushButtonClicked(self):
        self.id = self.text1.text()
        self.pw = self.text2.text()

        LOGIN_INFO['usr_id'] = self.id
        LOGIN_INFO['usr_pwd'] = self.pw

        self.try_login(1)

    def try_login(self,mode):  #mode = 1 수동, mode=2 자동  
        with requests.session() as s:
        
            global login_check

            login_check = 0

            #로그인에 실패하면 login에 isError 가 True로 나타나서 이걸 이용해 exception 처리 예정
            login_req = s.post('https://lms.knu.ac.kr/ilos/lo/login.acl', data=LOGIN_INFO)
            login = login_req.text
            login = json.loads(login)
            if(login['isError'] == False):
                login_check = 1
                if mode ==1:
                    QMessageBox.question(self,'Message','로그인 성공',QMessageBox.Ok)
                    set_lms[0].set_login(self.id,self.pw) #로그인성공하면 ID/PW저장
                if mode == 2:
                    QMessageBox.question(self,'Message','자동 로그인 성공',QMessageBox.Ok)
                self.close()

            else:
                QMessageBox.question(self,'Message','ID/PW를 확인하십시오',QMessageBox.Ok)


class ALARM_Window(QWidget): #메인 GUI
    

    def __init__(self):
        super().__init__()

        self.dialog = QDialog()
        self.d_s = depart_set()
        self.lms_login = lms_login()

        self.initUI()

    def initUI(self) :

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # 레이블 및 버튼 추가
        self.label1 = QLabel('LMS')
        font1 = self.label1.font()
        font1.setPointSize(40)
        self.label1.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.label1, 0, 0)

        self.label2 = QLabel('학부 홈페이지')
        font2 = self.label2.font()
        font2.setPointSize(40)
        self.label2.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.label2, 0, 1)

        self.button1 = QPushButton('On/Off')
        grid_layout.addWidget(self.button1, 1, 0)
        self.button1.setCheckable(True)
        self.button1.toggled.connect(self.lms_on_set)#lms on/off버튼에 기능 연결

        self.button2 = QPushButton('로그인')
        self.button2.clicked.connect(self.lms_setting)
        grid_layout.addWidget(self.button2, 2, 0)

        self.button3 = QPushButton('On/Off')
        grid_layout.addWidget(self.button3, 1, 1)
        self.button3.setCheckable(True)
        self.button3.toggled.connect(self.depart_on_set)#depart on/off버튼에 기능 연결

        self.button4 = QPushButton('설정')
        grid_layout.addWidget(self.button4, 2, 1)
        self.button4.clicked.connect(self.depart_setting)

        # initUI 세팅
        self.setWindowTitle('통합 알림 시스템')
        self.resize(400,200)
        self.show()

    def depart_setting(self):
        self.d_s.show()

    def depart_on_set(self):#학부 on/off 변경
        global depart_alarm_on
        global set_depart
        
        if(depart_alarm_on[0]==1):#알람이 on이였으면
            depart_alarm_on[0]=0#off 시키기
            print('학부 크롤링을 종료합니다')#테스트용 나중에 지울것

        elif(depart_alarm_on[0]==0):#알람이 off이였으면
            depart_alarm_on[0]=1#on 시키기

            print('학부 크롤링을 시작합니다')#테스트용 나중에 지울것
            set_depart[0].load()
            #print(set_depart[0].depart)
            for d in set_depart[0].depart:                             
                crawl_thread_depart = crawling_depart_thread(self,d)
                crawl_thread_depart.start()
                

    def lms_on_set(self):#LMS on/off 변경
        global lms_alarm_on
        global set_lms
        global login_check

        if(lms_alarm_on[0]==1):#알람이 on이였으면
            lms_alarm_on[0]=0#off 시키기
            print('lms 크롤링을 종료합니다')#테스트용 나중에 지울것

        elif(lms_alarm_on[0]==0):#알람이 off이였으면
            if (LOGIN_INFO['usr_id'] == '' or LOGIN_INFO['usr_pwd'] == '' or login_check == 0):
                QMessageBox.question(self,'Message','로그인을 먼저해주세요',QMessageBox.Ok)
                self.button1.setCheckable(False)
                self.button1.setCheckable(True)
            else:
                lms_alarm_on[0]=1#on 시키기

                print('lms 크롤링을 시작합니다')#테스트용 나중에 지울것
                set_lms[0].load()
                crawl_thread_lms = crawling_lms_thread(self)
                crawl_thread_lms.start()

    def lms_setting(self):
        self.lms_login.show()
    
class crawling_depart_thread(QThread):
    def __init__(self,parent,depart):
        super().__init__(parent)
        self.depart = depart

    def run(self):
         depart_crawl = depart_noti(self.depart)
         depart_crawl.alarm_depart_wait(depart_alarm_on,set_depart)

class crawling_lms_thread(QThread):
    def __init__(self,parent):
        super().__init__(parent)

    def run(self):
        alarm_lms_wait(lms_alarm_on,set_lms)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    windowExample = ALARM_Window()
    windowExample.show()
    sys.exit(app.exec_())