import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time

class NOSScraper:

	def __init__(self):
		self.main_url = 'https://nos.nl'


	# return title, text for a particular article
	def get_text(self, url):
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		title = soup.find('title').text
		
		text = ''
		divs = soup.findAll('div', 'sc-daa8fdde-1 kDUyiX')
		for div in divs:
			if div.find('aside'):
				continue
			#print(div)
			p = div.find('p', 'sc-d176aaed-0 blKpuK')
			if p:
				text += p.text
		return title, text


	# scrape and write a day's articles
	# format of date_string: yyyy-mm-dd
	def get_day_articles(self, date_string, dir_path):
		print('\n'+ date_string + '------------------- \n')
		url = 'https://nos.nl/nieuws/archief/' + date_string
		all_articles = []
		r = requests.get(url)
		soup = BeautifulSoup(r.content,'html.parser')

		li_list = soup.findAll('li', 'list-time__item')
		for li in li_list:
			href = li.find('a')
			link = self.main_url + href['href']
			


date_string = '2022-08-01'
dir_path = '../../corpus/nos/2022-08'

scraper = NOSScraper()
#scraper.get_day_articles(date_string, dir_path)
url = 'https://nos.nl/artikel/2439132-president-santokhi-doet-beloftes-maar-betogers-paramaribo-zijn-niet-tevreden'
scraper.get_text(url)