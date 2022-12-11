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

	# get threads and their details and call write function
	def get_threads(self, page=1):
		print("page: ", page)
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
			try:
				thread_id = int(thread_url.split('.')[-1].replace('/',''))
			except:
				print("ID ERROR")
				continue

			thread_title = title_div.text.strip()

			try:
				thread_username = div.find('a', class_='username').text.strip()
				thread_user_url = self.url + div.find('a', class_='username')['href']
				thread_user_id = int(thread_user_url.split('/')[-2].split('.')[1])
				#print(type(thread_user_id))
			except:
				print("CREATED BY ERROR")
				continue

			thread_date = div.find('li', class_='structItem-startDate').find('time')['datetime'][0:10]

			thread_comments = int(detail_div.findAll('dd')[0].text)
			
			thread_views = detail_div.findAll('dd')[1].text
			if 'K' in thread_views:
				thread_views = int(thread_views.split('K')[0])*1000

			threads.append(DrugsForumThread(
				url = thread_url,
				title = thread_title,
				username = thread_username,
				user_id = thread_user_id,
				user_url = thread_user_url,
				date = thread_date,
				views = thread_views,
				comments = thread_comments,
				thread_id = thread_id,
				forum = 'drugsforum'
			))

		for i,thread in enumerate(threads):
			thread.get_thread_content()
			print(i,thread.thread_id, thread.title)
		self.write_threads(threads, page)

	def get_comments_of_thread(self, thread_url):
		comments = []
		r = requests.get(thread_url)
		soup = BeautifulSoup(r.content, 'html.parser')
		articles = soup.findAll('article', class_='message--post')

		for article in articles:
			#comment_username = article['data-author']
			h4 = article.find('h4')
			comment_user_url = self.url + h4.find('a')['href']
			comment_username = h4.text
			comment_user_id = h4.find('a')['data-user-id']

			comment_id = int(article['data-content'].split('-')[-1])
			comment_date = article.find('time')['datetime'][0:10]

			thread_id = int(thread_url.split('.')[-1].replace('/',''))

			# getting content of comment and removing quoted parts from it
			message_body = article.find('article', class_="message-body")
			quoted = []
			for t,c in zip(message_body.findAll('div', class_='bbCodeBlock-title'), message_body.findAll('div', class_='bbCodeBlock-content')):
				quoted.append(t.text)
				quoted.append(c.text)

			content = message_body.text
			for q in quoted:
				content = content.replace(q, '')
			content = content.replace('\n', ' ')

			comments.append(Comment(
				user_url = comment_user_url,
				user_id = comment_user_id,
				username = comment_username,
				comment_id = comment_id,
				thread_id = thread_id,
				thread_url = thread_url, 
				content = content, 
				date = comment_date,
				forum = 'drugsforum'))
			print(comment_username)
		self.write_comments(comments)	


scraper = DrugsForumScraper()
for i in range(1,48):
	scraper.get_threads(i)

# url = 'https://drugsforum.nl/threads/4f-mph-of-3-cmc.73388/'
# scraper.get_comments_of_thread(url)