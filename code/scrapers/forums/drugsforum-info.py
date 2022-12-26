import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time
from classes import *
import pandas as pd


class DrugsForumNLThread(Thread):
	# get thread content and date here; everything else should be done through drugsforumscraper
	def get_thread_date_content(self):
		month_dict = {'jan':'01',
		'feb':'01',
		'maart':'03',
		'apr':'04',
		'mei':'05',
		'jun':'06',
		'jul':'07',
		'aug':'08',
		'sep':'09',
		'okt':'10',
		'nov':'11',
		'dec':'12',
		}

		r = requests.get(self.url)
		soup = BeautifulSoup(r.content, 'html.parser')
		div = soup.find('div', 'post')
		try:
			par = div.find('p', class_='author')
			text = par.text.replace(par.find('strong').text, '')
			text = text[8:].split(' ')
			month = month_dict[text[1]]
			date = text[2].replace(',','')
			year = text[3]
			date = '-'.join([year, month, date])
		except:
			print(self.url)
			date='something'		

		try:
			content = div.find('div', 'content').text.strip()
		except:
			content='something'
		
		return date, content

# main drugsforum.info scraper
class DrugsForumInfoScraper():
	def __init__(self):
		self.url = 'https://drugsforum.info'
		self.dir_path = '../../../corpus/forums/drugsforumInfo'

	# write list of Thread objects in a csv file
	def write_threads(self, threads, page):
		dir_path = self.dir_path + '/threads'
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)
		df = pd.DataFrame.from_records([t.to_dict() for t in threads])
		
		if page == 1:
			df.to_csv(dir_path + '/all.csv', index=False, sep=',')
		else:
			df.to_csv(dir_path + '/all.csv', mode='a', index=False, header=False, sep=',')

	# write list of Comment objects in a csv file
	def write_comments(self, comments):
		dir_path = self.dir_path + '/comments'
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)
		df = pd.DataFrame.from_records([c.to_dict() for c in comments])
		df.to_csv(dir_path + '/all.csv', index=False, sep=',')

	def get_next_page(self, page, url):
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		page_actions = soup.find('form', action=url)
		links = page_actions.findAll('a')
		for a in links:
			# only take the a tag that refers to next page
			if a.text != 'Volgende':
				continue
			print(a['href'])
			self.get_threads(page=page+1, url=a['href'])
			break


	# get threads and their details and call write function
	def get_threads(self, page=1, url = 'http://drugsforum.info/research-chemicals/'):
		print("page: ", page)
		threads = []
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')

		lis = soup.findAll('li', class_='row')
		for li in lis:
			if 'global-announce' in li['class']:
				continue
			if 'sticky' in li['class']:
				continue
			if 'bg1' not in li['class'] and 'bg2' not in li['class']:
				continue

			thread_title = li.find('a', class_='topictitle').text.strip()
			thread_comments = int(li.find('dd', class_='posts').text.strip().split(' ')[0])
			thread_views = int(li.find('dd', class_='views').text.strip().split(' ')[0])
			thread_url = li.find('a', class_='topictitle')['href']
			user_a = li.find('dt').findAll('a')[-1]
			thread_username = user_a.text
			thread_user_url = user_a['href']
			thread_id = int(thread_url.split('/')[-1].split('-')[-1].split('.')[0][1:])

			threads.append(DrugsForumNLThread(
				url = thread_url,
				title = thread_title,
				username = thread_username,
			#	user_id = thread_user_id,
				user_url = thread_user_url,
				views = thread_views,
				comments = thread_comments,
				thread_id = thread_id,
				forum = 'drugsforum-info'
			))
		
		for i,thread in enumerate(threads):
			threads[i].date, threads[i].content = thread.get_thread_date_content()
			print(i,thread.thread_id, thread.title)

		self.write_threads(threads, page)
		# get link to next page from the page
		self.get_next_page(page, url)

scraper = DrugsForumInfoScraper()
scraper.get_threads()