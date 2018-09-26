import requests
from bs4 import BeautifulSoup

#마이리틀포니 갤러리 첫 페이지만 추출

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


url = "http://gall.dcinside.com/board/lists/?id=mlp"

recept = request(url)
#print(recept.text)     #테스트용

soup = BeautifulSoup(recept.text, "html.parser")
nick_list = soup.find_all('td', {'class': "gall_writer ub-writer"})

#print(nick_list)   #테스트용
#print(nick_list[16].attrs)     #테스트용

for nicks in nick_list:
    try:    #첫부분 예외처리
        nick = nicks.attrs['data-nick']
        uid = nicks.attrs['data-uid']
        ip = nicks.attrs['data-ip']
    except:
        nick = "운영자"
    if nick == "운영자":   #공지사항
        continue
    print(nick, uid, ip)

