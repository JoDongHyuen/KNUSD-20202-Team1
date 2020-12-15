# parser.py
import requests
import re
from bs4 import BeautifulSoup as bs

# id / pwd에 본인 lms 아이디 비번 입력
LOGIN_INFO = {
    'usr_id': '',
    'usr_pwd': ''
}

with requests.session() as s:
    
    login_check = 0

    print(LOGIN_INFO)

    #로그인에 실패하면 login에 isError 가 True로 나타나서 이걸 이용해 exception 처리 예정
    login_req = s.post('https://lms.knu.ac.kr/ilos/lo/login.acl', data=LOGIN_INFO)
    login = login_req.text
    print(login)


    alarm = s.get('https://lms.knu.ac.kr/ilos/main/main_form.acl')
    html = alarm.text
    soup = bs(html,'html.parser')
    

    #만약 정상적으로 로그인 되었다면 html.txt 파일에 본인 이름을 찾을 수 있음
    score_file = open("html.txt", "w", encoding="utf8")
    print(html, file = score_file)
    score_file.close()


    pkg_list = soup.select('div[class=site-map-box]')
    print(pkg_list)
    

    #로그인 후 알림 창을 스크래핑하는 부분
    notification = s.get('https://lms.knu.ac.kr/ilos/mp/notification_list.acl')
    notification_html = notification.text
    soup = bs(notification_html, 'html.parser')

    score_file = open("notfi.txt","w",encoding="utf8")
    
    notification_html = re.sub('<.+?>', '', notification_html, 0).strip()
    print(notification_html)
    print(notification_html, file = score_file)
    score_file.close()