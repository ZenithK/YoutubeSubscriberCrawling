import time
import csv

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options

def press_btn(driver):
     cnt  = 0
     while True :
          try :
               elements = driver.find_elements_by_xpath("//button[@aria-label='다음']")
               for element in elements :
                    element.click()
               cnt += 1
               if cnt > 3 :
                    break
          except Exception :
               break

f = open('data.csv','a',encoding='utf-8', newline='')
wr = csv.writer(f)

driver = wd.Firefox(executable_path="C:/Users/LeeSeongHwan/Desktop/geckodriver.exe")
driver.set_page_load_timeout(3600)

# INPUT YOUTUBE URL
url = "https://www.youtube.com/watch?v=sXWlX8eqfTc"       # 댓글 수집할 Youtube URL입력
driver.get(url)

driver.maximize_window()

last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(5.0)       # 인터발 1이상으로 줘야 데이터 취득가능(롤링시 데이터 로딩 시간 때문)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height

html_source = driver.page_source
soup = BeautifulSoup(html_source,"html.parser")

a_tags = soup.find_all("a",{'class':"ytd-comment-renderer"})

base_url = "http://www.youtube.com"

count = 0

for a_tag in a_tags:
    # prevent double request occured by no reason
    if count%2 == 0 :
        user_channel = base_url+a_tag["href"]
        user_id = a_tag["href"][9:]
        
        driver.get(user_channel)
        source = driver.page_source
        soup2 = BeautifulSoup(source,"html.parser")
        
        
        # Scroll for All Subscriber information
        
        press_btn(driver)
        
        try :
             source = driver.page_source
             soup2 = BeautifulSoup(source,"html.parser")
        except Exception:
             continue
             
        # find All Subscriber information
        user_subscribers = soup2.find_all("a",{'id':"channel-info",'class':"ytd-grid-channel-renderer"})

        # get subscriber inherent channel id
        for user_subscriber in user_subscribers :
            try :
               if (user_subscriber["href"][1:8]) == "channel" :
                     wr.writerow([user_id,user_subscriber["href"][9:]])
               else :
                    channel = base_url+user_subscriber["href"]
                    driver.get(channel)
                    wr.writerow([user_id, driver.current_url[32:]])
            except Exception:
                continue
    count += 1
    
driver.close()
f.close()
