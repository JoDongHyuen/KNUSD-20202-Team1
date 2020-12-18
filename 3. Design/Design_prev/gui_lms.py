import sys
import json
import re
import requests
from bs4 import BeautifulSoup as bs
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


LOGIN_INFO = {
    'usr_id': '',
    'usr_pwd': ''
}

class lms_login(QWidget):
    def __init__(self):
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

    def pushButtonClicked(self):
        self.id = self.text1.text()
        self.pwd = self.text2.text()
        LOGIN_INFO['usr_id'] = self.id
        LOGIN_INFO['usr_pwd'] = self.pwd
        with requests.session() as s:
        
            login_check = 0

            #로그인에 실패하면 login에 isError 가 True로 나타나서 이걸 이용해 exception 처리 예정
            login_req = s.post('https://lms.knu.ac.kr/ilos/lo/login.acl', data=LOGIN_INFO)
            login = login_req.text
            login = json.loads(login)
            if(login['isError'] == False):
                self.close()
            else:
                QMessageBox.question(self,'Message','ID/PW를 확인하십시오',QMessageBox.Ok)

        #self.close()

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        self.lms_login = lms_login()

        label1 = QLabel('LMS')
        font = label1.font()
        font.setPointSize(30)
        label1.setFont(font)
        label1.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(label1, 0, 0)

        label2 = QLabel('학부')
        label2.setFont(font)
        grid_layout.addWidget(label2, 0, 1)
        label2.setAlignment(Qt.AlignCenter)
        
        button1 = QPushButton('On/Off')
        button1.clicked.connect(self.lms_notify)
        grid_layout.addWidget(button1, 1, 0)
        
        button2 = QPushButton('Setting')
        button2.clicked.connect(self.pushButtontoLogin)
        grid_layout.addWidget(button2, 2, 0)

        button3 = QPushButton('On/Off')
        grid_layout.addWidget(button3, 1, 1)
        
        button4 = QPushButton('Setting')
        grid_layout.addWidget(button4, 2, 1)
    
        
        self.setWindowTitle('통합 알림 시스템')
        self.setGeometry(500, 500, 500, 300)
        self.show()

    # 버튼 이벤트 함수
    def pushButtontoLogin(self):
        self.lms_login.show()

    def lms_notify(self):
        with requests.session() as s:
        
            login_check = 0

            #print(LOGIN_INFO)

            #로그인에 실패하면 login에 isError 가 True로 나타나서 이걸 이용해 exception 처리 예정
            login_req = s.post('https://lms.knu.ac.kr/ilos/lo/login.acl', data=LOGIN_INFO)
            login = login_req.text
            #print(login)

            #로그인 후 알림 창을 스크래핑하는 부분
            notification = s.get('https://lms.knu.ac.kr/ilos/mp/notification_list.acl')
            noti = bs(notification.content, 'html.parser')
            for i,j,k in zip(noti.find_all(class_="notification_subject"),noti.find_all(class_="notification_text"), noti.find_all(class_="notification_day")):
                i = re.sub('<.+?>', '', str(i), 0).strip()
                i = i.replace('\n', '')
                i = i.replace('\t', '')
                print(i)

                j = re.sub('<.+?>', '', str(j), 0).strip()
                j = j.replace('\n', '')
                j = j.replace('\t', '')
                j = j.replace('\r', '')
                title = j.split(' ')
                new = ' '.join(title[1:])
                new = new.lstrip()
                tit = title[0]
                print(tit+'\n'+new)

                k = re.sub('<.+?>', '', str(k), 0).strip()
                k = k.replace('\n', '')
                k = k.replace('\t', '')
                print(k)
                print('\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = basicWindow()
    window.show()
    sys.exit(app.exec_())