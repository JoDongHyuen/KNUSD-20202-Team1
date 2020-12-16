import sys, threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from setting_depart import *
from setting_lms import *
from crawling_depart import *


#call by reference의 형태로 변수를 넘겨주기 위해, 리스트형태

departupdate_check = [] #학부의 현재 알람 on/off 상태 디폴트는 off인 0
lmsupdate_check = [] #lms의 현재 알람 on/off 상태 디폴트는 off인 0
set_depart = [] #setting_depart 파일의 클래스
set_lms = [] #setting_lms 파일의 클래스

set_d = setting_depart()
set_d.load()
set_l = setting_lms()
set_l.load()

lmsupdate_check.append(0)
set_lms.append(set_l)
departupdate_check.append(0)
set_depart.append(set_d)

class depart_set(QWidget):

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
        if not len(set_depart[0].depart):
            self.depart_com.toggle()
        if '컴퓨터학부' in set_depart[0].depart:#현재 학부 선택 상태 반영
            self.depart_com.toggle()
        self.depart_com.stateChanged.connect(self.select_computer)#컴퓨터학부 체크박스 누를때 실행

        self.depart_electronic = QCheckBox('전자공학부', self)
        self.depart_electronic.move(200,160)
        if '전자공학부' in set_depart[0].depart:#현재 학부 선택 상태 반영
            self.depart_com.toggle()
        self.depart_electronic.stateChanged.connect(self.select_electronic)#전자공학부 체크박스 누를때 실행

        self.depart_electricity = QCheckBox('전기공학부', self)
        self.depart_electricity.move(300,160)
        if '전기공학부' in set_depart[0].depart:#현재 학부 선택 상태 반영
            self.depart_com.toggle()
        self.depart_electricity.stateChanged.connect(self.select_electricity)#전기공학부 체크박스 누를때 실행

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
        print(set_depart[0].keyword)
        for k in set_depart[0].keyword:
            if(k == self.addkeyword.text() and len(self.addkeyword.text()) < 1) : #입력한 키워드가 이미 존재할 경우
                return
        set_depart[0].append_keyword(self.addkeyword.text())#설정의 keyword에 키워드값 넣기
        self.print_keyword() 

    #삭제버튼 클릭시 동작
    def delete_action(self) :
        global set_depart
        print(set_depart[0].keyword)
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
        #set_depart[0].append_depart(text) #설정의 depart에 학부값 넣기
    
    #전자공학부 체크박스 상태변화시 동작
    def select_electronic(self):
        global set_depart
        if '전자공학부' in set_depart[0].depart:#이미 있는 학부면 삭제
            set_depart[0].delete_depart("전자공학부")
            return
        set_depart[0].append_depart("전자공학부")

    #전기공학부 체크박스 상태변화시 동작
    def select_electricity(self):
        global set_depart
        if '전기공학부' in set_depart[0].depart:#이미 있는 학부면 삭제
            set_depart[0].delete_depart("전기공학부")
            return
        set_depart[0].append_depart("전기공학부")

class ALARM_Window(QWidget):
    

    def __init__(self):
        super().__init__()
        
        self.dialog = QDialog()
        self.d_s = depart_set()

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
        self.button1.toggled.connect(self.crawling_lms_state)#lms on/off버튼에 기능 연결

        self.button2 = QPushButton('로그인')
        grid_layout.addWidget(self.button2, 2, 0)

        self.button3 = QPushButton('On/Off')
        grid_layout.addWidget(self.button3, 1, 1)
        self.button3.setCheckable(True)
        self.button3.toggled.connect(self.crawling_depart_state)#depart on/off버튼에 기능 연결

        self.button4 = QPushButton('설정')
        grid_layout.addWidget(self.button4, 2, 1)
        self.button4.clicked.connect(self.d_setting)

        # initUI 세팅
        self.setWindowTitle('통합 알림 시스템')
        self.resize(400,200)
        self.show()

    def d_setting(self):
        self.d_s.show()

    def crawling_depart_state(self):#학부 on/off 변경
        global departupdate_check
        global set_depart

        if(departupdate_check[0]==1):#알람이 on이였으면
            departupdate_check[0]=0#off 시키기
            print('크롤링을 종료합니다')#테스트용 나중에 지울것

        elif(departupdate_check[0]==0):#알람이 off이였으면
            departupdate_check[0]=1#on 시키기

            print('크롤링을 시작합니다')#테스트용 나중에 지울것
            set_depart[0].load()
            for d in set_depart[0].depart:             
                crawl_thread_depart = crawling_depart_thread(self,d)
                crawl_thread_depart.start()
                

    def crawling_lms_state(self):#LMS on/off 변경 - 미구현
        global lmsupdate_check

        if(lmsupdate_check[0]==1):#알람이 on이였으면
            lmsupdate_check[0]=0#off 시키기
            print('크롤링을 종료합니다')#테스트용 나중에 지울것

        elif(lmsupdate_check[0]==0):#알람이 off이였으면
            lmsupdate_check[0]=1#on 시키기
            print('크롤링을 시작합니다')#테스트용 나중에 지울것
    
class crawling_depart_thread(QThread):
    def __init__(self,parent,depart):
        super().__init__(parent)
        self.depart = depart

    def run(self):
         depart_crawl = depart_noti(self.depart)
         depart_crawl.get_change(departupdate_check,set_depart)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    windowExample = ALARM_Window()
    windowExample.show()
    sys.exit(app.exec_())