import os


login_file = "lms.txt" # 나중에 파일경로 설정해야할수도 있다

class setting_lms: #GUI와 연결해야함, lms역할분들이 참고할수있습니다.

    def __init__(self) :
        self.ID = ''
        self.PW = ''
        self.secret_PW = ''
        self.lmsupdate_check = 0#lms의 현재 알람 on/off 상태 디폴트는 off인 0

    def load(self):  #파일에서 설정들 불러옴
       
        if os.path.isfile(login_file):
            f1 = open(login_file, 'r')
            self.ID = f1.readline()
            self.secret_PW = f1.readline()
            self.decode_pw() #복호화
            f1.close()

        else: #파일이 존재하지않으면, 만든다, 디폴트값 없음
            f1 = open(login_file, 'w')
            f1.close()

    def set_login(self,ID,PW): #로그인 정보 설정후, 파일에 저장

        self.ID = ID
        self.PW = PW
        f1 = open(login_file, 'w')
        f1.write(ID)
        self.encode_pw() #암호화
        f1.write(self.secret_PW)
        f1.close()


    def encode_pw(self):
        #비밀번호 암호화 : i번째 글자의 아스키코드에 i를 빼서 저장한다
        self.secret_PW = ''

        for i in range(len(self.PW)):
            c = self.PW[i]
            ac = ord(c)
            ac -= i
            c = chr(ac)
            self.secret_PW += c

    def decode_pw(self):
        #비밀번호 복호화 : i번째 글자의 아스키코드에 i를 더해서 불러온다
        self.PW = ''

        for i in range(len(self.secret_PW)):
            c = self.secret_PW[i]
            ac = ord(c)
            ac += i
            c = chr(ac)
            self.PW += c