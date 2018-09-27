import requests
from bs4 import BeautifulSoup
import operator
import time
import re

def request(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'gall.dcinside.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url_get = requests.get(url, headers=header)
    return url_get

def gall_check(gall):
    recept = request("http://gall.dcinside.com/board/lists/?id=%s" %gall)
    soup = BeautifulSoup(recept.text, "html.parser")
    meta_data = soup.find_all("meta", {"name": "title"})
    comp = re.findall("\".*갤러리", str(meta_data))
    if comp == []:
        return None
    gall_name = comp[0] + "\""
    return gall_name


def main():
    gall = input("갤러리 id?(ex:mlp): ")
    if gall_check(gall):
        print(gall_check(gall))
    else:
        print("id 잘못 입력한듯")
        main()
    init_page = int(input("시작 페이지?: "))
    final_page = int(input("마지막 페이지?: "))
    nick_dic = dict()

    for page in range(init_page, final_page + 1):
        print("\rWorking page={}/{}".format(page, final_page), end="")
        recept = request("http://gall.dcinside.com/board/lists/?id=%s&page=%d" %(gall, page))
        soup = BeautifulSoup(recept.text, "html.parser")
        nick_list = soup.find_all('td', {'class': "gall_writer ub-writer"})

        for nicks in nick_list:
            try:  # 첫부분 예외처리
                nick = nicks.attrs['data-nick']
                uid = nicks.attrs['data-uid']
                ip = nicks.attrs['data-ip']
            except:
                nick = "운영자"
            if nick == "운영자":  # 공지사항
                continue
            nick_str = nick + "(" + uid + ip + ")"
            if nick_str in nick_dic:
                nick_dic[nick_str] += 1
            else:
                nick_dic[nick_str] = 1
    sorted_dic = sorted(nick_dic.items(), key=operator.itemgetter(1))   #딕셔너리 value로 정렬
    sorted_dic.reverse()
    nick_list = sorted_dic
    if input("닉변 처리?(y/n): ") == "y":
        nick_list = nick_change(nick_list)  #닉변 처리
    page_num = final_page - init_page
    file_writer(gall, nick_list, page_num)    #저장


def nick_change(nick_list):
    print("랭킹\t닉\t글수")
    for i in range(len(nick_list)):
        print("%d\t%s\t%s" %((i+1), nick_list[i][0], nick_list[i][1]))
    print("닉변 처리(ex)1위와 10위가 동일닉일 시 1,10 한번에 두개씩만, 종료는 0,0")
    while 1:
        change = input("닉변?: ")
        rankings = change.split(",")
        if rankings[0] == "0":
            break
        temp_1 = nick_list[int(rankings[0]) - 1][0] + "=" + nick_list[int(rankings[1]) - 1][0]
        temp_2 = nick_list[int(rankings[0]) - 1][1] + nick_list[int(rankings[1]) - 1][1]
        temp_3 = nick_list[int(rankings[1]) - 1][0]
        nick_list[int(rankings[0]) - 1] = (temp_1, temp_2)
        nick_list[int(rankings[1]) - 1] = (temp_3, 0)
    return nick_list


def file_writer(gall, nick_list, page_num):
    timestr = time.strftime("%Y_%m_%d-%H_%M")
    file_name = "%s_gall-%s.txt" %(gall, timestr)
    print(file_name)
    f = open(file_name, 'w')
    f.write("갤창랭킹 made by hanel2527, 마이 리틀 포니 갤러리\n")
    total = page_num*49
    f.write("총 글수: %d" %total)
    f.write("랭킹\t닉\t글 수\t갤 지분(%)\n")

    for i in range(len(nick_list)):
        string = "%d\t%s\t%d\t%.2f\n" %((i+1), nick_list[i][0], nick_list[i][1], (nick_list[i][1] / total * 100))
        f.write(string)
    f.close()


if __name__ == "__main__":
    print("갤창랭킹 made by hanel2527, mlp갤")
    main()