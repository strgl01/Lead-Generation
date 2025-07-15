from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import random
import time
import pandas as pd
from typing import Optional

proxies=["45.127.248.127:5128",
     "173.0.9.209:5792",
     "166.88.58.10:5735"]


topics= ["roofing business USA",]
proxy=random.choice(proxies)
class Content:

    def __init__(self, result:str,company:str,rating:str,website:str, mobile:str,open:str) -> None:
        self.result=result
        self.company=company
        self.rating=rating
        self.website=website
        self.mobile=mobile
        self.open=open

class Storage(Content):
    def __init__(self, result: str, company: str, rating: str, website: str, mobile: str, open:str, proxy:str, topic:str) -> None:
        super().__init__(result, company, rating, website, mobile, open)
        self.extract_obj=Extract(proxy, topic, self)
        
        # code for extract class

    def data_csv(self):
        temp={}
        temp['company']=self.extract_obj.company()
        temp['rating']=self.extract_obj.rating()
        temp['website']=self.extract_obj.website()
        temp['mobile']=self.extract_obj.mobile()
        temp['open']=self.extract_obj.open()
        pd.DataFrame(temp).to_csv('output.csv',index=False)

class Crawler:
    def __init__(self,proxy:str) -> None:
        custom_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br, zstd',
        }

        seleniumwire_options = {
        # 'request_storage_base_dir': 'requests',  # Optional: to store requests
        'custom_headers': custom_headers,
        'proxy': {
                'http': f'http://tlwiyzum:qkulf63de7nh@{proxy}',
                'https': f'http://tlwiyzum:qkulf63de7nh@{proxy}',
                'no_proxy': 'localhost,127.0.0.1'  # Exclude localhost
                }
        }

        service = Service(geckodriver_path = r"C:/Users/dell/Desktop/geckodriver.exe")
        options = Options()
        #options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
        self.driver = webdriver.Firefox(service=service, options=options, seleniumwire_options=seleniumwire_options)



    def search(self,topic:str) -> Optional[bytes]:
        self.driver.get('https://www.google.com/maps/')
        time.sleep(30)
        ele=self.driver.find_element(By.CSS_SELECTOR,'input.searchboxinput')
        ele.send_keys(topic)
        ele.send_keys(Keys.RETURN)
        time.sleep(30)
        scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        self.scroll_within_element(scrollable_div)
        
        return self.driver.page_source



    def scroll_within_element(self,element):
        total_height = 0
        distance = 1500
        scroll_pause_time = 30
        count=0

        while True:
            count=count+1
            print(count)
        # Scroll down by the distance
            self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);",element, distance)
            time.sleep(scroll_pause_time)  # Wait to load new content
        
        # Calculate the new scroll height and check if more content is loaded
            new_scroll_height = self.driver.execute_script("return arguments[0].scrollHeight;", element)
            print(new_scroll_height,total_height)
            if new_scroll_height == total_height:
                print('scrolling complete')
                break
            total_height = new_scroll_height

class Extract(Crawler):
    def __init__(self, proxy: str, topic:str, obj:Storage) -> None:
        super().__init__(proxy)
        self.storage_obj=obj
        self.result=bs(self.search(topic),'lxml').select(self.storage_obj.result)
        # f=open('html.txt','w',encoding='utf-8', errors='ignore')
        # f.write(str(self.result))

    def company(self):
        company=[]
        for result in self.result:
            try:
                company.append(result.select(self.storage_obj.company)[0].get_text())
            except:
                company.append(None)

        return company

    def rating(self):
        rating=[]
        for result in self.result:
            try:
                rating.append(result.select(self.storage_obj.rating)[0].get_text())
            except:
                rating.append(None)

        return rating

    def website(self):
        website=[]
        for result in self.result:
            try:
                website.append(result.select(self.storage_obj.website)[0].get('href'))
            except:
                website.append(None)

        return website

    def mobile(self):
        mobile=[]
        for result in self.result:
            try:
                mobile.append(result.select(self.storage_obj.mobile)[0].get_text())
            except:
                mobile.append(None)
        return mobile

    def open(self):
        open=[]
        for result in self.result:
            try:
                open.append(result.select(self.storage_obj.open)[0].get_text())
            except:
                open.append(None)
        return open


for topic in topics:
    Storage("div.lI9IFe","div.fontHeadlineSmall","span.MW4etd", "a.lcr4fd", "span.UsdlK", "span:contains('Opens')", proxy, topic).data_csv()