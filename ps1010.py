from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

import pandas as pd
import time
import datetime


def get_link():

    url = 'https://www.youtube.com/feed/trending'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver.exe',options=options)
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    driver.close()

    # name = soup.select('a#video-title')
    video_url = soup.select('a#video-title')
    # view = soup.select('a#video-title')

    
    url_list = []
    

    for i in video_url:
        url_list.append('{}{}'.format('https://www.youtube.com',i.get('href')))
        
    youtubeDic = {'Addr': url_list}

    youtube_df = pd.DataFrame(youtubeDic)
    youtube_df = youtube_df[~youtube_df['Addr'].str.contains('shorts')]# 쇼츠 영상 제외
    print(youtube_df)
    
    return youtube_df


def get_hash_tag(youtube_df):
    
    url_list = []
    tag_list = []
    date = []
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    
        
    for url in youtube_df['Addr']:
        
        
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # 이미지 로드 x 옵션
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome('./chromedriver.exe',options=options)
        driver.set_window_size(1200, 1080)
        driver.get(url)
        driver.implicitly_wait(10)
        actions = ActionChains(driver)
        wait = WebDriverWait(driver, 10)

        try:
            time.sleep(2.8)    
            driver.implicitly_wait(15)
            button = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="more"]/yt-formatted-string')))

            # 더보기 버튼 클릭액션
            driver.implicitly_wait(15)
            actions.move_to_element(button).click().perform()
            time.sleep(1)

            #태그 불러오기
            driver.implicitly_wait(15)
            hash_tag_size =  wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="description"]/yt-formatted-string')))

            #태그 갯수
            driver.implicitly_wait(15)
            tag_len = len(hash_tag_size.find_elements(By.TAG_NAME,'a'))
            
            
            for i in range(tag_len):

                print('-----', i + 1, '-----')
                size = i+1
                driver.implicitly_wait(10)
                tag = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="description"]/yt-formatted-string/a[{}]'.format(size))))
                print(tag.text)
                tag_list.append(tag.text)
                url_list.append(url)
                date.append(date_now)

            test = {'tags': tag_list, 'URL':url, 'DATE' :date}
            df_tags = pd.DataFrame(test)
            df_tags['tags'] = df_tags['tags'].str.replace('[#,@,&]', '',regex=True)
            df_result = df_tags[df_tags['tags'].str.contains(':') & ~df_tags['tags'].str.contains('#') == False & ~df_tags['tags'].str.contains('https',na=True) ]
            

            print("*" * 30)
            print(df_result)
            print("*" * 30) 
            
            driver.quit()
        except:
            print("----error----")
            driver.quit()

    list = {'tags':tag_list, 'URL':url_list, 'DATE' : date}
    df_list = pd.DataFrame(list)
    df_list['tags'] = df_list['tags'].str.replace('[#,@,&]', '',regex=True)
    df_result = df_list[df_list['tags'].str.contains(':') & ~df_list['tags'].str.contains('#') == False & ~df_list['tags'].str.contains('https',na=True) ]
    print("!!!!!!!!!----END----!!!!!!!!")

    return df_result



if __name__ == '__main__':

    get_link()
    print('')
