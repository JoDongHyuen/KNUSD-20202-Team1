import sys, threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from setting_depart import *
from setting_lms import *
from crawling_depart import *

set_depart = setting_depart() #setting_depart 파일의 클래스
set_lms = setting_lms() #setting_lms 파일의 클래스

class depart_set(QWidget):

    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        self.setUI()

    def setUI(self) :
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
        self.btnadd.clicked.connect(self.add_action)#추가버튼에 기능 연결

        self.btndelete = QPushButton('삭제')
        self.grid_layout.addWidget(self.btndelete, 20, 10)
        self.btndelete.clicked.connect(self.delete_action)#삭제버튼에 기능 연결

        self.label2 = QLabel('학부 선택')
        font1 = self.label2.font()
        font1.setPointSize(40)
        self.grid_layout.addWidget(self.label2, 30, 0)

        self.depart_list = QComboBox()
        self.depart_list.addItem('컴퓨터학부')
        self.depart_list.addItem('전자공학부')
        self.depart_list.addItem('전기공학과')
        self.grid_layout.addWidget(self.depart_list, 30, 10)
        self.depart_list.activated[str].connect(self.select_depart)

        self.label3 = QLabel('현재 설정된 키워드')#현재 설정된 키워드 정보 제목
        font1 = self.label3.font()
        font1.setPointSize(30)
        self.grid_layout.addWidget(self.label3, 0, 10)

        self.label4 = QLabel('')#현재 설정된 키워드 정보
        font1 = self.label4.font()
        font1.setPointSize(20)
        self.grid_layout.addWidget(self.label4, 1, 10)
        now_keyword = ",".join(set_depart.keyword)
        self.label4.setText(now_keyword)

        # 학부홈페이지 설정 창 세팅
        self.setWindowTitle('학부홈페이지 설정')
        self.resize(400,200)

    #추가버튼 클릭시 동작
    def add_action(self) :
        for k in set_depart.keyword:
            if(k == self.addkeyword.text()) : #입력한 키워드가 이미 존재할 경우
                return
        set_depart.keyword.append(self.addkeyword.text())#설정의 keyword에 키워드값 넣기
        now_keyword = ",".join(set_depart.keyword)#gui 출력용
        self.label4.setText(now_keyword)#gui 출력용

    #삭제버튼 클릭시 동작
    def delete_action(self) :
        for k in set_depart.keyword:
            if(k == self.deletekeyword.text()) : #삭제할 키워드가 존재
                set_depart.keyword.remove(self.deletekeyword.text())#설정의 keyword에 키워드값 삭제
        now_keyword = ",".join(set_depart.keyword)#gui 출력용
        self.label4.setText(now_keyword)#gui 출력용        

    #학부선택시 동작
    def select_depart(self, text):
        set_depart.depart = text#설정의 depart에 학부값 넣기
        print(set_depart.depart)#테스트용 출력 나중에 삭제 필요


        

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
        self.button1.clicked.connect(self.crawling_lms_state)#lms on/off버튼에 기능 연결

        self.button2 = QPushButton('설정')
        grid_layout.addWidget(self.button2, 2, 0)

        self.button3 = QPushButton('On/Off')
        grid_layout.addWidget(self.button3, 1, 1)
        self.button3.setCheckable(True)
        self.button3.clicked.connect(self.crawling_depart_state)#depart on/off버튼에 기능 연결

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
        if(set_depart.departupdate_check==1):#알람이 on이였으면
            set_depart.departupdate_check=0#off 시키기
            print('크롤링을 종료합니다')#테스트용 나중에 지울것

        elif(set_depart.departupdate_check==0):#알람이 off이였으면
            set_depart.departupdate_check=1#on 시키기

            print('크롤링을 시작합니다')#테스트용 나중에 지울것
            print(set_depart.departupdate_check)
            set_depart.load()
            for d in set_depart.depart:
                depart_crawl = depart_noti(d)
                crawl_thread_depart = threading.Thread(target = depart_crawl.get_change())
                crawl_thread_depart.start()
                

    def crawling_lms_state(self):#LMS on/off 변경
        if(set_lms.lmsupdate_check==1):#알람이 on이였으면
            set_lms.lmsupdate_check=0#off 시키기
            print('크롤링을 종료합니다')#테스트용 나중에 지울것

        elif(set_lms.lmsupdate_check==0):#알람이 off이였으면
            set_lms.lmsupdate_check=1#on 시키기
            print('크롤링을 시작합니다')#테스트용 나중에 지울것
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = ALARM_Window()
    windowExample.show()
    sys.exit(app.exec_())