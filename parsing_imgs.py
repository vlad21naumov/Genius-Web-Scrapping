from parsing_info import links
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import tqdm
import os

# directory is already made
# os.mkdir('song_images')

browser = webdriver.Chrome()
# takes some time to scrap all pictures
for link in tqdm.tqdm(links):
    img_name = link.split('/')[-1]
    browser.get(link)
    res = browser.page_source
    image_soup = BeautifulSoup(res, 'html.parser')
    img_elems = image_soup.find('img').get('src')
    img_response = requests.get(img_elems)
    with open(f"song_images/{img_name}.jpg", "wb") as f:
        f.write(img_response.content)
