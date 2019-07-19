import requests
import os
import time
from bs4 import BeautifulSoup
import datetime

date=datetime.datetime.now().strftime('%Y-%m-%d')
with open("url.txt", "r")as f:
    url_list=f.readlines()
    f.close() 
print(url_list)

headers = {'Referer': 'http://cl.y4e.xyz/thread0806.php?fid=7',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
           }
for url in url_list:
    url = url.replace("\n", "")
    if len(url) == 0:
        continue
    re = requests.get(url,headers=headers)
    re.encoding = "gb18030"
    soup = BeautifulSoup(re.text, "html.parser")
    title = soup.title.text.split("- ")[0].replace(" ", "")
    print(title)
    #print(re.text)
    img_list = soup.select("[data-src]")
    #print(img_list)

    if os.path.exists(date+"/"+title)==False:
        os.makedirs(date+"/"+title)
    for link in img_list:
        link = link.get("data-src")
        print(link)
        with open(date+"/"+title+"/"+link.split("/")[-1], "wb") as f:
            pic = requests.get(link, headers=headers)
            f.write(pic.content)
            f.close()
        time.sleep(1)
    # filesys = os.path.dirname(os.path.realpath(__file__))+"\\"+date+"\\"+ title
    # os.system("explorer "+filesys)
    #print(filesys)

    print("==========={}已完成，暂停5秒等待中=========".format(title))
    time.sleep(5)
os.system('explorer.exe .\\')
