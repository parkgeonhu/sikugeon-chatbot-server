import requests
import json
from bs4 import BeautifulSoup


def get_image_url(query):
    url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='+query

    response=requests.get(url)


    soup = BeautifulSoup(response.text, "lxml")
    img = soup.find(class_='_img')
    if img is None:
        pic_url=""
    else:
        pic_url = img['data-source']
    
    return pic_url