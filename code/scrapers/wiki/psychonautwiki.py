import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time

class PsychonautWikiScraper():
	def __init__(self):
		self.url = 'https://psychonautwiki.org'

	# get synonyms of one NPS from its page
	def get_nps_synonyms(self, url):
		names = []
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		table = soup.find('table', id='InfoTable')
		if not table:
			return None
		for row in table.findAll('tr'):
			if not row.find('th'):
				continue
			if 'common name' in row.find('th').text.strip().lower():
				td = row.find('td').text.strip()
				names.extend([n.strip() for n in td.split(', ')])
			if 'substitutive name' in row.find('th').text.strip().lower():
				td = row.find('td').text.strip()
				names.extend([n.strip() for n in td.split(', ')])
				print(names)
				return names

	# get all NPS of one category from main wiki page
	def get_category_nps(self, category=''):
		drugs = []
		print(category)
		url = 'https://psychonautwiki.org/wiki/Main_Page'
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		lis = soup.findAll('li', class_='featured list-item')
		for li in lis:
			if li.find('span', class_='mw-headline').find('a'):
				if li.find('span', class_='mw-headline').find('a').text.strip() != category:
					continue
			else:
				continue
			cat_div = li.find('div', class_='media-body')
			break

		for a in cat_div.findAll('a'):
			if a.text.strip() == category:
				continue
			drugs.append(self.get_nps_synonyms(self.url + a['href']))
		return drugs

	def get_drugs_all_categories(self):
		categories = [
		'Novel psychedelics', 
		'Dissociatives', 
		'Depressants', 
		'Cannabinoids', 
		'Stimulants', 
		'Nootropics'
		]
		drugs = []
		for c in categories:
			drugs.extend(self.get_category_nps(c))

		f = open('../../../corpus/wiki/psychonautwiki.txt','w')
		for drug in drugs:
			print(drug)
			if not drug:
				continue
			to_write = '||'.join(drug) + '\n'
			f.write(to_write)
		f.close()

scraper = PsychonautWikiScraper()
scraper.get_drugs_all_categories()

# category = 'Novel psychedelics'
# scraper.get_category_nps(category)