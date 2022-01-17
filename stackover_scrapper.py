


import requests
import datetime
from bs4 import BeautifulSoup
from requests.api import get
from selenium import webdriver


urls =[""]

# def main():

    

#     browser = webdriver.Chrome()
#     browser.get("https://www.youtube.com/feed/trending")
#     content = browser.page_source.encode('utf-8').strip()
#     soup = BeautifulSoup(content, 'lxml')
#     title = soup.find_all('a', id='video-title')
#     print(title)
# # URL = f"https://stackoverflow.com/jobs?q=python&sort=i"


# 마지막 페이지번호 가져오기
def get_last_page(url):
    
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page  = pages[-2].get_text(strip=True)
	
    print(last_page)
    return int(last_page)


#===================================================================================================

# 공고목록  세트로 리턴
def extract_job(html):
    
    title = html.find("div", {"class":"flex--item fl1"}).find("h2").find("a")["title"]
    company,location = html.find("h3", {"class":"fc-black-700 fs-body1 mb4"}).find_all("span", recursive=False) #recursive span안에 다른 span은 안가져옴
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\r")
    job_id =  html['data-result-id']
    # print(f"https://stackoverflow.com/jobs/{job_id}")

    return  {'title':title,
             'company':company,
             'location':location ,
             'link' : f"https://stackoverflow.com/jobs/{job_id}"}


#===================================================================================================

# 마지막 페이지번호 가져오기
def extrcat_jobs(last_pages,url):

    jobs = []

    for page in range(last_pages):
        print('Scrapping StackOverflow: Page: {}'.format(page))
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)


    return jobs


#===================================================================================================


def get_jobs(text):
    
    url = f"https://stackoverflow.com/jobs?q={text}&sort=i"
    last_pages = get_last_page(url)
    jobs = extrcat_jobs(last_pages,url)

    return jobs

