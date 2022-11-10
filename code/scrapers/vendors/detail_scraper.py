from bs4 import BeautifulSoup 
from bs4.element import Comment
import os
import datetime
import time
import requests
import re

class DetailScraper():
	def tag_visible(self,element):
		if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
			return False
		if isinstance(element, Comment):
			return False
		return True

	def text_from_html(self, soup):
		texts = soup.findAll(text=True)
		visible_texts = filter(self.tag_visible, texts)  
		return u" ".join(t.strip() for t in visible_texts)

	def get_phone(self, soup, response):
		visible_text = self.text_from_html(soup)
		try:
			phone = soup.select("a[href*=callto]")[0].text
			return phone
		except:
			pass
		r_string = r'\+[ ]*3[ ]*1[ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9]'

		try:
			phone = re.findall(r_string, visible_text)[0]
			return phone.replace(' ','')
		except:
			pass

		try:
			phone = re.findall(r_string, visible_text)[-1]
			return phone.replace(' ','')
		except:
			pass

		try:
			r_string = r'[0]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9]'
			phone = re.findall(r_string, visible_text)[0]
			return phone.replace(' ','')

		except:
			print ('Phone number not found')
			phone = ''
			return phone

	def get_details(self, url):
		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		print(self.get_phone(soup, response))


#url = 'https://funcaps.nl'
#url = 'https://homechemistry.nl/shop/chemicals/'
url = 'https://realchems.nl/'

scraper = DetailScraper()
scraper.get_details(url)