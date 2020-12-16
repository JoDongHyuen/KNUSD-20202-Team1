import os

depart_file = "depart.txt"  # 나중에 파일경로 설정해야할수도 있음
keyword_file = "keyword.txt"

class setting_depart: #GUI와 연결해야함

    def __init__(self) :
        #self.depart_num
        self.depart = []
        self.keyword = []

    def load(self):
        #파일에서 설정값들 불러옴

        if os.path.isfile(depart_file): #학부리스트
            f1 = open(depart_file, 'r')
            self.depart = f1.readlines()
            f1.close()

        else: #파일이 존재하지않으면, 만들어서 디폴트값을 넣는다
            f1 = open(depart_file, 'w')
            f1.write('컴퓨터학부')
            f1.close()

        if os.path.isfile(keyword_file): #키워드 리스트
            f2 = open(keyword_file, 'r')
            self.keyword = f2.readlines()
            f2.close()

        else: #키워드 리스트는 디폴트값이 없다
            f2 = open(keyword_file, 'w')
            f2.close()

    def append_keyword(self,keyword): #키워드 추가

        self.keyword.append(keyword)
        f2 = open(keyword_file, 'a')
        f2.write(keyword+'\n')
        f2.close()

    def delete_keyword(self,keyword): #키워드 삭제

        for k in self.keyword:
            if(k==keyword):
                self.keyword.remove(keyword)
                break

        f2 = open(keyword_file, 'w')
        for k in self.keyword:
            f2.write(k)
        f2.close()

    def append_depart(self,depart): #학부 추가

        self.depart.append(depart)
        f1 = open(depart_file, 'a')
        f1.write(depart+'\n')
        f1.close()

    def delete_depart(self,depart): #학부 삭제

        for d in self.depart:
            if(d==depart):
                self.depart.remove(depart)
                break

        f1 = open(keyword_file, 'w')
        for d in self.depart:
            f1.write(d)
        f1.close()