import requests, time, threading, os
from win10toast import ToastNotifier
from bs4 import BeautifulSoup

history_file = "./DB/history_depart.txt" #알림 내역들

URL_dic = {'컴퓨터학부' : 'https://computer.knu.ac.kr/06_sub/02_sub.html',
           '전자공학부' : 'https://see.knu.ac.kr/content/board/notice.html',
           '전기공학과' : 'https://electric.knu.ac.kr/HOME/electric/sub.htm?nav_code=ele1465563397'
    }
tagnum_dic = {'컴퓨터학부' : "td.bbs_num", #학부홈페이지마다 태그다름
              '전자공학부' : "td.row", #전자공학부는 태그형식이 다름
              '전기공학과' : "td.fst"
              
    }


class depart_noti :
    def __init__(self,depart) :
        self.depart = depart
        self.noti_depart = ''

        self.num_max = 0
        self.pre_max = 0

        self.toaster = ToastNotifier()

        
    def alarm_depart_wait(self,depart_alarm_on,set_depart): #학부 setting값을 인자로 받음, 
        req = requests.get(URL_dic[self.depart])
        html = req.text
        soup = BeautifulSoup(html,'html.parser')

        #가장 최근의 공지사항 번호 받아오기
        #numbers = soup.find_all(class_="bbs_num")
        numbers = soup.select(tagnum_dic[self.depart])
        self.load_recent(numbers)

        #1분마다 업데이트되는지 체크
        while depart_alarm_on[0] == 1:  #ON/OFF에서 OFF시 update_check = 0으로 함
            print('가장 최근의 공지사항 번호는 ',self.pre_max, '이다.')
            time.sleep(60) #60초

            req = requests.get(URL_dic[self.depart])
            
            html = req.text
            soup = BeautifulSoup(html,'html.parser')

            notis = soup.select('tr' ) #tr태그 목록들

            self.get_change_depart(notis,set_depart)

    def get_change_depart(self,notis,set_depart): #변경사항 확인
        num_txt = ''
        title = ''

        for noti in notis:      
            num_html =noti.select(tagnum_dic[self.depart]) #tr태그에서 공지사항 번호

            for n in num_html:
                num_txt = n.text 
            if(len(num_txt)==0 or num_txt == ''  or num_txt == '공지' ):
                continue
                
            self.num_max = int(num_txt)

            title_html= noti.select('td>a')   #tr태그에서 공지사항 제목
            for t in title_html:
                title = t.text

            if(self.num_max != '공지'): 
                if(self.num_max == self.pre_max+1) : #예를들어 가장 최근 공지사항이 2983번일때, 2984번이 있으면 변경사항 체크
                    break

        if(self.num_max == self.pre_max+1):        #변경사항 있을때, 키워드 체크
            self.process_noti(title,set_depart[0])
                
        else:                           #변경사항 없을때, 아무것도 안함, 밑에 출력은 테스트용
            print("[변경사항없음]"+'['+self.depart+']')

    def process_noti(self,title,set_depart): #키워드 체크+알림 가공
        set_depart.load()
        title = title.replace('\t', '')
        title = title.replace('\r', '')
        title = title.replace('\n', '')

        if not set_depart.keyword:   #키워드리스트 설정안했을때
            self.noti_depart = str(self.num_max)+"["+self.depart+"] "+" : "+title
            self.send_noti(self.depart,self.noti_depart)

            print("[변경사항있고, 키워드설정x]"+self.noti_depart)
            self.store_history(self.noti_depart)

        else:                      #키워드리스트 설정했을때
            include_keyword = 0

            for keyword in set_depart.keyword :
                if keyword in title:    #키워드하나가 포함됨
                    include_keyword = 1
                    self.noti_depart = str(self.num_max)+"["+self.depart+"] "+" : "+title+", 키워드 : "+keyword
                    self.send_noti(self.depart,self.noti_depart)

                    print("[변경사항있고, 키워드포함o]"+self.noti_depart)
                    self.store_history(self.noti_depart)
                    break

            if include_keyword == 0: #테스트 전용, 원래는 키워드 포함되어있지않으면, 아무것도안함
                print("[변경사항있지만, 키워드포함 x]"+str(self.num_max)+"["+self.depart+"]"+":",title) 

        self.pre_max = self.num_max

    def send_noti(self,depart,noti): #윈도우10 알림창에 공지사항 알림 보냄
        title = depart + ' 홈페이지'
       
        try:
            self.toaster.show_toast(title,noti,icon_path = '', duration =None, threaded = False) 
        except :
            pass

        

    def store_history(self,noti): #알림내역 저장
        f1 = open(history_file, 'a')
        f1.write(noti+'\n')
        f1.close()

    def load_recent(self,numbers): 
         if os.path.isfile(history_file) and os.stat(history_file).st_size>0: #제일 최근 알림내역에서 공지사항 번호 추출
            f1 = open(history_file, 'r')
            notis = f1.readlines()
            f1.close()
            last_noti = notis[len(notis)-1]
            self.pre_max = int(last_noti[0]+last_noti[1]+last_noti[2]+last_noti[3])

         else: #파일이 존재하지않으면, 만들어서 디폴트값을 넣는다
            f1 = open(history_file, 'w')

            for number in numbers:
                if(number.text.isdigit() == 1):
                    if(self.pre_max<int(number.text)):
                        self.pre_max=int(number.text)
                        break
            f1.write(str(self.pre_max)+"\n")
            f1.close()