# parser.py
import requests
import re
import shutil
from bs4 import BeautifulSoup as bs

# id / pwd에 본인 lms 아이디 비번 입력
LOGIN_INFO = {
    'usr_id': '',
    'usr_pwd': ''
}

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
    notfi_file = open("new.txt","w",encoding="utf8")
    for i,j in zip(noti.find_all(class_="notification_subject"),noti.find_all(class_="notification_text")):
        
        i = re.sub('<.+?>', '', str(i), 0).strip()
        i = i.replace('\n', '')
        i = i.replace('\t', '')    
        print(i, file=notfi_file)

        j = re.sub('<.+?>', '', str(j), 0).strip()
        j = j.replace('\n', '')
        j = j.replace('\t', '')
        j = j.replace('\r', '')
        title = j.split(' ')
        new = ' '.join(title[1:])
        new = new.lstrip()
        tit = title[0]
        print(tit+'\n'+new+'\n', file=notfi_file)
    notfi_file.close()

#파일 비교하는 부분

file_checker = 1 #f2가 정상적으로 열리면 1, 비정상이면 0의 값을 가짐


new = open("new.txt", "r", encoding="utf8")
#처음에 사용하면 prev.txt가 생성안되어서 try, except로 new.txt를
#prev.txt로 복사하도록 처리하였음
try:
    prev = open("prev.txt", "r", encoding="utf8")
except:
    shutil.copy('new.txt', 'prev.txt')
    file_checker = 0
    pass

if file_checker == 1:
    new_lines = new.readlines()
    prev_lines = prev.readlines()

    for i in range(0,3):
        check = (f1_lines[i] == f2_lines[i])
        if check == False:
            print("변동사항 확인")
            break

    f2.close()
f1.close()