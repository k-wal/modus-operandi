import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time
import json
from newspaper import Article

# class TelegraafScraper():

# 	def __init__(self):
# 		self.main_url = 'https://www.telegraaf.nl'

# 	# return title, text for a particular article
# 	def get_text(self, url):
# 		r = requests.get(url)
# 		soup = BeautifulSoup(r.content, 'html.parser')
# 		print(soup)
# 		title = soup.find('h1', class_='ArticleTitleBlock__title ArticleTitleBlock__title--chapeau').text
# 		print(title)
		
# 		text = []
# 		sc = soup.find("script").text
# 		data = sc.split("=", 1)[1]
# 		ld = json.loads(data)
# 		print(ld)
# 	#	return title, text



url = 'https://www.telegraaf.nl/sport/772235966/us-open-verrassing-brouwer-snakt-naar-terugvlucht-na-maandenlange-trip'
# scraper = TelegraafScraper()
# scraper.get_text(url)

article = Article(url)
article.download()
article.parse()
article.text