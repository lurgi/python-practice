import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb://lurgi:doubleu!2@52.79.132.116/', 27017)
db = client.jungle

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
response = requests.get(
    'https://movie.daum.net/ranking/boxoffice/yearly', headers=headers)


def webScrapping():
    if response.status_code == 200:
        db.movies.drop()
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_list = soup.select(".list_movieranking > li")
        for movie in movie_list:
            image_url = movie.select_one(
                ".thumb_item > .poster_movie > img")["src"]
            age_limit = movie.select_one(
                ".thumb_item > .poster_movie > .txt_tag > span").text
            title = movie.select_one(".thumb_cont > .tit_item > a").text
            movie_url = movie.select_one(".thumb_cont > .tit_item > a")["href"]
            (open_year, open_month, open_day) = movie.select_one(
                ".thumb_cont > .txt_info > .info_txt:nth-child(1) > span").text.split(".")
            views = movie.select_one(
                ".thumb_cont > .txt_info > .info_txt:nth-child(2)").findChild(string=True, recursive=False)
            views_num = int(views.replace(",", "").replace("명", ""))

            movie_data = {
                "image_url": image_url,
                "age_limit": age_limit,
                "title": title,
                "movie_url": movie_url,
                "open_year": open_year,
                "open_month": open_month,
                "open_day": open_day,
                "views_str": views,
                "views_num": views_num,
                "likes": 0,
                "is_deleted": False,
            }
            db.movies.insert_one(movie_data)


webScrapping()
