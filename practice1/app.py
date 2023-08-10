from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)

base_url = "https://kr.indeed.com/jobs?q="
search_input = "frontend"

browser.get(base_url+search_input)
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
