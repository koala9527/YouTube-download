import  youtube_dl
import requests
from bs4 import BeautifulSoup
import re
import time


headers={
'Referer': 'https://www.youtube.com/',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}



def getlisturl(url,headers):
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    reg = r'/watch\?v=[a-zA-Z0-9_-]*\\u0026list=[0-9-a-zA-Z-_]*'
    urlre = re.compile(reg)
    urllist = re.findall(urlre,soup.decode('utf-8'))
    l=[]
    for i in urllist:
        if i not in l:
            i=str('https://www.youtube.com'+i.replace("\\u0026",'&'))
            l.append(i)
    return l

def getdownloadurl(url,headers):
    time.sleep(1)
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    detail=soup.find_all('script')

    reg = r'/watch\?v=[a-zA-Z0-9_-]*'
    urlre = re.compile(reg)
    urllist = re.findall(urlre,str(detail[28]))
    l=[]
    for i in urllist:
        i=str('https://www.youtube.com'+i)
        if i not in l:
            l.append(i)
    return l

def download(url):
    try:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception:
        pass

if __name__=="__main__":
    list1=[]
    url = 'https://www.youtube.com/channel/UCSs4A6HYKmHA2MG_0z-F0xw/playlists'
    for i in getlisturl(url, headers):

        list1+=getdownloadurl(i,headers)
    list1=list(set(list1))
    print(list1)
    for i in list1:
        download(i)