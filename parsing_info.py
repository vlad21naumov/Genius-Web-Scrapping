import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# make webdriver to click "Load more" button
driver = webdriver.Chrome(options=Options())
driver.get('https://genius.com/#top-songs')

num_clicks = 5 # you can change it to load more top songs!
driver.get('https://genius.com/#top-songs');
for n in range(5):
    button = driver.find_element(By.XPATH, '//*[@id="top-songs"]/div/div[3]/div')
    button.click()
    time.sleep(0.7)

page = driver.page_source

soup = BeautifulSoup(page, 'lxml')
boxes = soup.find_all('div', class_='PageGridFull-sc-18uuafq-0 kfrnFZ')[0]
box_links = boxes.find_all('a', href=True)
song_pages = []
for link in box_links:
    song_pages.append(link['href'])

songs_data = []
links = []
for link in song_pages:
    links.append(link)
    song_request = requests.get(link)
    song_soup = BeautifulSoup(song_request.content, 'lxml')

    song_name = song_soup.find('span', class_='SongHeaderdesktop__HiddenMask-sc-1effuo1-11 iMpFIj').text
    try:
        song_author = song_soup.find('a', class_='Link__StyledLink-rwn6i6-0 kMnVYG HeaderArtistAndTracklistdesktop__Artist-sc-4vdeb8-1 jhWHLb').text
    except:
        song_author = 'can not find author :('
    soup_song_info = song_soup.find_all('span', class_='LabelWithIcon__Label-hjli77-1 hgsvkF')
    if len(soup_song_info) < 3:
        continue
    song_date = soup_song_info[0].text
    song_num_viewers = soup_song_info[1].text
    try:
        song_num_views = soup_song_info[2].text
    except:
        song_num_views = 'no info :('

    song_dict = {
        'Name': song_name.replace('\u200b', '').replace('\n', ''),
        'Author': song_author,
        'Release date': song_date,
        '№ viewers': song_num_viewers,
        '№ views': song_num_views
    }

    songs_data.append(song_dict)

top_songs = pd.DataFrame(songs_data)
top_songs.to_csv('Genius_top_songs.csv')
