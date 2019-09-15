#!/usr/bin/python3
# monitorHomepage.py checks www.upce.cz/en for changes in its content

import requests, logging, shelve, os
from bs4 import BeautifulSoup

logging.basicConfig(filename = 'monitorHomepage.log',level = logging.DEBUG, format ='%(asctime)s - %(levelname)s - %(message)s')

resHomepage = requests.get('http://www.upce.cz/en') #scrape homepage
resHomepage.raise_for_status() #check if download was successful

soupHomepage = BeautifulSoup(resHomepage.text, 'html.parser') #parse homepage

#Create list of various titles found on homepage, css style has banner_subtitle, banner_title and news_title classes
soupSubtitles = soupHomepage.select('.banner_subtitle a')
soupNewsTitles = soupHomepage.select('.news_title a')
soupBannerTitles = soupHomepage.select('.banner_title a')

subtitles = [] 
for subtitle in soupSubtitles:
	subtitles.append(subtitle.get_text())

newsTitles = []
for newsTitle in soupNewsTitles:
	newsTitles.append(newsTitle.get_text())

bannerTitles = []
for bannerTitle in soupBannerTitles:
	bannerTitles.append(bannerTitle.get_text())

logging.debug('I have found the following titles: {} {} {}'.format(bannerTitles, newsTitles, subtitles))

#read file with title from previous check if it exists
if os.path.exists('previousCheck.db') == False:
	logging.debug('Data from previous file not found')
with shelve.open('previousCheck.db') as storage:
	try:
		previousBannerTitles = storage['bannerTitles']
		previousNewsTitles = storage['newsTitles']
		previousSubtitles = storage['subtitles']
	except KeyError:
		logging.debug('One of the variables was not found in previous database')

#TODO:check current titles with previous titles
for title in previousBannerTitles:
	if title in bannerTitles:
		print('No changes in banner title')
	if title not in bannerTitles:
		print(title + ' has dissapeared')

for title in previousNewsTitles:
	if title in newsTitles:
		print('No changes in banner title')
	if title not in newsTitles:
		print(title + ' has dissapeared')

for title in previousSubtitles:
	if title in subtitles:
		print('No changes in banner title')
	if title not in subtitles:
		print(title + ' has dissapeared')


#overwrite previous titles with current titles for next check
with shelve.open ('previousCheck.db') as storage:
	storage['bannerTitles'] = bannerTitles
	storage['newsTitles'] = newsTitles
	storage['subtitles'] = subtitles

