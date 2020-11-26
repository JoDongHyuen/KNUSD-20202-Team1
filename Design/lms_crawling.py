# parser.py
import requests
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
    

    #여기 밑에서부터는 로그인 성공한 세션이라 크롤링 코드 짜면 됨




