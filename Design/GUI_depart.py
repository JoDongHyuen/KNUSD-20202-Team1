import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from setting_depart import keyword
#from setting_depart import depart

keyword = []

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
        self.btnadd.clicked.connect(self.addaction)#버튼에 기능 연결

        self.btndelete = QPushButton('삭제')
        self.grid_layout.addWidget(self.btndelete, 20, 10)
        self.btndelete.clicked.connect(self.deleteaction)#버튼에 기능 연결

        self.label2 = QLabel('학부 선택')
        font1 = self.label2.font()
        font1.setPointSize(40)
        self.grid_layout.addWidget(self.label2, 30, 0)

        self.depart_list = QComboBox()
        self.depart_list.addItem('컴퓨터학부')
        self.depart_list.addItem('전자공학부')
        self.depart_list.addItem('전기공학과')
        self.grid_layout.addWidget(self.depart_list, 30, 10)

        self.label3 = QLabel('현재 설정된 키워드')#현재 설정된 키워드 정보 제목
        font1 = self.label3.font()
        font1.setPointSize(30)
        self.grid_layout.addWidget(self.label3, 0, 10)

        self.label4 = QLabel('')#현재 설정된 키워드 정보
        font1 = self.label4.font()
        font1.setPointSize(30)
        self.grid_layout.addWidget(self.label4, 1, 10)
        now_keyword = ",".join(keyword)
        self.label4.setText(now_keyword)

        # 학부홈페이지 설정 창 세팅
        self.setWindowTitle('학부홈페이지 설정')
        self.resize(400,200)

    #추가버튼 클릭시 동작
    def addaction(self) :
        keyword.append(self.addkeyword.text())
        now_keyword = ",".join(keyword)
        self.label4.setText(now_keyword)


    #삭제버튼 클릭시 동작
    def deleteaction(self) :
        for k in keyword:
            if(k == self.deletekeyword.text()) : #삭제할 키워드가 존재
                keyword.remove(self.deletekeyword.text())
        now_keyword = ",".join(keyword)
        self.label4.setText(now_keyword)        
        
        

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

        self.button2 = QPushButton('설정')
        grid_layout.addWidget(self.button2, 2, 0)

        self.button3 = QPushButton('On/Off')
        grid_layout.addWidget(self.button3, 1, 1)
        self.button3.setCheckable(True)

        self.button4 = QPushButton('설정')
        grid_layout.addWidget(self.button4, 2, 1)
        self.button4.clicked.connect(self.d_setting)

        # initUI 세팅
        self.setWindowTitle('통합 알림 시스템')
        self.resize(400,200)
        self.show()

    def d_setting(self):
        self.d_s.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = ALARM_Window()
    windowExample.show()
    sys.exit(app.exec_())