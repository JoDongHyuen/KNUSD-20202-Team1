import requests
from bs4 import BeautifulSoup
import time

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

        #기존의 공지사항 번호의 최대값 받아오기
        numbers = soup.find_all(class_="bbs_num")

        for number in numbers:
            if(number.text.isdigit() == 1):
                if(pre_max<int(number.text)):
                    pre_max=int(number.text)
                    break

        print('가장 최근의 공지사항 번호는 ',pre_max, '이다.')
           
        #1분마다 업데이트되는지 체크
        while 1:
            if(update_check==0):
                break

            time.sleep(60)
            print('새로고침')

            req = requests.get(URL)
            html = req.text
            soup = BeautifulSoup(html,'html.parser')

            notis = soup.select('tr' )

            for noti in notis:
                num_html =noti.select('td.bbs_num') #번호 
                for n in num_html:
                    num_max = n.text
                if(num_max == ''):
                    continue

                title_html= noti.select('td>a')   #제목
                for t in title_html:
                    title = t.text

                if(num_max != '공지'):
                        if(num_max == pre_max+1) :
                            break

            if(num_max == pre_max+1):        #변경사항 없음
                print("변경사항있음 : [공지사항]",num_max,":",title)
                pre_max = num_max
            else:                           #변경사항 있음
                print("변경사항없음")
                #print("[공지사항]",num_max,":",title)
    

if __name__ == '__main__':
    noti = depart_noti()
    noti.get_change() 