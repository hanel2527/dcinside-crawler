import requests
from bs4 import BeautifulSoup
import operator
import datetime

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

def main():
    print("갤창랭킹 made by hanel2527, mlp갤")
    gall = input("갤러리 id?(ex:mlp): ")
    init_page = int(input("시작 페이지?: "))
    final_page = int(input("마지막 페이지?: "))
    nick_dic = dict()

    for page in range(init_page, final_page + 1):
        print("\rWorking page={}/{}".format(page, final_page), end="")
        nick_listing = list()
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
    print(nick_dic)
    file_writer(nick_dic)


def file_writer(nick_dic):
    present_time = datetime.date.today()
    file_name = "gallchang%s.txt" %present_time
    print(file_name)
    f = open(file_name, 'w')
    f.write("갤창랭킹 made by hanel2527, 마이 리틀 포니 갤러리\n")
    f.write("랭킹\t닉\t글수\n")
    sorted_dic = sorted(nick_dic.items(), key=operator.itemgetter(1))
    sorted_dic.reverse()
    for i in range(len(sorted_dic)):
        string = "%d\t%s\t%s\n" %((i+1), sorted_dic[i][0], sorted_dic[i][1])
        f.write(string)
    f.close()


if __name__ == "__main__":
    main()
