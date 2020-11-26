from bs4 import BeautifulSoup
import urllib.request as req
import time
check=1
max=0
baseURL = 'https://computer.knu.ac.kr/06_sub/02_sub.html'
res = req.urlopen(baseURL)
soup = BeautifulSoup(res,'html.parser')
numbers = soup.find_all(class_="bbs_num")
#titles = soup.find_all(style_="text-align:left;")
#print(titles)
for number in numbers:
    if(number.text.isdigit() == 1):
        if(max<int(number.text)):
            max=int(number.text)      
m=max
print(max)

#print(titles)       
while 1:
    if(check==0):
        break
    time.sleep(60)
    print('새로고침')
    res = req.urlopen(baseURL)
    soup = BeautifulSoup(res,'html.parser')
    numbers = soup.find_all(class_='bbs_num')
    for number in numbers:
        if(number.text.isdigit() == 1):
            if(max<int(number.text)):
                max=int(number.text)
    if m<max:
        print("공지사항 번호가 ",max,"번인 새로운 공지사항 올라왔다")
        m=max
    