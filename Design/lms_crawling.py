# parser.py
import requests
import re
from bs4 import BeautifulSoup as bs
from gui_lms import LOGIN_INFO

# id / pwd에 본인 lms 아이디 비번 입력
LOGIN_INFO = {
    'usr_id': '',
    'usr_pwd': ''
}
class lms_notify:
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