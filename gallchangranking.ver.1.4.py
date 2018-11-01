import requests
from bs4 import BeautifulSoup
import operator
import time
import re
import os

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
    try:
        url_get = requests.get(url, headers=header)
    except:
        url_get = requests.get(url, headers=header)
    return url_get

def gall_check(mg: bool, gall: str) -> (bool, str):
    if mg:
        recept = request("http://gall.dcinside.com/board/lists/?id=%s" %gall)
    else:
        recept = request("http://gall.dcinside.com/mgallery/board/lists?id=%s" %gall)
    soup = BeautifulSoup(recept.text, "html.parser")
    meta_data = soup.find_all("meta", {"name": "title"})
    comp = re.findall("\"(.*갤러리)", str(meta_data))
    if comp == []:
        if mg != True:
            return (False, "망갤")
        else:
            return gall_check(False, gall)
    else:
        gall_name = comp[0]
        tuple = (mg, gall_name)
        return tuple


def main():
    gall = input("갤러리 id?(정식, 마이너갤 자동 구분)(ex:mlp): ")
    (mg, gall_name) = gall_check(True, gall)

    if gall_name != "망갤":
        print(gall_name)
    else:
        print("id 잘못 입력한듯")
        main()
    init_page = int(input("시작 페이지?: "))
    final_page = int(input("마지막 페이지?: "))
    nick_dic = dict()

    for page in range(init_page, final_page + 1):
        print("\rWorking page={}/{}".format(page, final_page), end="")
        if mg:
            recept = request("http://gall.dcinside.com/board/lists/?id=%s&page=%d" %(gall, page))
        else:
            recept = request("http://gall.dcinside.com/mgallery/board/lists/?id=%s&page=%d" %(gall, page))
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
    nick_list = dict_sorter(nick_dic)
    file_writer(gall, nick_list)    #저장


def dict_sorter(nick_dic):
    sorted_dic = sorted(nick_dic.items(), key=operator.itemgetter(1))   #딕셔너리 value로 정렬
    sorted_dic.reverse()
    return sorted_dic


def nick_search(nick_list, item1, item2):
    for i in range(len(nick_list)):
        if item2 == "없음없음없음":
            if (nick_list[i][0].find(item1) != -1):
                print(i+1, nick_list[i][0], " | ", end="\t")
        elif (nick_list[i][0].find(item1) != -1) or (nick_list[i][0].find(item2) != -1):
            print(i+1, nick_list[i][0], " | ", end="\t")
    print()


def nick_change(nick_list):
    print("랭킹\t닉\t글수")
    for i in range(len(nick_list)):
        print("%d\t%s\t%s" %((i+1), nick_list[i][0], nick_list[i][1]))
    print("닉변 처리(ex)1위, 3위, 10위가 동일인일시 1 3 10(띄어쓰기로 구분)")
    print("닉, 아이디 검색(ex): search hanel2527 (hanel2527을 검색)")
    print("두 개 동시에 검색(ex): search hanel2527 twilight (띄어쓰기로 구분)")
    print("종료는 0")
    while 1:
        change = input("닉변?: ")
        rankings = change.split()
        if rankings[0] == "0":
            break
        elif rankings[0] == "search":
            if len(rankings) == 2:
                nick_search(nick_list, rankings[1], "없음없음없음")
            else:
                nick_search(nick_list, rankings[1], rankings[2])
            continue
        else:
            for i in range(len(rankings)):
                rankings[i] = int(rankings[i])
            nick_list = nick_change_multiple(rankings, nick_list)
    temp_dic = dict(nick_list)
    nick_list = dict_sorter(temp_dic)
    return nick_list


def nick_change_multiple(rankings, nick_list):
    while 1:
        if len(rankings) < 2:
            break
        else:
            original = nick_list[rankings[0] - 1][0]
            plus_nick = nick_list[rankings[1] - 1][0]
            temp_1 = original + "=" + plus_nick
            temp_2 = nick_list[rankings[0] - 1][1] + nick_list[(rankings[1]) - 1][1]
            nick_list[(rankings[0]) - 1] = (temp_1, temp_2)
            nick_list[(rankings[1]) - 1] = (plus_nick, 0)
            rankings.pop(1)
    return nick_list


def file_writer(gall, nick_list):
    timestr = time.strftime("%Y_%m_%d-%H_%M")
    file_name = "%s_gall-%s.txt" %(gall, timestr)
    edit_file_name = "edit_%s_gall-%s.txt" %(gall, timestr)
    print(file_name)
    f = open(file_name, 'w')
    ef = open(edit_file_name, "w")
    f.write("갤창랭킹 made by hanel2527, 마이 리틀 포니 갤러리\n")
    total = 0
    for i in range(len(nick_list)):
        total += nick_list[i][1]
    f.write("총 글수: %d\n" %total)
    f.write("랭킹\t닉\t글 수\t갤 지분(%)\n")
    error = 0
    for i in range(len(nick_list)):
        if nick_list[i][1] == 0:
            continue
        string = "%d\t%s\t%d\t%.2f\n" %((i+1), nick_list[i][0], nick_list[i][1], (nick_list[i][1] / total * 100))
        try:
            f.write(string)
            ef.write("%s\t%d\n" %(nick_list[i][0], nick_list[i][1]))
        except:
            error += nick_list[i][1]
            f.write(str(error))
    f.close()
    ef.close()

def edit_nick():
    filename_list = list()
    n = 0
    for filename in os.listdir():
        if re.match("^edit_.*\.txt", filename):
            n += 1
            print(n, filename)
            filename_list.append(filename)
    num = int(input("맞는 것 번호?: "))
    file_name = filename_list[num - 1]
    print(file_name)
    f = open(file_name, "r")
    nicks = f.readlines()
    nick_list = list()
    for i in range(len(nicks)):
        temp = nicks[i].split('\t')
        nick_list.append((temp[0], int(temp[1])))
    nick_list = nick_change(nick_list)  #닉변
    gall = re.findall("^edit_(.*)_gall", file_name)[0]
    file_writer(gall, nick_list)
    f.close()
    original = re.findall("^edit_(.*\.txt)", file_name)[0]
    if input("원본파일 삭제?(y/n): ") == "y":
        os.remove(original)     #원본파일 삭제
        os.remove(file_name)


if __name__ == "__main__":
    print("갤창랭킹 made by hanel2527, mlp갤")
    if input("갤창랭킹/편집(g/e): ") == "g":
        main()
    edit_nick() #닉변처리
