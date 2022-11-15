import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time
from classes import *
import pandas as pd

class DrugsForumThread(Thread):
	# get thread content here; everything else should be done through drugsforumscraper
	def get_thread_content(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.content, 'html.parser')
		self.content = soup.find('article', class_='message-body js-selectToQuote').text.replace('\n',' ')

# main drugsforum.nl scraper
class DrugsForumScraper():
	def __init__(self):
		self.url = 'https://drugsforum.nl'
		self.dir_path = '../../../corpus/forums/drugsforum'

	# write list of Thread objects in a csv file
	def write_threads(self, threads):
		dir_path = self.dir_path + '/threads'
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)
		df = pd.DataFrame.from_records([t.to_dict() for t in threads])
		df.to_csv(dir_path + '/all.csv', sep=',')


	# get threads and their details and call write function
	def get_threads(self):
		page = 1
		url = 'https://drugsforum.nl/forums/research-chemicals.37/page-'+str(page)+'?order=post_date&direction=desc'
		threads = []
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		divs = soup.findAll('div', class_='structItem-cell structItem-cell--main')
		detail_divs = soup.findAll('div', class_='structItem-cell structItem-cell--meta')
		for div, detail_div in zip(divs, detail_divs):
			sticky_i = div.find('i', class_='structItem-status structItem-status--sticky')
			if sticky_i:
				continue
			
			title_div = div.find('div', class_='structItem-title')
			thread_url = self.url + title_div.find('a')['href']
			thread_title = title_div.text.strip()

			thread_created_by = div.find('a', class_='username').text.strip()
			thread_date = div.find('li', class_='structItem-startDate').find('time')['datetime'][0:10]

			thread_comments = int(detail_div.findAll('dd')[0].text)
			
			thread_views = detail_div.findAll('dd')[1].text
			if 'K' in thread_views:
				thread_views = int(thread_views.split('K')[0])*1000

			threads.append(DrugsForumThread(
				url = thread_url,
				title = thread_title,
				created_by = thread_created_by,
				date = thread_date,
				views = thread_views,
				comments = thread_comments
			))

		for i,thread in enumerate(threads):
			thread.get_thread_content()
			print(i,thread.title,thread.date)
		self.write_threads(threads)

scraper = DrugsForumScraper()
scraper.get_threads()