

#
#1.remember to change your Chrome User Data path
#
#2.notice to modified path
#
#3.when run this progress must close all Chrome browser
#
#4.Chinese user :首先得能上P站！
#
#
#
#
from bs4 import BeautifulSoup
import re,os,time
import requests
from selenium import webdriver
from lxml import etree
from threading import Thread
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
        , 'Referer':'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=70639869'
    }


def selesearch(keys,hot,page):
    print("跳转页面中...")
    chrome_dir = r'C:\Users\admin\AppData\Local\Google\Chrome\User Data'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir="+os.path.abspath(chrome_dir))
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    key_meg = keys+hot+'users入り'
    driver.get('https://www.pixiv.net/tags/%s/artworks?p=%d&s_mode=s_tag'%(key_meg,page)) 
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    html = driver.page_source
    driver.close
    return html
    # driver.find_elements_by_css_selector("[class='sc-LzNPC gYaVLD']")[1].click()
    #找出共多少页
    # pages = len(driver.find_elements_by_css_selector("[class='sc-LzNPC gYaVLD']"))
    # print(pages)
    # #返回页面
     
    #  #由于是分页式加载
    # html_list=[]
    # for i in range(pages):
    #     driver.find_element_by_css_selector("[class='sc-LzNPC gYaVLD']")[i].click()
    #     time.sleep(2)
    #     html_list.append(driver.page_source)
def re_html(html):
    print("开始解析页面...")
    dom = etree.HTML(html)
    #找图片地址
    imgs = dom.xpath('//img[contains(@src,"1200")]/@src')
    print(imgs)
    #找图片名字
    img_name =dom.xpath('//img[contains(@src,"1200")]/@alt')

    url_png_list = []
    url_jpg_list = []
    for img in imgs:
        url_png ='https://i.pximg.net/img-original/img/'+re.findall(r'/img/(.+?)_',img)[0]+'_p0.png'
        
        url_png_list.append(url_png)
        url_jpg ='https://i.pximg.net/img-original/img/'+re.findall(r'/img/(.+?)_',img)[0]+'_p0.jpg'
        url_jpg_list.append(url_jpg)
    
    #把url和图片名字转化成元组再转为字典
    png_msg = {}
    jpg_msg = {}
    png_msg = dict(zip(url_png_list,img_name))
    
    jpg_msg = dict(zip(url_jpg_list,img_name))
    
    #把两个字典结合
    url_msg = png_msg.copy()
    url_msg.update(jpg_msg)
    
    return url_msg
    
def download(url_msg,address,keys):
    print("正在下载...")
    #P给图片取名
    path = address+keys+'/'
    if not os.path.exists(path):
        os.mkdir(path)
    
    # urls = url_msg.keys

    #取字典的key和value
    for key,values in tqdm(url_msg.items()):
        try:
            r = requests.get(key,headers=headers)
            if r.status_code ==200:
                with open('%s%s.jpg'%(path,values),'wb') as f:
                    f.write(r.content)
                    f.close()
        except:
                continue

def begin(keys,hot,address):
    page = 1
   
    while page>0:
        print("开始爬取第%d页..."%page)

        html = selesearch(keys,hot,page)

        url_msg = re_html(html)

        #如果是空列表，证明到底了，返回

        if len(url_msg) ==2 :
            return
        t = Thread(target=download,args=(url_msg,address,keys))
        t.start()
        t.join()
        page = page+1
        
    
if __name__ == "__main__":

    #parameter: keys, hot ,path
   begin('風景','10000','I://landscape/')
