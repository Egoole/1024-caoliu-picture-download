import threading
import queue as Queue
import random
import time
import requests
import os
from bs4 import BeautifulSoup
import datetime



date = datetime.datetime.now().strftime('%Y-%m-%d')

class Producter(threading.Thread):
    """生产者线程"""
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        #打开文件读取地址
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        with open("url.txt", "r")as f:
            url_list = f.readlines()
            f.close()
        print(url_list)
        #将地址放入队列
        for url in url_list:
            url = url.replace("\n", "")
            if len(url) == 0:
                continue
            self.queue.put(url,1)
        print('put queue done')


class ConsumeEven(threading.Thread):
    """奇数消费线程"""

    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        while True:
            if self.queue.qsize()==0:
                print("===队列清空，退出线程{}".format(self.getName()))
                return
            queue_url = self.queue.get(True, 1)
            print('Get URL 【%s】 ' % queue_url)
            headers = {'Referer': 'http://cl.y4e.xyz/thread0806.php?fid=7',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                       }
            re = requests.get(queue_url, headers=headers)
            re.encoding = "gb18030"
            soup = BeautifulSoup(re.text, "html.parser")
            title = soup.title.text.split("- ")[0].replace(" ", "")
            print(title)
            #print(re.text)
            img_list = soup.select("[data-src]")
            #print(img_list)

            if os.path.exists(date+"/"+title) == False:
                os.makedirs(date+"/"+title)
            num = int("000")
            for link in img_list:
                link = link.get("data-src")
                print(link)
                num += 1
                with open(date+"/"+title+"/【"+str(num)+"】"+link.split("/")[-1], "wb") as f:
                    pic = requests.get(link, headers=headers)
                    f.write(pic.content)
                    f.close()
                time.sleep(1)
            # filesys = os.path.dirname(os.path.realpath(__file__))+"\\"+date+"\\"+ title
            # os.system("explorer "+filesys)
            #print(filesys)
            print("==={}========{}已完成，暂停5秒等待中=========".format(self.getName(),title))


q = Queue.Queue()
pt = Producter('producter', q)
pt.start()
pt.join()

for x in range(int(q.qsize()/5)):
    x = ConsumeEven("Thread【{}】".format(x), q)
    x.start()

# ce = ConsumeEven('consumeeven', q)
# ce2 = ConsumeEven('consumeeven222222', q)
# ce.start()
# ce2.start()
