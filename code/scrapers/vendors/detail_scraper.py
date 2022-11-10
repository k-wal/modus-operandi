from bs4 import BeautifulSoup 
import os
import datetime
import time


class DetailScraper():
	def get_email(self, soup):
		try:
			phone = soup.select("a[href*=callto]")[0].text
			return phone
		except:
			pass

		try:
			phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', response.text)[0]
			return phone
		except:
			pass

		try:
		   phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', response.text)[-1]
		   return phone
		except:
			print ('Phone number not found')
			phone = ''
			return phone


	