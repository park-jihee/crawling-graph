import requests
from bs4 import *
import matplotlib.pyplot as p

def input_company(): # 정보 입력 받는 함수

    days = int(input("종가 추출 기간을 입력하세요 : "))

    while not days > 0 : # 예외처리 - 0보다 큰 수를 입력할 때까지 반복
        days = int(input("잘못 입력하셨습니다. 자연수를 입력하세요\n" + \
                         "종가 추출 기간을 입력하세요 : "))

    page = days // 20 # 짝대기 두 번 쓰면 정수만 뽑아낸다

    if days > page * 20: # 뽑아올 페이지 수 구하기
        page = page + 1

    c_index = int(input("1:samsung, 2:lge, 3:hynix, 4:naver, 5:hyun_car\n" + \
                        "회사 번호를 입력하세요 : "))

    while not 0 < c_index < 6 : # 예외처리 - 0보다 크고 6보다 작은 수를 입력할 떄까지 반복
        c_index = int(input("잘못 입력하셨습니다. 1 ~ 5 사이의 숫자를 입력하세요\n" +\
                            "1:samsung, 2:lge, 3:hynix, 4:naver, 5:hyun_car\n" + \
                            "회사 번호를 입력하세요 : "))
        

    company = ['005930', '066570', '000660', '035420', '005380'] # 각 회사별 코드
    url = 'https://finance.naver.com/item/frgn.nhn?code={}&page='.format(company[c_index-1]) # {}안에 회사별 코드 넣어준다

    name_list = ['samsung', 'lge', 'hynix', 'naver', 'hyun_car'] # 회사 이름이 담긴 List
    name = name_list[c_index-1] # index값과 맞추기 위해 -1을 한다

    return page, url, name # 값을 보내줄 수 있도록 보낸다


def make_pList(url, page): # html파일안에서 정보 가져오는 함수

    pList = []

    for i in range(1, page + 1):
        wp = requests.get(url + str(i))

        soup = BeautifulSoup( wp.text, 'html.parser' ) # BeautifulSoup - html파일을 가져올 수 있다

        trList = soup.find_all('tr', {'onmouseover':"mouseOver(this)"}) # 주어진 조건에 해당되는 정보들을 List에 담는다
        for tr in trList: 
            td = tr.find_all('td')[1].get_text() # 2번째에 td에 text를 가져온다
            td = td.replace(",", "") # text안에 ,뺴준다
            pList.append(int(td)) # pList에 넣어준다
            
    pList.reverse() # List안에 정보들을 뒤집어서 과거 ~ 현재 순으로 정렬
    return pList


def make_avg(numMA, pList): # 이동평균 구하는 함수

    mList = list();
    Q = list();
    mSum = pList[0] * numMA
    
    for i in range(numMA):
        Q.append(pList[0])

    for price in pList:
        mSum = mSum - Q.pop(0)
        mSum = mSum + price
        mList.append(mSum / numMA)
        Q.append(price)

    return mList


def print_avg(name, pList): # 그래프 그리는 함수

    xAxis = list(range(1, len(pList) + 1))

    p.plot(xAxis, pList, 'r', label = name)
    p.plot(xAxis, make_avg(5, pList), 'b', label = '5MA')
    p.plot(xAxis, make_avg(20, pList), 'g', label = '20MA')
    p.plot(xAxis, make_avg(60, pList), 'y', label = '60MA')
    p.xlabel('Day')
    p.ylabel('Last Price')
    p.grid(True)
    p.legend(loc = 'upper right')
    p.show()