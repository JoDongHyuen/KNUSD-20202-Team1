import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class lms_set(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        la1 = QLabel('ID')
        grid_layout.addWidget(la1)
        text = QLineEdit()
        grid_layout.addWidget(text)
        la2 = QLabel('PW')
        grid_layout.addWidget(la2)
        text2 = QLineEdit()
        text2.setEchoMode(QLineEdit.Password)
        grid_layout.addWidget(text2)
        btn=QPushButton('OK')
        grid_layout.addWidget(btn)
        self.setWindowTitle('LMS Login')
        self.setGeometry(300,300,300,100)

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        self.l_s = lms_set()

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
        grid_layout.addWidget(button1, 1, 0)
        button2 = QPushButton('Setting')
        button2.clicked.connect(self.lms_login)
        grid_layout.addWidget(button2, 2, 0)
        button3 = QPushButton('On/Off')
        grid_layout.addWidget(button3, 1, 1)
        button4 = QPushButton('Setting')
        grid_layout.addWidget(button4, 2, 1)
    
        
        self.setWindowTitle('통합 알림 시스템')
        self.setGeometry(500, 500, 500, 300)
        self.show()

    # 버튼 이벤트 함수
    def lms_login(self):
        self.l_s.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = basicWindow()
    window.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())
