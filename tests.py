# from django.test import TestCase


from bs4 import BeautifulSoup
import requests
from selenium import webdriver

class crwaling:
    driver = webdriver.Chrome('/Users/seilylook/Downloads/chromedriver')
    url = 'https://www.mangoplate.com/top_lists/661_yeouido'
    driver.get(url)
    driver.implicitly_wait(20)


    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    imgs= soup.find_all("img")
    # print(type(imgs))
    # print(imgs)

    imgs= soup.find_all("img", attrs={'class': 'center-croping lazy'})
    
# Create your tests here.
