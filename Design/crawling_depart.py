import requests, time
from bs4 import BeautifulSoup

from setting_depart import *

URL = 'https://computer.knu.ac.kr/06_sub/02_sub.html' #여기에 다른학부 URL도 추가가능

class depart_noti :
    #def __init__(self) :

    def get_change(self):
        req = requests.get(URL)
        html = req.text
        soup = BeautifulSoup(html,'html.parser')

        update_check=1
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
            if(update_check==0): #ON/OFF에서 OFF시 update_check = 0으로 할예정
                break

            time.sleep(60)
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
                
            else:                           #변경사항 없을때, 아무것도 안함
                print("변경사항없음")
    
    def check_keyword(self,title):
        setting.load()

        if not setting.keyword:   #키워드리스트 설정안했을때
            print("변경사항있음 : [공지사항]",num_max,":",title)
            pre_max = num_max

        else:                      #키워드리스트 설정했을때
            include_keyword = 0

            for keyword in setting.keyword :
                if keyword in title:    #키워드하나가 포함됨
                    include_keyword = 1
                    print("변경사항있음 : [공지사항]",num_max,":",title,", 키워드 : ",keyword)
                    break

            if include_keyword == 0: #테스트 전용, 원래는 키워드 포함되어있지않으면, 아무것도안함
                print("변경사항있지만, 키워드포함 x : [공지사항]",num_max,":",title) 

#테스트용
#if __name__ == '__main__':
#    noti = depart_noti()
#    noti.get_change() 