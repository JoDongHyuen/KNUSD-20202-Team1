import requests, time, threading
from win10toast import ToastNotifier
from bs4 import BeautifulSoup

from setting_depart import * 

URL = 'https://computer.knu.ac.kr/06_sub/02_sub.html' #여기에 다른학부 URL도 추가가능

class depart_noti :
    def __init__(self,depart) :
        self.depart = depart
        self.noti = ''
        self.send_thread_list = [] #각 알림을 쓰레드를 사용하고, 쓰레드들의 리스트

    def get_change(self):
        req = requests.get(URL)
        html = req.text
        soup = BeautifulSoup(html,'html.parser')

        departupdate_check=1
        pre_max =0
        num_max=0
        title = ''

        #가장 최근의 공지사항 번호 받아오기
        numbers = soup.find_all(class_="bbs_num")

        for number in numbers:
            if(number.text.isdigit() == 1):
                if(pre_max<int(number.text)):
                    pre_max=int(number.text)
                    break

        print('가장 최근의 공지사항 번호는 ',pre_max, '이다.')
        
        #setting_depart 파일의 클래스
        setting = setting_depart() 

        #1분마다 업데이트되는지 체크
        while 1:
            if(departupdate_check==0): #ON/OFF에서 OFF시 update_check = 0으로 할예정
                break

            time.sleep(2)
            print('새로고침')

            req = requests.get(URL)
            html = req.text
            soup = BeautifulSoup(html,'html.parser')

            notis = soup.select('tr' ) #tr태그 목록들

            for noti in notis:
                num_html =noti.select('td.bbs_num') #tr태그에서 공지사항 번호
                for n in num_html:
                    num_max = n.text
                if(num_max == ''):
                    continue

                title_html= noti.select('td>a')   #tr태그에서 공지사항 제목
                for t in title_html:
                    title = t.text

                if(num_max != '공지'): 
                        if(num_max == pre_max+1) : #예를들어 가장 최근 공지사항이 2983번일때, 2984번이 있으면 변경사항 체크
                            break

            if(num_max == pre_max+1):        #변경사항 있을때, 키워드 체크
                check_keyword(self,title)
                
            else:                           #변경사항 없을때, 아무것도 안함, 밑에 출력은 테스트용
                self.noti = "변경사항없음"
                send_thread = threading.Thread(target = self.send_noti, args = (self.depart, self.noti))
                self.send_thread_list.append(send_thread)
                send_thread.start()

                print(self.noti)
    
    def check_keyword(self,title):
        setting.load()

        if not setting.keyword:   #키워드리스트 설정안했을때
            self.noti = "변경사항있음 : [공지사항]",num_max,":",title
            send_thread = threading.Thread(target = self.send_noti, args = (self.depart, self.noti))
            self.send_thread_list.append(send_thread)
            send_thread.start()

            print(self.noti)
            pre_max = num_max

        else:                      #키워드리스트 설정했을때
            include_keyword = 0

            for keyword in setting.keyword :
                if keyword in title:    #키워드하나가 포함됨
                    include_keyword = 1

                    self.noti = "변경사항있음 : [공지사항]",num_max,":",title,", 키워드 : ",keyword
                    send_thread = threading.Thread(target = self.send_noti, args = (self.depart, self.noti))
                    self.send_thread_list.append(send_thread)
                    send_thread.start()

                    print(self.noti)
                    break

            if include_keyword == 0: #테스트 전용, 원래는 키워드 포함되어있지않으면, 아무것도안함
                print("변경사항있지만, 키워드포함 x : [공지사항]",num_max,":",title) 

    def send_noti(self,depart,noti): #윈도우10 알림창에 공지사항 알림 보냄
        toaster = ToastNotifier()
        title = depart + ' 홈페이지'
        toaster.show_toast(title,noti,icon_path = None, duration = 3600, threaded = False) #3600초 알림지속
        

#테스트용
if __name__ == '__main__':
    noti = depart_noti("컴퓨터학부")
    noti.get_change() 