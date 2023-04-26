from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm #progress bar 생성
import time
from tqdm.notebook import tqdm
import pandas as pd

#홈페이지 열기
driver = webdriver.Chrome("C:\chromedriver_win32 (1)\chromedriver")
url = "https://factcheck.snu.ac.kr/"
driver.get(url)

#공지사항 지우기
driver.find_element_by_xpath('/html/body/div[5]/div[2]/label').click()
driver.find_element_by_xpath('/html/body/div[4]/div[2]/label').click()


#검색창에 검색어 입력하기
input_  = driver.find_element_by_xpath('//*[@id="gnb"]/div/div/form/fieldset/input')
input_.send_keys("카카오")

#검색버튼 클릭하기
btn_search = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/form/fieldset/button')
btn_search.send_keys(Keys.ENTER)

#페이지를 넘기면서 href를 포함하는 element 가져오기
def get_urls(page_num):

    href_list = []
    
    for i in range(page_num):
        page_btn_xpath = '//*[@id="pagination"]/div/'+'a['+str(i+3)+']'
        driver.find_element_by_xpath(page_btn_xpath).click()
        page_urls = driver.find_elements_by_xpath('//*[@id="container"]/div/div[3]/div/ul/li/div/div[1]/div[3]/p[1]/a')
        
        for page in page_urls:
            href_list.append(page.get_attribute('href'))
            
    return href_list

href_list = get_urls(3)

#category, speaker, title, source, veracity, logo_url 가져오기
def element_to_text(url):
    
    driver.get(url)
    
    category= driver.find_element_by_xpath('//*[@id="content_detail"]/div/div[3]/div[1]/div/div[2]/div[2]/ul')
    speaker = driver.find_element_by_xpath('//*[@id="content_detail"]/div/div[3]/div[1]/div/div[1]/p')
    title = driver.find_element_by_xpath('//*[@id="content_detail"]/div/div[3]/div[1]/div/div[2]/div[1]/p[1]/a')
    source = driver.find_element_by_xpath('//*[@id="content_detail"]/div/div[3]/div[1]/div/div[2]/div[1]/p[2]')
    veracity = driver.find_element_by_xpath('//div[starts-with(@id,"meter-item")]/div[2]')
    logo_url = driver.find_element_by_xpath('//li[starts-with(@id, "score")]/div/div[1]/div[2]/ul/li/img').get_attribute('src')
    
    return {
        'category': category.text,
        'speaker': speaker.text,
        'title': title.text,
        'source': source.text,
        'veracity': veracity.text,
        'logo_url': logo_url
    }

data = []
pbar = tqdm(range(len(href_list)))

for href in href_list:
    article_info = element_to_text(href)
    data.append(article_info)
    time.sleep(3)
    pbar.update()
    
pbar.close()

#크롤링 결과를 csv파일로 저장하기
df = pd.DataFrame(data)
df.to_csv('kakako_news.csv', index=False, encoding='utf-8-sig')
