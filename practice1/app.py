from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_page_count(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    base_url = "https://kr.indeed.com/jobs?q="

    browser.get(base_url+keyword)
    response = browser.page_source

    soup = BeautifulSoup(response, 'html.parser')
    pagination = soup.select("nav > div > a")
    if pagination == None:
        print("page is only one")
    for page in pagination:
        print(page["href"])


get_page_count("frontend")


def extract_indeed_jobs(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    base_url = "https://kr.indeed.com/jobs?q="

    browser.get(base_url+keyword)
    response = browser.page_source

    soup = BeautifulSoup(response, 'html.parser')
    lists = soup.select(".jobsearch-ResultsList > li", recursive=False)
    for job in lists:
        zone = job.select_one(".mosaic-zone")
        if zone == None:
            ancher = job.select_one("h2 a")
            title = ancher['aria-label']
            link = ancher['href']
            print(title)
            print("///\n///")
