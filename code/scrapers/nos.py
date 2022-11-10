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
			p = div.find('p', 'sc-d176aaed-0 blKpuK')
			if p:
				text += ' ' + p.text
		return title, text

	# write a day's articles
	def write_day_articles(self, articles, filename, dir_path):
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)
		file = open(dir_path + '/' + filename + '.txt', 'w')
		for article in articles:
			title, text, url, date = article['title'], article['text'], article['url'], article['date']
			to_write = '||'.join([date, title, text, url])
			file.write(to_write + '\n')
		file.close()

	# scrape and write a day's articles
	# format of date_string: yyyy-mm-dd
	def get_day_articles(self, date_string, dir_path):
		print('\n'+ date_string + '------------------- \n')
		url = 'https://nos.nl/nieuws/archief/' + date_string
		all_articles = []
		r = requests.get(url)
		soup = BeautifulSoup(r.content,'html.parser')

		li_list = soup.findAll('li', 'list-time__item')
		for index, li in enumerate(li_list):
			href = li.find('a')
			link = self.main_url + href['href']
			try:
				title, text = self.get_text(link)
			except:
				print("ERROR")
				continue
			print(index, title)
			article = {'date':date_string, 'url':link, 'title':title, 'text':text}
			all_articles.append(article)

		self.write_day_articles(all_articles, date_string, dir_path)

	# get articles in the given interval (both dates included; format yyyy-mm-dd)
	def get_interval_articles(self, start_string, end_string, dir_path = '../../corpus/nos'):
		start_date = datetime.datetime.strptime(start_string, "%Y-%m-%d")
		end_date = datetime.datetime.strptime(end_string, "%Y-%m-%d")

		cur_date = start_date
		while cur_date <= end_date:
			date_string = datetime.datetime.strftime(cur_date, "%Y-%m-%d")
			month_string = datetime.datetime.strftime(cur_date, "%Y-%m")
			cur_dir_path = dir_path + '/' + month_string
			self.get_day_articles(date_string, cur_dir_path)

			time.sleep(3)
			cur_date += datetime.timedelta(days=1)	


start_string = '2021-09-01'
end_string = '2021-12-31'

scraper = NOSScraper()
scraper.get_interval_articles(start_string, end_string)
