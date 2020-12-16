# parser.py
import requests,re,time, shutil
import os
from bs4 import BeautifulSoup as bs
from win10toast import ToastNotifier

# id / pwd에 본인 lms 아이디 비번 입력
LOGIN_INFO = {
    'usr_id': '',
    'usr_pwd': ''
}

prev_file = "prev_lms.txt" #이전 알림 내역들
new_file = "new_lms.txt" #비교할 알림 내역들
toaster = ToastNotifier()

def lms_notify(lmsupdate_check,set_lms):

    toaster = ToastNotifier()
    LOGIN_INFO['usr_id'] = set_lms[0].ID
    LOGIN_INFO['usr_pwd'] = set_lms[0].PW


    #1분마다 업데이트되는지 체크
    while lmsupdate_check[0] == 1:
        time.sleep(3) #60초
        notfi_file = open("new_lms.txt","w",encoding="utf8")
        with requests.session() as s:
            login_check = 0

            #print(LOGIN_INFO)

            #로그인에 실패하면 login에 isError 가 True로 나타나서 이걸 이용해 exception 처리 예정
            login_req = s.post('https://lms.knu.ac.kr/ilos/lo/login.acl', data=LOGIN_INFO)
            login = login_req.text

            #로그인 후 알림 창을 스크래핑하는 부분
            notification = s.get('https://lms.knu.ac.kr/ilos/mp/notification_list.acl')
            noti = bs(notification.content, 'html.parser')
            
        

            for i,j in zip(noti.find_all(class_="notification_subject"),noti.find_all(class_="notification_text")):

                i = re.sub('<.+?>', '', str(i), 0).strip()
                i = i.replace('\n', '')
                i = i.replace('\t', '')
                #print(i)
                print(i, file=notfi_file)
                
                j = re.sub('<.+?>', '', str(j), 0).strip()
                j = j.replace('\n', '')
                j = j.replace('\t', '')
                j = j.replace('\r', '')
                title = j.split(' ')
                new = ' '.join(title[1:])
                new = new.lstrip()
                tit = title[0]
                #print(tit+'\n'+new)
                print(tit+'\n'+new+'\n', file=notfi_file)
                
                # k = re.sub('<.+?>', '', str(k), 0).strip()
                # k = k.replace('\n', '')
                # k = k.replace('\t', '')
                # #print(k+'\n')
                # print(k+'\n',file = notfi_file)
             
        notfi_file.close()

        compare_file(toaster)

def compare_file(toaster): #파일 비교하는 부분

    file_checker = 1 #f2가 정상적으로 열리면 1, 비정상이면 0의 값을 가짐
    
    new = open("new_lms.txt", "r", encoding="utf8")
    #처음에 사용하면 prev.txt가 생성안되어서 try, except로 new.txt를
    #prev.txt로 복사하도록 처리하였음
    try:
        prev = open("prev_lms.txt", "r", encoding="utf8")
    except:
        shutil.copy("new_lms.txt","prev_lms.txt")
        file_checker = 0
        pass

    if file_checker == 1:
        new_lines = new.readlines()
        prev_lines = prev.readlines()

        for i in range(0,3):
            check = (new_lines[i] == prev_lines[i])
            
            if check == False:
                print("[LMS 변동사항 확인]")
                alarm_string = new_lines[0] + new_lines[1] + new_lines[2]
                send_noti(alarm_string,toaster)
                shutil.copy("new_lms.txt","prev_lms.txt")
                break

        prev.close()
    new.close()


def send_noti(noti,toaster): #윈도우10 알림창에 공지사항 알림 보냄

    title = 'LMS 알림'

    try:   
        toaster.show_toast(title,noti,icon_path = None, duration =None, threaded=False) #3600초 알림지속
    except:
        pass